# AGENT Instructions

These instructions outline how the agent should scrape data from the Coinglass public API using the existing `coinglass_scraper.py` script in this repository.

1. **Verify required files**
   
   - Ensure `coinglass_scraper.py` exists in the repository root. This script contains the logic for contacting the Coinglass API.

2. **Check for Python availability**
   - Confirm that Python 3 is installed by running `python --version`.

3. **read documentation**
   - doc.csv has information on how to use api 

   - Run `python coinglass_scraper.py --help` to view available arguments.

4. **Prepare parameters**
   - Choose a symbol to query (e.g. `BTC`).
   - If the API requires authentication, provide the API key via `--api-key YOUR_KEY`.
   - Decide where to store the resulting CSV files (default is `data`).

5. **Run the scraper**
   ```bash
   python coinglass_scraper.py --symbol BTC --output-dir data
   ```
   - Include `--api-key` if necessary.

6. **Verify results**
   - After execution, check the specified output directory for CSV files (e.g. `fear_and_greed_history.csv`, `funding_rates.csv`, `open_interest_history.csv`).
   - Ensure each CSV file contains data.
   -start over untill it works 

Follow these steps whenever the goal is to scrape data from Coinglass.
