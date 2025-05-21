import argparse
import csv
import json
import os
import urllib.parse
import urllib.request

DEFAULT_API_KEY = os.getenv("COINGLASS_API_KEY", "53b0a3236d8d4d2b9fff517c70c544ea")
BASE_URL = "https://open-api-v4.coinglass.com"


def fetch(endpoint: str, params=None, api_key=None) -> dict:
    url = urllib.parse.urljoin(BASE_URL, endpoint)
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    if api_key:
        req.add_header("coinglassSecret", api_key)
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
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="Coinglass API key if required")
    parser.add_argument("--symbol", default="BTC", help="Trading symbol, e.g. BTC")
    parser.add_argument("--output", default="current_oi.csv", help="Output CSV file")
    args = parser.parse_args()

    data = fetch("/api/futures/open_interest", {"symbol": args.symbol}, api_key=args.api_key)
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
