import sys
import fetch_by_category

if __name__ == "__main__":
    if '--category' not in sys.argv:
        sys.argv += ['--category', 'bitfinex-margin-long-short']
    fetch_by_category.main()
