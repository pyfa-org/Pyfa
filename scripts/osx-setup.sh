#!/usr/bin/env bash
set -euo pipefail
echo "Syncing locked dependencies..."
uv sync --frozen --no-dev --group packaging
echo "Python version:"
uv run python --version
