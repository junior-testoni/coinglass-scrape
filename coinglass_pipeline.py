"""Coinglass BTC/ETH Data Pipeline

This script collects several futures indicators from Coinglass and
stores them in a local SQLite database for later analysis. It fetches
open interest, funding rates, long/short ratios and liquidations for a
list of symbols (BTC, ETH by default).

The script requires a Coinglass API key. Provide it with ``--api-key`` or
set the ``COINGLASS_API_KEY`` environment variable.
"""

from __future__ import annotations

import argparse
import logging
import os
import sqlite3
import time
from typing import Iterable

import requests


BASE_URL = "https://open-api-v4.coinglass.com/api"

ENDPOINTS = {
    "open_interest": "/futures/open-interest/aggregated-history",
    "funding_rate": "/futures/funding-rate/oi-weight-history",
    "long_short_ratio": "/futures/top-long-short-account-ratio/history",
    "liquidations": "/futures/liquidation/aggregated-history",
}


class CoinglassClient:
    """Simple API client with retry logic."""

    def __init__(self, api_key: str, base_url: str = BASE_URL) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"accept": "application/json", "CG-API-KEY": api_key})

    def get(self, endpoint: str, params: dict) -> dict:
        url = self.base_url + endpoint
        for attempt in range(3):
            try:
                resp = self.session.get(url, params=params, timeout=10)
            except requests.RequestException as exc:  # network issue
                logging.warning("Network error: %s", exc)
                time.sleep(2)
                continue
            if resp.status_code != 200:
                logging.warning("HTTP %s: %s", resp.status_code, resp.text)
                time.sleep(1)
                continue
            try:
                data = resp.json()
            except ValueError:
                logging.warning("Invalid JSON from %s", endpoint)
                time.sleep(1)
                continue
            if data.get("code") != "0":
                raise RuntimeError(f"API error {data.get('code')}: {data.get('msg')}")
            return data.get("data", [])
        raise RuntimeError(f"Failed to fetch {endpoint}")

    def fetch_open_interest(self, symbol: str, interval: str = "4h") -> list[dict]:
        params = {"symbol": symbol, "interval": interval}
        logging.info("Fetching open interest for %s", symbol)
        return self.get(ENDPOINTS["open_interest"], params)

    def fetch_funding_rate(self, symbol: str, interval: str = "4h") -> list[dict]:
        params = {"symbol": symbol, "interval": interval}
        logging.info("Fetching funding rate for %s", symbol)
        return self.get(ENDPOINTS["funding_rate"], params)

    def fetch_long_short_ratio(
        self, symbol: str, exchange: str, interval: str = "4h"
    ) -> list[dict]:
        params = {"symbol": symbol, "exchangeName": exchange, "interval": interval}
        logging.info("Fetching long/short ratio for %s on %s", symbol, exchange)
        return self.get(ENDPOINTS["long_short_ratio"], params)

    def fetch_liquidations(self, symbol: str, interval: str = "4h") -> list[dict]:
        params = {"symbol": symbol, "interval": interval}
        logging.info("Fetching liquidations for %s", symbol)
        return self.get(ENDPOINTS["liquidations"], params)


class DataStorage:
    """Store data points in an SQLite database."""

    def __init__(self, db_file: str) -> None:
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS open_interest (
                symbol TEXT,
                time   INTEGER,
                open   REAL,
                high   REAL,
                low    REAL,
                close  REAL,
                PRIMARY KEY(symbol, time)
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS funding_rate (
                symbol TEXT,
                time   INTEGER,
                open   REAL,
                high   REAL,
                low    REAL,
                close  REAL,
                PRIMARY KEY(symbol, time)
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS long_short_ratio (
                symbol TEXT,
                exchange TEXT,
                time   INTEGER,
                long_percent  REAL,
                short_percent REAL,
                ratio REAL,
                PRIMARY KEY(symbol, exchange, time)
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS liquidations (
                symbol TEXT,
                time   INTEGER,
                long_liq  REAL,
                short_liq REAL,
                PRIMARY KEY(symbol, time)
            )
            """
        )
        self.conn.commit()

    def insert_open_interest(self, symbol: str, data: Iterable[dict]) -> None:
        rows = [
            (symbol, int(d["time"]), float(d["open"]), float(d["high"]), float(d["low"]), float(d["close"]))
            for d in data
        ]
        self.cur.executemany(
            "INSERT OR IGNORE INTO open_interest VALUES (?, ?, ?, ?, ?, ?)", rows
        )
        self.conn.commit()

    def insert_funding_rate(self, symbol: str, data: Iterable[dict]) -> None:
        rows = [
            (symbol, int(d["time"]), float(d["open"]), float(d["high"]), float(d["low"]), float(d["close"]))
            for d in data
        ]
        self.cur.executemany(
            "INSERT OR IGNORE INTO funding_rate VALUES (?, ?, ?, ?, ?, ?)", rows
        )
        self.conn.commit()

    def insert_long_short_ratio(self, symbol: str, exchange: str, data: Iterable[dict]) -> None:
        rows = [
            (
                symbol,
                exchange,
                int(d["time"]),
                float(d.get("top_account_long_percent", 0.0)),
                float(d.get("top_account_short_percent", 0.0)),
                float(d.get("top_account_long_short_ratio", 0.0)),
            )
            for d in data
        ]
        self.cur.executemany(
            "INSERT OR IGNORE INTO long_short_ratio VALUES (?, ?, ?, ?, ?, ?)", rows
        )
        self.conn.commit()

    def insert_liquidations(self, symbol: str, data: Iterable[dict]) -> None:
        rows = [
            (
                symbol,
                int(d["time"]),
                float(d["aggregated_long_liquidation_usd"]),
                float(d["aggregated_short_liquidation_usd"]),
            )
            for d in data
        ]
        self.cur.executemany(
            "INSERT OR IGNORE INTO liquidations VALUES (?, ?, ?, ?)", rows
        )
        self.conn.commit()

    def close(self) -> None:
        self.cur.close()
        self.conn.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download futures data from Coinglass into SQLite",
    )
    env_key = os.getenv("COINGLASS_API_KEY")
    parser.add_argument("--api-key", help="Coinglass API key")
    parser.add_argument("--symbols", default="BTC,ETH", help="Comma-separated list of symbols")
    parser.add_argument("--exchange", default="Binance", help="Exchange name for ratios")
    parser.add_argument("--interval", default="4h", help="Data interval (>=4h for Hobbyist)")
    parser.add_argument("--db-file", default="coinglass_data.db", help="SQLite database file")
    args = parser.parse_args()
    args.api_key = args.api_key or env_key
    if not args.api_key:
        parser.error("An API key is required. Use --api-key or set COINGLASS_API_KEY.")
    return args


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    client = CoinglassClient(args.api_key)
    storage = DataStorage(args.db_file)

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]

    for symbol in symbols:
        try:
            oi = client.fetch_open_interest(symbol, args.interval)
            storage.insert_open_interest(symbol, oi)

            fr = client.fetch_funding_rate(symbol, args.interval)
            storage.insert_funding_rate(symbol, fr)

            ls = client.fetch_long_short_ratio(symbol, args.exchange, args.interval)
            storage.insert_long_short_ratio(symbol, args.exchange, ls)

            liq = client.fetch_liquidations(symbol, args.interval)
            storage.insert_liquidations(symbol, liq)
        except Exception as exc:
            logging.error("Failed for %s: %s", symbol, exc)

    storage.close()
    logging.info("Pipeline completed")


if __name__ == "__main__":
    main()

