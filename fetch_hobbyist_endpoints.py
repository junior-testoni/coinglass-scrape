import argparse
import json
import os
import urllib.parse
import urllib.request

BASE_URL = "https://open-api-v4.coinglass.com"
DEFAULT_API_KEY = os.getenv("COINGLASS_API_KEY", "53b0a3236d8d4d2b9fff517c70c544ea")

# Endpoints that the Hobbyist plan can access
HOBBYIST_ENDPOINTS = {
    "spot_supported_coins": {"path": "/api/spot/supported-coins", "params": {}},
    "futures_supported_coins": {"path": "/api/futures/supported-coins", "params": {}},
    "option_max_pain": {"path": "/api/option/max-pain", "params": {"symbol": "BTC", "exchange": "Deribit"}},
    "exchange_assets": {"path": "/api/exchange/assets", "params": {"exchange": "Binance", "per_page": 10, "page": 1}},
    "bitcoin_etf_list": {"path": "/api/etf/bitcoin/list", "params": {}},
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
