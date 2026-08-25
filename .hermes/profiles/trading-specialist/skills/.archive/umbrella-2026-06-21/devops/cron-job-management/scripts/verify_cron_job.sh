#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <job_id> <script_path>"
  exit 1
fi

JOB_ID=$1
SCRIPT_PATH=$2

echo "Validating cron job $JOB_ID script $SCRIPT_PATH"

if [[ ! -f "$SCRIPT_PATH" ]]; then
  echo "❌ Script file does not exist: $SCRIPT_PATH"
  exit 1
fi

if [[ ! -x "$SCRIPT_PATH" ]]; then
  echo "⚙️  Making script executable..."
  chmod +x "$SCRIPT_PATH"
fi

echo "✅ Script exists and is executable at $SCRIPT_PATH"