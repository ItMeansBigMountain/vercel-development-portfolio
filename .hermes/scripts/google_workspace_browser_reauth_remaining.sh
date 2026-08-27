#!/bin/bash
set -u
export PLAYWRIGHT_BROWSERS_PATH=/opt/data/cache/ms-playwright
PY=/opt/data/.venvs/google-oauth-browser/bin/python
SCRIPT=/opt/data/scripts/google_workspace_browser_reauth.py
status=0
for profile in personal-secondary trapiistan classicalechos burner; do
  if ! "$PY" "$SCRIPT" "$profile"; then
    status=1
  fi
done
exit "$status"
