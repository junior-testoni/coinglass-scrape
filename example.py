# get supported coins
import os
from api_utils import fetch

url = "/api/futures/supported-coins"

api_key = os.getenv("COINGLASS_API_KEY")
if not api_key:
    raise SystemExit("Please set the COINGLASS_API_KEY environment variable")

data = fetch(url, api_key=api_key)
print(data)
