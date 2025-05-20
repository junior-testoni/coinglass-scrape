# fgfgfgfgfgfg

This repository demonstrates a simple script for retrieving data from the
[Coinglass](https://coinglass.com/) public API and storing the results in
CSV files.

## Usage

Run `coinglass_scraper.py` to fetch a few example indicators (fear and
greed history, funding rates, open interest history, and option max pain).
A default API key is included in the script for convenience. You can
override it via the `--api-key` option or the `COINGLASS_API_KEY`
environment variable if you prefer to supply your own key.

```bash
python coinglass_scraper.py --symbol BTC --output-dir data
```

Include the `--exchange` option when retrieving option data (defaults to
`Deribit`):

```bash
python coinglass_scraper.py --symbol BTC --exchange Deribit --output-dir data
```

Each indicator is saved as a separate CSV file inside the specified
output directory.
