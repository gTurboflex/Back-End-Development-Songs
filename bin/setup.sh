#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 --version
python3 -m venv backend-songs-venv
backend-songs-venv/bin/python -m pip install --disable-pip-version-check -q -r requirements.txt
backend-songs-venv/bin/python -c 'import flask; print("Flask import: OK")'
echo "Environment Setup completed successfully: backend-songs-venv"
echo "Activate with: source backend-songs-venv/bin/activate"
