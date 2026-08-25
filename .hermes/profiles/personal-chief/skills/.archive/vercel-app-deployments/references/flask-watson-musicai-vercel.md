# Legacy Flask + Watson NLU app on Vercel

Use this reference when converting an existing legacy Flask project with API credentials (Spotify/Genius/Watson/Imgflip-style) into a Vercel-deployable Python app while preserving the original Flask module.

## Pattern discovered

A legacy Flask app may expose `application = flask.Flask(...)` in a non-standard filename such as `musicAI.py`, with templates/static assets at project root and no Vercel config. Vercel Python can still deploy it by adding a tiny `api/index.py` WSGI shim and routing all paths to it.

### Minimal Vercel entrypoint

Create `api/index.py`:

```python
"""Vercel Python entrypoint for a legacy Flask app."""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from musicAI import application as app  # adapt module name

application = app
```

Create `vercel.json`:

```json
{
  "version": 2,
  "builds": [{ "src": "api/index.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "api/index.py" }]
}
```

## Credential/env handling

- Keep real credentials in ignored `.env` files and Vercel project env vars; do not commit or print values.
- For direct CLI deploys where env vars already exist in `.env`, source them locally and pass only variable values to `npx vercel --env KEY="$KEY"` so the deployment receives them without writing secrets to tracked files.
- Favor multiple compatible Watson variable names when the legacy code uses old names and new code uses clearer names, e.g. `WATSON_API_KEY`, `WATSON_SERVICE_URL`, `WATSON_NLU_APIKEY`, `WATSON_NLU_URL`, `IBM_NLU_API_KEY`, `IBM_NLU_URL`.

## Make integrations testable without full OAuth

For apps whose main value is hidden behind Spotify/OAuth, add a low-friction public verification path before deploying:

- `/healthz` returns non-secret booleans for configured integrations.
- `/api/analyze-text` accepts JSON text and exercises Watson NLU directly.
- `/analyze-text` provides a simple UI for manual testing without Spotify login.

This proves the AI integration and gives the user something useful immediately while OAuth redirect whitelisting is pending.

## Verification checklist

Local:

```bash
python -m py_compile musicAI.py watson.py api/index.py
python test_app.py
python - <<'PY'
import watson
print(type(watson.nlu_client).__name__)
print(watson.ai_to_Text('This song feels joyful and energetic.')['sentiment'])
PY
```

Run the Flask app and verify:

```bash
curl -fsS http://127.0.0.1:8080/healthz
curl -fsS http://127.0.0.1:8080/analyze-text
curl -fsS -X POST http://127.0.0.1:8080/api/analyze-text \
  -H 'Content-Type: application/json' \
  -d '{"text":"This track is bright, confident, joyful, and made for winning."}'
```

Remote after Vercel deploy:

- Check public `/healthz` returns HTTP 200 and non-secret config booleans.
- Check `/analyze-text` returns HTTP 200.
- POST `/api/analyze-text` and confirm `ok: true` plus a Watson sentiment label.
- Document any remaining OAuth redirect URL that must be added in the provider dashboard, including the trailing slash if the Flask route requires it.

## Pitfalls

- Do not report full Spotify playlist auth as verified until the production callback URL is added in Spotify Developer settings and the OAuth flow is manually tested.
- Avoid committing `.vercel/`, `.env`, local venvs, credentials, generated token JSON, and other deployment artifacts.
- Legacy files with CRLF may trigger `git diff --check` trailing-whitespace noise after patching; normalize only the edited hunk or use targeted cleanup, not a huge unrelated formatting rewrite.
