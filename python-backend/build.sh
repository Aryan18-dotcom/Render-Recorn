#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install standard dependencies package
pip install -r requirements.txt

# 2. Install all browser types explicitly (including headless variants)
playwright install --with-deps