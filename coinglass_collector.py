import argparse
import csv
import json
import os
import re
import time
from pathlib import Path

from api_utils import fetch

# How long to wait between requests (seconds) to stay under 20 req/min
REQUEST_DELAY = 3.1


def load_endpoints(file_path: str):
    """Yield (title, url, category) tuples from a tab-separated endpoint file."""
    with open(file_path, "r") as f:
        next(f)  # skip header
        for line in f:
            if not line.strip():
                continue
            title, url, _ = line.strip().split("\t")
            # category is the first segment after '/api/'
            parts = url.split("/api/")
            category = parts[1].split("/")[0] if len(parts) > 1 else "misc"
            yield title, url, category


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def save_response(data, base_path: Path) -> None:
    """Save data to CSV if possible, otherwise JSON."""
    if isinstance(data, dict) and "data" in data:
        content = data["data"]
    else:
        content = data

    if isinstance(content, list) and content and isinstance(content[0], dict):
        out_file = base_path.with_suffix(".csv")
        with open(out_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=content[0].keys())
            writer.writeheader()
            writer.writerows(content)
    else:
        out_file = base_path.with_suffix(".json")
        with open(out_file, "w") as f:
            json.dump(content, f, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download multiple Coinglass endpoints with rate limiting",
        epilog="Provide your API key via --api-key or COINGLASS_API_KEY env var",
    )
    env_key = os.getenv("COINGLASS_API_KEY")
    parser.add_argument("--api-key", help="Coinglass API key")
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Directory to store the downloaded files",
    )
    parser.add_argument(
        "--endpoints",
        default="endpoints.txt",
        help="Path to the file listing endpoints",
    )

    args = parser.parse_args()
    api_key = args.api_key or env_key
    if not api_key:
        parser.error("An API key is required. Use --api-key or set COINGLASS_API_KEY.")

    base_dir = Path(args.output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    for title, url, category in load_endpoints(args.endpoints):
        cat_dir = base_dir / category
        cat_dir.mkdir(parents=True, exist_ok=True)
        file_base = cat_dir / slugify(title)
        try:
            data = fetch(url, api_key=api_key)
            save_response(data, file_base)
            print(f"Fetched {title}")
        except Exception as exc:
            with open(file_base.with_suffix(".txt"), "w") as f:
                f.write(str(exc))
            print(f"Failed to fetch {title}: {exc}")

        # wait to respect rate limit
        time.sleep(REQUEST_DELAY)

    print(f"Saved data to {base_dir}/")


if __name__ == "__main__":
    main()
