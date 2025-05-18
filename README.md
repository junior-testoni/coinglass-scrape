# fgfgfgfgfgfg

This repository demonstrates a simple script for retrieving data from the
[Coinglass](https://coinglass.com/) public API and storing the results in
CSV files.

## Usage

Run `coinglass_scraper.py` to fetch a few example indicators (fear and
greed history, funding rates, and open interest history). A Coinglass API
key can be supplied via the `--api-key` option if the API endpoint
requires authentication.

```bash
python coinglass_scraper.py --symbol BTC --output-dir data
```

Each indicator is saved as a separate CSV file inside the specified
output directory.
