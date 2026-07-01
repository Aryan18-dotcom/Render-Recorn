#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Standard python packages setup
pip install -r requirements.txt

# 2. Install full browser suite (includes the required chrome-headless-shell)
python -m playwright install