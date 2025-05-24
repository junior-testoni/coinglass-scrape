# Coinglass Data Scraper

This repository contains simple Python scripts for retrieving cryptocurrency market data from the public [Coinglass](https://coinglass.com/) API and saving it to CSV files.

## Prerequisites

All requests to the CoinGlass API require authentication using a unique, user-specific API Key.

Requests without a valid API Key or missing headers will be rejected with an authentication error.

## Installation

Before running any of the scripts you will need Python 3 and the `pip` package manager.
If `pip` does not seem to work, try calling it through Python directly:

```bash
python3 -m pip --version
```

To set up everything automatically you can run the helper script `setup_env.sh` which creates a virtual environment and installs the requirements:

```bash
bash setup_env.sh
```

If you prefer to do it manually, open a terminal in this project folder and run:

```bash
pip install -r requirements.txt
```

This command downloads the dependencies used in the example scripts.

All Python files rely on a small helper in `api_utils.py` which sends the
authenticated HTTP requests. You don't need to edit this file—just keep it in
the same folder as the other scripts.

## Setting Your API Key

1. Copy the file `config.env` and open it in a text editor.
2. Replace `YOUR_API_KEY` with the key you received from Coinglass.
3. In the terminal run `source config.env` to load the variable.

Alternatively you can supply the key when running a script using the `--api-key` option.

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
source config.env  # sets COINGLASS_API_KEY
python coinglass_scraper.py --symbol BTC --output-dir data
```

For current open interest only, run:

```bash
source config.env
python current_oi.py --symbol BTC --output current_oi.csv
```

Each script writes one or more CSV files containing the returned data.

## Fetching All Hobbyist Endpoints

`fetch_hobbyist_endpoints.py` reads the list of URLs in `endpoints_merged.txt` (or
any file you provide with `--endpoints`) and saves the response from each one to
a file. By default the script tries to pick the best file type for each piece of
data (CSV for tables, text for plain messages). You can override this behaviour
with the `--format` option and choose `csv`, `json`, or `txt`.

```bash
source config.env
python fetch_hobbyist_endpoints.py --output-dir data
```

The script creates the directory `data` if it does not already exist. Inside you
will find files in the chosen format (CSV, JSON, or plain text). If a request
fails, the corresponding file will contain the error message instead of data.

## Fetching Endpoints by Category

For convenience there is a ready-made script for every API category. Each file
is named `fetch_<category>.py` where `<category>` matches the part after
`/api/` in the URLs from `endpoints.txt`. For example, to download all endpoints
under the `futures` category run:

```bash
source config.env
python fetch_futures.py --output-dir my_data
```

The script automatically sets the category for you, so the only options you need
are the API key and an output directory. Similar files exist for other
categories such as `spot`, `etf`, and `exchange`. Check the repository for the
available `fetch_*.py` scripts. Internally these wrappers call
`fetch_by_category.py`.

If the list of endpoints changes, run `python generate_category_scripts.py` to
recreate the wrapper files.

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

## Simplified Collector Script

If you prefer a single command that downloads everything with safe rate limiting, run `coinglass_collector.py`. The script reads the list of URLs in `endpoints.txt` and saves each response into a subfolder named after the API category.

```bash
source config.env  # loads COINGLASS_API_KEY
python coinglass_collector.py --output-dir my_data
```

It waits about three seconds between requests so that no more than 20 requests are made per minute.


## SQLite Data Pipeline

`coinglass_pipeline.py` downloads several futures statistics for a set
of symbols and keeps them in a small SQLite database. This is useful if
you want to query the data later without saving multiple CSV files.

Run the script after setting your API key:

```bash
source config.env  # sets COINGLASS_API_KEY
python coinglass_pipeline.py --symbols BTC,ETH --db-file my_data.db
```

The database will contain tables for open interest, funding rates,
long/short ratios and liquidations. Re-running the command adds any new
records without duplicating existing ones.

