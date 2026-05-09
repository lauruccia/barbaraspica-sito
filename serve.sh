#!/usr/bin/env bash
# Anteprima locale del sito Barbara Spica
cd "$(dirname "$0")"
echo "→ http://localhost:8000"
if command -v php >/dev/null 2>&1; then
  php -S localhost:8000 -t .
elif command -v python3 >/dev/null 2>&1; then
  python3 -m http.server 8000
else
  echo "Installa PHP o Python per usare questo script"; exit 1
fi
