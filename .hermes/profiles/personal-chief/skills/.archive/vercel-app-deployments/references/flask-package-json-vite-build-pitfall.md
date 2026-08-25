# Vercel Flask deploy with Playwright/package.json present

Use this when a legacy Flask app on Vercel later gains `package.json` for Playwright or other dev tooling. Vercel may infer a Node/Vite build and run `vite build`, causing deployment failure even though the app is Python/Flask.

## Symptom

During `npx vercel deploy --prod`, build output can end with:

```txt
Installing dependencies...
Error: Command "vite build" exited with 127
```

This can happen after adding Playwright smoke tests via `package.json` to a Flask app that previously deployed through implicit settings.

## Fix

Add an explicit Vercel Python entrypoint and route config so the project is treated as a Python function app.

`api/index.py`:

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

`vercel.json`:

```json
{
  "version": 2,
  "builds": [{ "src": "api/index.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "api/index.py" }]
}
```

Then verify locally and deploy:

```bash
python -m py_compile musicAI.py api/index.py
npx vercel deploy --prod --token "$VERCEL_TOKEN"
```

## Notes

- The Vercel warning that project dashboard Build Settings will not apply is expected when `builds` exists in `vercel.json`.
- Do not delete `package.json` if it is needed for Playwright smoke tests; make deployment explicit instead.
- Keep `.vercel/`, `.env*`, `node_modules/`, Playwright browser caches, and reports ignored.
