import argparse
import json
import os
import urllib.request
from pathlib import Path
import re

DEFAULT_API_KEY = os.getenv("COINGLASS_API_KEY", "53b0a3236d8d4d2b9fff517c70c544ea")

ENDPOINT_FILE = "endpoints.txt"

def fetch(url: str, api_key: str) -> dict:
    """Fetch JSON data from the given URL."""
    req = urllib.request.Request(url)
    req.add_header("CG-API-KEY", api_key)
    with urllib.request.urlopen(req) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Request failed: {resp.status}")
        return json.loads(resp.read().decode())


def load_endpoints(file_path: str):
    """Yield (title, url) tuples from a tab-separated endpoint file."""
    with open(file_path, "r") as f:
        next(f)  # skip header
        for line in f:
            if not line.strip():
                continue
            title, url, _ = line.strip().split("\t")
            yield title, url


def slugify(text: str) -> str:
    """Convert title to a safe file name."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch data from Hobbyist-accessible Coinglass endpoints"
    )
    parser.add_argument(
        "--api-key",
        default=DEFAULT_API_KEY,
        help="Your Coinglass API key",
    )
    parser.add_argument(
        "--output-dir",
        default="hobbyist_output",
        help="Directory to store JSON files",
    )
    parser.add_argument(
        "--endpoints",
        default=ENDPOINT_FILE,
        help="Path to endpoints.txt",
    )

    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for title, url in load_endpoints(args.endpoints):
        file_name = slugify(title) + ".json"
        path = out_dir / file_name
        try:
            data = fetch(url, args.api_key)
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Fetched {title}")
        except Exception as exc:
            with open(path, "w") as f:
                json.dump({"error": str(exc)}, f, indent=2)
            print(f"Failed to fetch {title}: {exc}")

    print(f"Saved endpoint data to {out_dir}/")

if __name__ == "__main__":
    main()
