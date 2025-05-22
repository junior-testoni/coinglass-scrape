#!/usr/bin/env bash
# Simple script to set up a Python virtual environment
# and install the required packages.

set -e

PYTHON=${PYTHON:-python3}

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "Python 3 is required but was not found. Please install Python 3." >&2
    exit 1
fi

# Create virtual environment in ./venv if it doesn't exist
if [ ! -d "venv" ]; then
    "$PYTHON" -m venv venv
fi

# Activate the environment
. venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "\nSetup complete. Activate the environment with: source venv/bin/activate"
