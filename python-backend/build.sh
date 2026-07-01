#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Standard python packages setup
pip install -r requirements.txt

# 2. Invoke Playwright via the dynamic python context
python -m playwright install chromium