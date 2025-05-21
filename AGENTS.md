# AGENT Instructions

These scripts retrieve data from the Coinglass public API. Ensure you have Python 3 installed and a valid API key.

1. **Provide your API key**
   - Every request must include the HTTP header `CG-API-KEY: <your key>`. Missing or invalid keys result in a 401 error.
   - Supply the key using `--api-key YOUR_KEY` or the `COINGLASS_API_KEY` environment variable.

2. **Run a script**
   - Example: `python coinglass_scraper.py --symbol BTC --output-dir data --api-key YOUR_KEY`
   - For open interest only: `python current_oi.py --symbol BTC --output current_oi.csv --api-key YOUR_KEY`

3. **Check results**
   - CSV files will appear in the specified directory.
