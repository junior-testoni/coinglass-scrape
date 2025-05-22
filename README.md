# Coinglass Data Scraper

This repository contains simple Python scripts for retrieving cryptocurrency market data from the public [Coinglass](https://coinglass.com/) API and saving it to CSV files.

## Prerequisites

All requests to the CoinGlass API require authentication using a unique, user-specific API Key.

Requests without a valid API Key or missing headers will be rejected with an authentication error.

✅ Example Usage

curl

curl -request GET
--url  '<https://open-api-v4.coinglass.com/api/futures/supported-coins>'
--header 'accept: application/json'\
--header 'CG-API-KEY: API\_KEY'

📦 Header Requirement

Every request must include the following HTTP header:

CG-API-KEY: your_api_key_here

If this header is missing or the API Key is invalid, the request will be denied with a 401 Unauthorized error.
Errors & Rate Limits
📡 API Response Status Codes

The CoinGlass API uses standard HTTP status codes to indicate the success or failure of your requests. Refer to the table below for a quick understanding of common response codes:

Status Code Description
0 Successful Request
400 Missing or invalid parameters
401 Invalid or missing API key
404 The requested resource does not exist
405 Unsupported HTTP method
408 The request took too long to complete
422 Parameters valid but not acceptable
429 Rate limit exceeded
500 An unexpected error occurred on the server

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

`fetch_hobbyist_endpoints.py` reads the list of URLs in `endpoints_merged.txt` (or
any file you provide with `--endpoints`) and saves the response from each one to
a file. By default the script tries to pick the best file type for each piece of
data (CSV for tables, text for plain messages). You can override this behaviour
with the `--format` option and choose `csv`, `json`, or `txt`.

```bash
python fetch_hobbyist_endpoints.py --api-key YOUR_KEY --output-dir data
```

The script creates the directory `data` if it does not already exist. Inside you
will find files in the chosen format (CSV, JSON, or plain text). If a request
fails, the corresponding file will contain the error message instead of data.

## Merging Endpoint Lists

If you have two different files of API URLs, such as `endpoints.txt` and
`endpoints2.txt`, you can combine them into a single file with the helper script
`merge_endpoints.py`:

```bash
python merge_endpoints.py --file1 endpoints.txt --file2 endpoints2.txt --output endpoints_merged.txt
```

This command produces `endpoints_merged.txt`. Use that file with
`fetch_hobbyist_endpoints.py` by adding the `--endpoints endpoints_merged.txt`
option.
