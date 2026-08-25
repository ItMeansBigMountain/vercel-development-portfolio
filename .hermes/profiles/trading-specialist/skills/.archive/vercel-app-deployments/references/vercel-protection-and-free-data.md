# Vercel protection and free-data decisions

Session-derived reusable notes for Vercel legacy-project deployments.

## Disabling Vercel SSO deployment protection

When existing Vercel deployments return `401 Unauthorized` in anonymous/manual checks, inspect project detail for protection keys:

```bash
python - <<'PY'
import os,json,urllib.request
TOKEN=os.environ.get('VERCEL_TOKEN') or os.environ.get('VERCEL_API_TOKEN')
headers={'Authorization':'Bearer '+TOKEN}
projects=json.load(urllib.request.urlopen(urllib.request.Request('https://api.vercel.com/v9/projects?limit=100',headers=headers),timeout=30)).get('projects',[])
for p in projects:
    name=p['name']
    detail=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.vercel.com/v9/projects/{name}',headers=headers),timeout=30))
    print('\n##', name)
    for k in sorted(detail):
        if any(s in k.lower() for s in ['protect','password','sso','auth','public']):
            print(k, detail.get(k))
PY
```

Observed protection shape:

```json
"ssoProtection": {"deploymentType": "all_except_custom_domains"}
```

When the user approves public manual testing, disable it with:

```json
{"ssoProtection": null}
```

via `PATCH /v9/projects/{name}`. Then test app URLs anonymously. Outcomes can distinguish:

- `401` before patch: protection/auth blocked manual testing.
- `200` after patch: ready for manual review.
- `404` after patch: protection is fixed; the deployment itself needs rebuild/redeploy/alias repair.

## Free data/storage default

When the user asks to use SQLite/free options:

- Keep frontend-only projects on Vercel.
- For Django projects already using `django.db.backends.sqlite3`, preserve SQLite for demo/local mode and add seed data.
- For Vercel serverless, do not promise durable local SQLite writes. Use bundled read-only seed data, JSON, or a free hosted DB if writes are required.
- For apps with optional live integrations, ship sample/demo mode first and request credentials later.
- For persistent write-heavy Django/Flask apps, prefer a free/cheap persistent-disk host over forcing Vercel serverless.

## Documentation pattern

Add a short plan document to the workspace, e.g. `projects/FREE_HOSTING_AND_SQLITE_PLAN.md`, and link it from the projects README next to the Vercel tracker. Include:

- protection status,
- per-project backend/data plan,
- what can be done without credentials,
- which credentials are needed later.
