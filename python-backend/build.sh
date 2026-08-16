#!/usr/bin/env bash
set -o errexit

export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/src/.local-browsers

pip install -r requirements.txt
python -m playwright install chromium