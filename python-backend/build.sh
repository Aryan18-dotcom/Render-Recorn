#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Ensure the browser path is consistent
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/src/.local-browsers

# 2. Install Python packages
pip install -r requirements.txt

# 3. Install Chromium and its Linux system libraries
python -m playwright install --with-deps chromium