import argparse
import csv
import json
import os
import requests
from pathlib import Path
import re

DEFAULT_API_KEY = os.getenv("COINGLASS_API_KEY", "53b0a3236d8d4d2b9fff517c70c544ea")

# Default list of public endpoints to fetch. Update this path if you
# maintain your own file of URLs.
ENDPOINT_FILE = "endpoints.txt"

def fetch(url: str, api_key: str) -> dict:
    """Fetch JSON data from the given URL."""
    headers = {"CG-API-KEY": api_key}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"Request failed: {resp.status_code}")
    return resp.json()


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


def save_response(data: dict | list, base_path: Path, fmt: str = "best") -> None:
    """Save the response data to ``base_path`` using the chosen format."""

    # Many Coinglass responses wrap the actual content in a ``data`` field.
    if isinstance(data, dict) and "data" in data:
        content = data["data"]
    else:
        content = data

    # Explicit JSON dump
    if fmt == "json":
        out_file = base_path.with_suffix(".json")
        with open(out_file, "w") as f:
            json.dump(data, f, indent=2)
        return

    # Explicit text dump
    if fmt == "txt":
        out_file = base_path.with_suffix(".txt")
        with open(out_file, "w") as f:
            if isinstance(data, (dict, list)):
                json.dump(data, f, indent=2)
            else:
                f.write(str(data))
        return

    # CSV requested or best-effort when fmt == "best"
    if isinstance(content, list) and content and isinstance(content[0], dict):
        out_file = base_path.with_suffix(".csv")
        with open(out_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=content[0].keys())
            writer.writeheader()
            writer.writerows(content)
        return
    if isinstance(content, dict):
        out_file = base_path.with_suffix(".csv")
        with open(out_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=content.keys())
            writer.writeheader()
            writer.writerow(content)
        return

    # If CSV conversion failed or fmt was not 'csv', fall back to text
    out_file = base_path.with_suffix(".txt")
    with open(out_file, "w") as f:
        if isinstance(content, (dict, list)):
            json.dump(content, f, indent=2)
        else:
            f.write(str(content))

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
        help="Directory to store downloaded files",
    )
    parser.add_argument(
        "--endpoints",
        default=ENDPOINT_FILE,
        help="Path to the file containing endpoint URLs",
    )
    parser.add_argument(
        "--format",
        choices=["best", "csv", "json", "txt"],
        default="best",
        help="Force a particular output format or use 'best' to auto-detect",
    )

    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for title, url in load_endpoints(args.endpoints):
        file_base = out_dir / slugify(title)
        try:
            data = fetch(url, args.api_key)
            save_response(data, file_base, args.format)
            print(f"Fetched {title}")
        except Exception as exc:
            err_path = file_base.with_suffix(".txt")
            with open(err_path, "w") as f:
                f.write(str(exc))
            print(f"Failed to fetch {title}: {exc}")

    print(f"Saved endpoint data to {out_dir}/")

if __name__ == "__main__":
    main()
