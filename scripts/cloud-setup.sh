#!/usr/bin/env bash
# Setup script for the Claude Code cloud environment (paste into the environment's setup script).
# Installs what the agents need to build and test. No secrets here.
set -euo pipefail

python3 -m pip install --upgrade pip
if [ -f requirements.txt ]; then python3 -m pip install -r requirements.txt; fi
python3 -m pip install pytest pre-commit

if [ -f package.json ]; then npm ci; fi

if [ -f .pre-commit-config.yaml ]; then pre-commit install || true; fi

echo "Cloud environment ready."
