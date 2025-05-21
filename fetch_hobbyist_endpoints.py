"""Gather data from free Coinglass API endpoints.

This script queries several API endpoints that are available with the
free "Hobbyist" plan and stores all results in one JSON file.  Use it
to quickly get sample data without writing any Python code yourself.
"""

import argparse
import json
import os
import urllib.parse
import urllib.request

BASE_URL = "https://open-api-v4.coinglass.com"
# Default API key is read from the environment.  Replace the fallback
# value with your own key or pass ``--api-key`` on the command line.
DEFAULT_API_KEY = os.getenv("COINGLASS_API_KEY", "53b0a3236d8d4d2b9fff517c70c544ea")

# Endpoints that the Hobbyist plan can access
# A mapping of friendly names to endpoint information.  Each entry
# specifies the API path and default query parameters.  You can modify
# these parameters if you want different data.
HOBBYIST_ENDPOINTS = {
    # General reference data
    "spot_supported_coins": {"path": "/api/spot/supported-coins", "params": {}},
    "futures_supported_coins": {"path": "/api/futures/supported-coins", "params": {}},
    "bitcoin_etf_list": {"path": "/api/etf/bitcoin/list", "params": {}},

    # Example option/futures data
    "option_max_pain": {
        "path": "/api/option/max-pain",
        "params": {"symbol": "BTC", "exchange": "Deribit"},
    },
    "exchange_assets": {
        "path": "/api/exchange/assets",
        "params": {"exchange": "Binance", "per_page": 10, "page": 1},
    },

    # Historical price and indicator endpoints mentioned by the user
    "price_history": {
        "path": "/api/futures/price/history",
        "params": {"symbol": "BTC", "interval": "24h"},
    },
    "oi_aggregated_history": {
        "path": "/api/futures/open-interest/aggregated-history",
        "params": {"symbol": "BTC", "interval": "24h"},
    },
    "funding_rate_history": {
        "path": "/api/futures/funding-rate/history",
        "params": {"symbol": "BTC", "interval": "24h"},
    },
    "funding_rate_oi_weight": {
        "path": "/api/futures/funding-rate/oi-weight-history",
        "params": {"symbol": "BTC", "interval": "24h"},
    },
    "funding_rate_vol_weight": {
        "path": "/api/futures/funding-rate/vol-weight-history",
        "params": {"symbol": "BTC", "interval": "24h"},
    },
    "funding_rate_exchange_list": {
        "path": "/api/futures/funding-rate/exchange-list",
        "params": {"symbol": "BTC"},
    },
    "global_long_short_ratio_history": {
        "path": "/api/futures/global-long-short-account-ratio/history",
        "params": {"symbol": "BTC", "exchange": "Binance"},
    },
    "top_long_short_account_ratio_history": {
        "path": "/api/futures/top-long-short-account-ratio/history",
        "params": {"symbol": "BTC", "exchange": "Binance"},
    },
    "top_long_short_position_ratio_history": {
        "path": "/api/futures/top-long-short-position-ratio/history",
        "params": {"symbol": "BTC", "exchange": "Binance"},
    },
    "taker_buy_sell_volume": {
        "path": "/api/futures/taker-buy-sell-volume/exchange-list",
        "params": {"symbol": "BTC"},
    },
    "liquidation_history": {
        "path": "/api/futures/liquidation/history",
        "params": {"symbol": "BTC", "interval": "24h"},
    },
}

def fetch(endpoint: str, params: dict, api_key: str) -> dict:
    """Fetch JSON data from the given Coinglass endpoint."""
    url = urllib.parse.urljoin(BASE_URL, endpoint)
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("CG-API-KEY", api_key)
    with urllib.request.urlopen(req) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Request failed: {resp.status}")
        return json.loads(resp.read().decode())

def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch data from Hobbyist-accessible Coinglass endpoints")
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="Your Coinglass API key")
    parser.add_argument("--output", default="hobbyist_data.json", help="File to store combined JSON output")
    args = parser.parse_args()

    results = {}
    for name, meta in HOBBYIST_ENDPOINTS.items():
        try:
            data = fetch(meta["path"], meta["params"], args.api_key)
            results[name] = data
            print(f"Fetched {name}")
        except Exception as exc:
            print(f"Failed to fetch {name}: {exc}")
            results[name] = {"error": str(exc)}

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved data to {args.output}")

if __name__ == "__main__":
    main()
