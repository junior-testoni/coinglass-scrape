import urllib.parse
import requests

BASE_URL = "https://open-api-v4.coinglass.com"


def fetch(endpoint: str, params: dict | None = None, api_key: str | None = None) -> dict:
    """Return JSON data from the given Coinglass endpoint."""
    url = urllib.parse.urljoin(BASE_URL, endpoint)
    headers = {}
    if api_key:
        headers["CG-API-KEY"] = api_key
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 401:
        raise RuntimeError("Unauthorized. Check your API key.")
    if resp.status_code == 429:
        raise RuntimeError("Rate limit exceeded. Try again later.")
    if resp.status_code != 200:
        raise RuntimeError(f"Request failed: {resp.status_code}")
    return resp.json()
