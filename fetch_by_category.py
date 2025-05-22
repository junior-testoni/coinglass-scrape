import argparse
import json
import os
import requests
from pathlib import Path
import re

DEFAULT_API_KEY = os.getenv("COINGLASS_API_KEY", "53b0a3236d8d4d2b9fff517c70c544ea")
ENDPOINT_FILE = "endpoints.txt"


def fetch(url: str, api_key: str) -> dict:
    """Fetch JSON data from the given URL."""
    headers = {"CG-API-KEY": api_key}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"Request failed: {resp.status_code}")
    return resp.json()


def load_endpoints(file_path: str):
    """Yield (title, url, category) tuples from the endpoint file."""
    with open(file_path, "r") as f:
        next(f)  # skip header
        for line in f:
            if not line.strip():
                continue
            title, url, _ = line.strip().split("\t")
            # Category inferred from URL path e.g. /api/futures/...
            # Taking the part after '/api/'
            parts = url.split("/api/")
            category = parts[1].split("/")[0] if len(parts) > 1 else "misc"
            yield title, url, category


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def save_json(data: dict, base_path: Path) -> None:
    out_file = base_path.with_suffix(".json")
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch Coinglass endpoints for a specific category"
    )
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="Your Coinglass API key")
    parser.add_argument("--output-dir", default="category_output", help="Directory to store results")
    parser.add_argument("--endpoints", default=ENDPOINT_FILE, help="Path to endpoints list")
    parser.add_argument("--category", required=True, help="Category to fetch (e.g. futures, spot)")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for title, url, cat in load_endpoints(args.endpoints):
        if cat != args.category:
            continue
        file_base = out_dir / slugify(title)
        try:
            data = fetch(url, args.api_key)
            save_json(data, file_base)
            print(f"Fetched {title}")
        except Exception as exc:
            with open(file_base.with_suffix(".txt"), "w") as f:
                f.write(str(exc))
            print(f"Failed to fetch {title}: {exc}")


if __name__ == "__main__":
    main()
