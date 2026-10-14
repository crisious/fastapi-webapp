#!/usr/bin/env bash
# Dev server launcher.
#   ./run.sh            # default port 8000
#   PORT=9000 ./run.sh  # custom port
set -euo pipefail
cd "$(dirname "$0")"

PY=".venv/bin/python"
if [ ! -x "$PY" ]; then
  echo "No project venv found. Create one with:" >&2
  echo "  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 1
fi

exec "$PY" -m uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" --reload
