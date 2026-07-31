#!/usr/bin/env bash
set -euo pipefail
echo "Syncing locked dependencies..."
uv sync --frozen --no-default-groups --group packaging --group wx-binary
echo "Python version:"
uv run --no-sync python --version
