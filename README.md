# Coinglass Data Scraper

This repository contains simple Python scripts for retrieving cryptocurrency market data from the public [Coinglass](https://coinglass.com/) API and saving it to CSV files.

## Prerequisites

- Python 3
- A valid Coinglass API key

The Coinglass documentation states that every request must include the `CG-API-KEY` header. Requests without this header will be rejected with a 401 Unauthorized error.

Generate your key from your API Key Dashboard and supply it via the `--api-key` option or the `COINGLASS_API_KEY` environment variable when running the scripts.

## Example Usage

Fetch several indicators for Bitcoin and store them in the `data` directory:

```bash
python coinglass_scraper.py --symbol BTC --output-dir data --api-key YOUR_KEY
```

For current open interest only, run:

```bash
python current_oi.py --symbol BTC --output current_oi.csv --api-key YOUR_KEY
```

Each script writes one or more CSV files containing the returned data.

## Fetching All Hobbyist Endpoints

Use `fetch_hobbyist_endpoints.py` to gather data from several endpoints that are available with the free Hobbyist plan. The script sends a request to each endpoint and saves all of the responses together in one JSON file.

```bash
python fetch_hobbyist_endpoints.py --api-key YOUR_KEY --output hobbyist_data.json
```

The resulting `hobbyist_data.json` file will contain one entry for each endpoint. If a request fails, that entry will store an error message instead of data. Open the file with a text editor to view the raw JSON.

The script queries these endpoints by default (for the `BTC` symbol):

- `/api/futures/price/history`
- `/api/futures/open-interest/aggregated-history`
- `/api/futures/funding-rate/history`
- `/api/futures/funding-rate/oi-weight-history`
- `/api/futures/funding-rate/vol-weight-history`
- `/api/futures/funding-rate/exchange-list`
- `/api/futures/global-long-short-account-ratio/history`
- `/api/futures/top-long-short-account-ratio/history`
- `/api/futures/top-long-short-position-ratio/history`
- `/api/futures/taker-buy-sell-volume/exchange-list`
- `/api/futures/liquidation/history`
