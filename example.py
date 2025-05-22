# get supported coins
import requests
import os

url = "https://open-api-v4.coinglass.com/api/futures/supported-coins"

api_key = os.getenv("COINGLASS_API_KEY")
if not api_key:
    raise SystemExit("Please set the COINGLASS_API_KEY environment variable")

headers = {
    "accept": "application/json",
    "CG-API-KEY": api_key,
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Request failed: {response.status_code}")
else:
    print(response.text)
