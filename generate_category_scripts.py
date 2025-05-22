import re
from pathlib import Path

ENDPOINT_FILE = "endpoints.txt"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def get_categories() -> set[str]:
    categories = set()
    with open(ENDPOINT_FILE) as f:
        next(f)
        for line in f:
            if not line.strip():
                continue
            try:
                _, url, _ = line.strip().split("\t")
            except ValueError:
                continue
            parts = url.split("/api/")
            cat = parts[1].split("/")[0] if len(parts) > 1 else "misc"
            categories.add(cat)
    return categories


def create_script(category: str) -> None:
    slug = slugify(category)
    path = Path(f"fetch_{slug}.py")
    path.write_text(
        "import sys\n"
        "import fetch_by_category\n\n"
        "if __name__ == \"__main__\":\n"
        "    if '--category' not in sys.argv:\n"
        f"        sys.argv += ['--category', '{category}']\n"
        "    fetch_by_category.main()\n"
    )
    print(f"Created {path}")


def main():
    for cat in sorted(get_categories()):
        create_script(cat)


if __name__ == "__main__":
    main()
