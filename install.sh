#!/bin/sh
set -e

if command -v uv >/dev/null 2>&1; then
    uv tool install --upgrade omurtag
elif command -v pip >/dev/null 2>&1; then
    pip install --user --upgrade omurtag
else
    echo "error: neither uv nor pip found. Install one first:" >&2
    echo "  uv:  curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    echo "  pip: https://pip.pypa.io/en/stable/installation/" >&2
    exit 1
fi
