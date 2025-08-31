#!/usr/bin/env bash
set -euo pipefail

# Source project-local virtualenv if present
if [[ -d ".venv" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

python -m tests.simple_agent "$@"


