"""Simple scraper for Coinglass public API.

This script demonstrates how to retrieve a few example indicators from the
Coinglass open API and write them to CSV files. The endpoints and field
names used here are based on public documentation and may require
adjustments if Coinglass changes their API.

A Coinglass API key can be provided via the ``--api-key`` option if
the endpoint requires authentication.
"""

import argparse
import csv
import json
import os
import urllib.parse
import urllib.request


# Default base URL for the Coinglass open API v4
BASE_URL = "https://open-api-v4.coinglass.com"

# Example endpoints. Additional endpoints can be added to this mapping.
# Each entry contains the endpoint path and a list of required parameters.
ENDPOINTS = {
    "fear_and_greed_history": {"path": "/api/pro/dashboard/bitcoin", "params": []},
    # Funding rates typically require a symbol parameter
    "funding_rates": {"path": "/api/options/OptionGreeks", "params": ["symbol"]},
    # Open interest history also expects a symbol
    "open_interest_history": {"path": "/api/futures/open_interest_history", "params": ["symbol"]},
    # Options max pain requires both symbol and exchange
    "option_max_pain": {"path": "/api/option/max-pain", "params": ["symbol", "exchange"]},
}


def fetch(endpoint: str, params: dict | None = None, api_key: str | None = None) -> dict:
    """Fetch JSON data from the given Coinglass endpoint."""
    url = urllib.parse.urljoin(BASE_URL, endpoint)
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    if api_key:
        # According to the CoinGlass documentation, requests must include the
        # "CG-API-KEY" header for authentication. The old header name
        # "coinglassSecret" no longer works.
        req.add_header("CG-API-KEY", api_key)

    with urllib.request.urlopen(req) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Request failed: {resp.status}")
        return json.loads(resp.read().decode())


def save_list_of_dicts(items: list[dict], filepath: str) -> None:
    """Write a list of dictionaries to ``filepath`` as CSV."""
    if not items:
        return
    fieldnames = list(items[0].keys())
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape data from Coinglass and store as CSV files")
    env_key = os.getenv("COINGLASS_API_KEY")
    parser.add_argument("--api-key", help="Coinglass API key")
    parser.add_argument("--exchange", help="Exchange for option data", default="Deribit")
    parser.add_argument("--symbol", help="Symbol to query (e.g. BTC)", default="BTC")
    parser.add_argument("--output-dir", help="Directory to store CSV files", default="data")
    args = parser.parse_args()

    api_key = args.api_key or env_key
    if not api_key:
        parser.error("An API key is required. Use --api-key or set COINGLASS_API_KEY.")

    os.makedirs(args.output_dir, exist_ok=True)

    for name, meta in ENDPOINTS.items():
        endpoint = meta["path"]
        params = {p: getattr(args, p) for p in meta.get("params", [])}
        try:
            data = fetch(endpoint, params=params, api_key=api_key)
            if isinstance(data, dict):
                content = data.get("data") or data
            else:
                content = data
            if isinstance(content, list):
                save_list_of_dicts(content, os.path.join(args.output_dir, f"{name}.csv"))
                print(f"Saved {name} data to {name}.csv")
            else:
                print(f"Unexpected format for {name}: {content}")
        except Exception as exc:
            print(f"Failed to fetch {name}: {exc}")


if __name__ == "__main__":
    main()
