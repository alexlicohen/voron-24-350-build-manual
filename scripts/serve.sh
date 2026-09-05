#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -x .venv/bin/mkdocs ]; then
  MKDOCS=.venv/bin/mkdocs
else
  MKDOCS=mkdocs
fi

HOST_LOCAL="$(scutil --get LocalHostName 2>/dev/null || echo localhost).local"
IP="$(ipconfig getifaddr en0 2>/dev/null || echo unknown)"

echo "LAN URLs (open on the iPad, same Wi-Fi):"
echo "  http://${HOST_LOCAL}:8000"
echo "  http://${IP}:8000"
echo

exec "$MKDOCS" serve -a 0.0.0.0:8000 --livereload
