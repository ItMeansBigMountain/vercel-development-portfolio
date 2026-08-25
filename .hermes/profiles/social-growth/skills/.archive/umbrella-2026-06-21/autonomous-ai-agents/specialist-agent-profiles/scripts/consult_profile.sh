#!/usr/bin/env bash
# Query a named Hermes specialist profile from another script/session.
# Usage: consult_profile.sh <profile> "prompt"
set -euo pipefail
PROFILE="${1:-}"
shift || true
PROMPT="${*:-}"
if [[ -z "$PROFILE" || -z "$PROMPT" ]]; then
  echo "Usage: $0 <profile> 'question for specialist profile'" >&2
  exit 2
fi
HERMES_BIN="${HERMES_BIN:-/opt/data/.local/bin/hermes}"
exec "$HERMES_BIN" --profile "$PROFILE" chat -q "$PROMPT"
