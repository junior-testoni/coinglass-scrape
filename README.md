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

`fetch_hobbyist_endpoints.py` reads the list of URLs in `endpoints.txt` and saves the
response from each one to its own JSON file. This script is aimed at people who
are not comfortable with coding. Simply run the command below and look in the
output folder for the results.

```bash
python fetch_hobbyist_endpoints.py --api-key YOUR_KEY --output-dir data
```

The script creates the directory `data` if it does not already exist. Inside you
will find a JSON file for every endpoint listed in `endpoints.txt`. If a request
fails, the corresponding file will contain an error message instead of data.

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
