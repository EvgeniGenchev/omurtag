#!/usr/bin/env sh
cd "$(dirname "$0")"
python3 -m http.server "${1:-8080}"
