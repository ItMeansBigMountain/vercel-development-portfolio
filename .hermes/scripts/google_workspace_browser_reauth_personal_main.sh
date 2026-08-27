#!/bin/bash
set -euo pipefail
export PLAYWRIGHT_BROWSERS_PATH=/opt/data/cache/ms-playwright
exec /opt/data/.venvs/google-oauth-browser/bin/python /opt/data/scripts/google_workspace_browser_reauth.py personal-main
