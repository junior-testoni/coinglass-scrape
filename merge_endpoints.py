import argparse
import csv


def read_endpoints1(path):
    """Read tab-separated endpoints file with header."""
    entries = []
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)  # skip header
        for row in reader:
            if len(row) >= 3:
                title, link, desc = row[0], row[1], row[2]
                entries.append((title.strip(), link.strip(), desc.strip()))
    return entries


def read_endpoints2(path):
    """Read endpoints2 format: title, url, description repeated."""
    entries = []
    with open(path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]
    i = 0
    while i + 2 < len(lines):
        title = lines[i]
        url = lines[i + 1]
        desc = lines[i + 2]
        if not url.startswith("http"):
            i += 1
            continue
        if title.lower().startswith("version"):
            break
        if title == "Getting Started":
            break
        entries.append((title, url, desc))
        i += 3
    return entries


def merge_lists(list1, list2):
    merged = {}
    for title, link, desc in list1 + list2:
        if link not in merged:
            merged[link] = (title, link, desc)
    return list(merged.values())


def write_endpoints(path, entries):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["title", "link", "description"])
        for title, link, desc in entries:
            writer.writerow([title, link, desc])


def main():
    parser = argparse.ArgumentParser(description="Merge endpoint lists")
    parser.add_argument("--file1", default="endpoints.txt", help="First endpoints file")
    parser.add_argument("--file2", default="endpoints2.txt", help="Second endpoints file")
    parser.add_argument("--output", default="endpoints_merged.txt", help="Output file")
    args = parser.parse_args()

    list1 = read_endpoints1(args.file1)
    list2 = read_endpoints2(args.file2)
    merged = merge_lists(list1, list2)
    write_endpoints(args.output, merged)
    print(f"Merged {len(merged)} endpoints into {args.output}")


if __name__ == "__main__":
    main()
