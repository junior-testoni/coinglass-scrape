import argparse
import csv
import json
import os
import urllib.parse
import urllib.request
BASE_URL = "https://open-api-v4.coinglass.com"


def fetch(endpoint: str, params=None, api_key=None) -> dict:
    url = urllib.parse.urljoin(BASE_URL, endpoint)
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    if api_key:
        # Updated header name per official CoinGlass API documentation.
        req.add_header("CG-API-KEY", api_key)
    with urllib.request.urlopen(req) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Request failed: {resp.status}")
        return json.loads(resp.read().decode())


def save_dict(data: dict, filepath: str) -> None:
    if not data:
        return
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch current open interest from Coinglass")
    env_key = os.getenv("COINGLASS_API_KEY")
    parser.add_argument("--api-key", help="Coinglass API key")
    parser.add_argument("--symbol", default="BTC", help="Trading symbol, e.g. BTC")
    parser.add_argument("--output", default="current_oi.csv", help="Output CSV file")
    args = parser.parse_args()

    api_key = args.api_key or env_key
    if not api_key:
        parser.error("An API key is required. Use --api-key or set COINGLASS_API_KEY.")

    data = fetch("/api/futures/open_interest", {"symbol": args.symbol}, api_key=api_key)
    content = data.get("data") if isinstance(data, dict) else data
    if isinstance(content, list):
        if content:
            content = content[0]
        else:
            content = {}
    save_dict(content, args.output)
    print(f"Saved current open interest to {args.output}")


if __name__ == "__main__":
    main()
