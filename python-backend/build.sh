#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install standard dependencies package
pip install -r requirements.txt

# 2. Install ONLY the browser binaries (no root privileges requested)
python -m playwright install chromium