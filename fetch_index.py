import sys
import fetch_by_category

if __name__ == "__main__":
    if '--category' not in sys.argv:
        sys.argv += ['--category', 'index']
    fetch_by_category.main()
