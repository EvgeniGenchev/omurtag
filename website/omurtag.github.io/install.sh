#!/bin/sh
set -e

REPO="https://github.com/EvgeniGenchev/omurtag.git"
TMP="$(mktemp -d)"

echo "Cloning omurtag..."
git clone --depth 1 "$REPO" "$TMP/omurtag"

echo "Installing..."
if command -v uv >/dev/null 2>&1; then
    uv tool install "$TMP/omurtag"
elif command -v pip >/dev/null 2>&1; then
    pip install --user "$TMP/omurtag"
else
    echo "error: neither uv nor pip found." >&2
    echo "  install uv: curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    rm -rf "$TMP"
    exit 1
fi

rm -rf "$TMP"
echo "Done. Run: omurtag --help"
