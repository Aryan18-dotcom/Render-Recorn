#!/usr/bin/env bash
# exit on error
set -o errexit

# Install standard python dependencies
pip install -r requirements.txt

# Crucial step: Install Playwright and its native Linux system dependencies
playwright install chromium