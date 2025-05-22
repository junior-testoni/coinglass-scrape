import argparse
from collections import OrderedDict
from pathlib import Path


def read_lines(path):
    lines = []
    with open(path, 'r') as f:
        for line in f:
            stripped = line.rstrip('\n')
            if stripped:
                lines.append(stripped)
    return lines


def merge_files(file1, file2):
    seen = OrderedDict()
    for path in [file1, file2]:
        for line in read_lines(path):
            if line not in seen:
                seen[line] = None
    return list(seen.keys())


def main():
    parser = argparse.ArgumentParser(description="Merge two files containing API endpoints into one without duplicates.")
    parser.add_argument('--file1', required=True, help='First endpoints file')
    parser.add_argument('--file2', required=True, help='Second endpoints file')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    merged = merge_files(args.file1, args.file2)

    output_path = Path(args.output)
    output_path.write_text('\n'.join(merged) + '\n')
    print(f"Merged {len(merged)} endpoints into {output_path}")


if __name__ == '__main__':
    main()
