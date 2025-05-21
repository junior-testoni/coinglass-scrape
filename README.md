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

Use `fetch_hobbyist_endpoints.py` to retrieve data from every Coinglass endpoint that the free Hobbyist plan can access. The script combines the responses and stores them in a single JSON file.

```bash
python fetch_hobbyist_endpoints.py --api-key YOUR_KEY --output hobbyist_data.json
```

`hobbyist_data.json` will contain one JSON object with entries for each endpoint. Any errors are reported in the file as well.
