#!/usr/bin/env sh
set -eu

DOMAIN=${1:?usage: ./smoke-test.sh social.example.com}
BASE="https://$DOMAIN"
curl --fail --silent --show-error --location --max-time 30 "$BASE/" >/dev/null
curl --fail --silent --show-error --max-time 30 "$BASE/api/public/v1/integrations" \
  -H "Authorization: Bearer ${POSTIZ_API_KEY:?set POSTIZ_API_KEY for authenticated smoke test}" >/dev/null
printf 'HTTPS and authenticated Public API checks passed for %s\n' "$BASE"
