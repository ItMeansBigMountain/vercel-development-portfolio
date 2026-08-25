# HeRmEz imported-project redeploy patterns

Use these notes when continuing deployment triage for `/opt/data/HeRmEz/projects` legacy/imported projects.

## Static/CRA redeploy baseline

For already-linked Vercel projects with `.vercel/project.json`:

```bash
npm run build
npx --yes vercel@latest deploy --prod --yes --token "$VERCEL_TOKEN"
```

Verify both the deployment URL and alias anonymously:

```bash
python3 - <<'PY'
import urllib.request
for url in ['https://deployment-url.vercel.app','https://alias.vercel.app']:
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:
        print(url, r.status, r.getheader('content-type'))
PY
```

## Express API in a subdirectory on Vercel

When a legacy Express API lives under a subdirectory like `SERVER/` and exports an app from `api/index.js`, a minimal `SERVER/vercel.json` that works with Vercel serverless is:

```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.js", "use": "@vercel/node" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "api/index.js" }
  ]
}
```

Deploy from the API subdirectory, not the repo root:

```bash
cd /opt/data/HeRmEz/projects/<project>/SERVER
npx --yes vercel@latest deploy --prod --yes --token "$VERCEL_TOKEN"
```

If Vercel returns `FUNCTION_INVOCATION_FAILED`, use expanded logs:

```bash
npx --yes vercel@latest logs <deployment-or-alias> --token "$VERCEL_TOKEN" --since 1h --expand --limit 20
```

## Sequelize + MySQL on Vercel serverless

A common runtime error is:

```text
Error: Please install mysql2 package manually
```

Even when `mysql2` is listed in dependencies, Sequelize may need an explicit dialect module inside the serverless bundle:

```js
const { Sequelize } = require('sequelize');
const mysql2 = require('mysql2');

const databaseUrl = process.env.DATABASE_URL || process.env.MYSQL_URL;

const sequelize = databaseUrl
  ? new Sequelize(databaseUrl, {
      dialect: 'mysql',
      dialectModule: mysql2,
      logging: false,
    })
  : new Sequelize(
      process.env.MYSQL_DATABASE || 'app',
      process.env.MYSQL_USER || 'root',
      process.env.MYSQL_PASSWORD || '',
      {
        dialect: 'mysql',
        dialectModule: mysql2,
        host: process.env.MYSQL_HOST || 'localhost',
        logging: false,
      }
    );
```

Public/no-DB routes can then verify the API shell, while DB-backed auth/highscore routes still need a real `DATABASE_URL`/`MYSQL_URL` or a storage refactor.

## Demo-mode fallback for manual login/signup review

When the user needs a legacy app to be testable before real database provisioning, add an explicit demo-mode storage path instead of letting auth routes hang on localhost MySQL. This is appropriate for manual review only; document that data is transient across cold starts/redeploys.

Pattern for Express auth APIs:

- Detect DB availability from env (`DATABASE_URL`, `MYSQL_URL`, or host/user/db keys), not from a failed request timeout.
- If no DB is configured, skip Sequelize/model calls and use module-level in-memory stores such as `Map` for users and arrays for scores.
- Keep the response contract identical to the real backend. If the frontend expects `{ token }` after signup/login, demo signup must also return a JWT.
- Sign JWTs with `process.env.JWT_SECRET || process.env.SECRET_KEY || 'demo-development-secret'` so private-route flows can be verified without secrets, but make the fallback visibly demo-only in logs/docs.
- Verify the full remote flow with a script: `POST /api/signup`, `POST /api/login`, and `GET /api/private` using the token.
- Record the blocker as "needs durable database for persistence" rather than "login broken" once demo mode is live.

Minimal remote verification script:

```python
import json, time, urllib.request
base='https://<api-alias>.vercel.app/api'
email=f'demo-{int(time.time())}@example.com'
payload={'name':'Demo User','email':email,'password':'password123'}

def req(path, body=None, token=None):
    data=json.dumps(body).encode() if body is not None else None
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']='Bearer '+token
    r=urllib.request.urlopen(urllib.request.Request(base+path,data=data,headers=headers),timeout=30)
    return r.status, json.loads(r.read().decode() or '{}')

status, signup=req('/signup', payload)
assert status == 200 and signup.get('token'), signup
status, login=req('/login', {'email': email, 'password': payload['password']})
assert status == 200 and login.get('token'), login
status, private=req('/private', token=login['token'])
assert status == 200, private
print('signup/login/private OK', private)
```

## No-login leaderboard simplification for prototype games

When a legacy game/quiz app has login only to attach a name to a high score, prefer simplifying the product before provisioning a database:

- Remove login/signup from the frontend navigation and route directly to the game/home screen.
- Collect only a display name after the game is complete, alongside the final score/time.
- Submit anonymous leaderboard rows such as `{ username, score, time }` to the existing score endpoint.
- Render the leaderboard from the API response; do not leave the screen as console-only logging.
- Sort in the API by highest score and then fastest time. If there is no durable DB, use a clearly documented module-level in-memory array as demo mode.
- Document the distinction: **no user database needed** for the current product, but a tiny persistent store is still needed if global leaderboard rows must survive cold starts/redeploys.
- Verification should include frontend HTTP 200, `GET /api/highscores`, `POST /api/add-highscore` without auth, and readback that the posted score appears.

This pattern is especially useful for Expo web demos where auth friction blocks review and the user only asked for a playable leaderboard.

## Django API on Vercel with no-secret latest-news demo fallback

For legacy Django apps that need a deployable API before paid/private news or LLM credentials are ready:

- Add `requirements.txt` in the Django project folder with only needed runtime packages (`Django`, `djangorestframework`, auth/CORS libs). Avoid optional SDKs unless the endpoint requires them.
- Create `api/index.py` for Vercel Python:

```python
from stock_news_backend.wsgi import application as app
```

- Use a minimal `vercel.json` from the Django backend directory:

```json
{
  "version": 2,
  "builds": [{ "src": "api/index.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "api/index.py" }]
}
```

- Make `settings.py` production-safe enough for Vercel: import `os`, read `SECRET_KEY` from env with a demo fallback, default `DEBUG=False`, and set `ALLOWED_HOSTS` to include `.vercel.app`, `localhost`, and `127.0.0.1`.
- If a public demo analysis route must work without login, put the specific path (for example `/api/stocks/analyze-stocks/`) before catch-all/detail routes like `/api/stocks/<int:stock_id>/`.
- If IBM Watson/NewsAPI credentials are missing, keep those integrations optional and add a transparent fallback. For stock-news sentiment, a workable no-secret fallback is Yahoo Finance RSS via `https://feeds.finance.yahoo.com/rss/2.0/headline?s=<TICKER>&region=US&lang=en-US` plus a documented keyword heuristic that returns the same response shape as the future LLM/NLU path.
- For manual-review frontends, browser `localStorage` can hold demo portfolio rows while the API only performs read-only analysis. Document that durable accounts/portfolio storage are future work.
- Verify locally with `python manage.py check`, Django tests for the public endpoint, then anonymous remote `curl` against both `/api/health/` and the JSON analysis endpoint.

## Expo web frontend in a nested app folder

For older/imported Expo apps nested under a subfolder:

1. Install from the app folder: `npm ci`.
2. Export web: `npx expo export --platform web`.
3. Use a nested app `vercel.json`:

```json
{
  "outputDirectory": "dist",
  "framework": null,
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

4. If the Vercel project is linked at the parent folder, create/verify `.vercel/project.json` in the nested app folder before deploying so the CLI targets the intended frontend project.
5. Deploy from the nested app folder:

```bash
cd /opt/data/HeRmEz/projects/<project>/<expo-app-folder>
npx --yes vercel@latest deploy --prod --yes --token "$VERCEL_TOKEN"
```

Patch hardcoded LAN/local API URLs in the Expo screens to the deployed API alias before export, e.g. `https://<api-alias>.vercel.app/api`.

## Turning broken image prompts into reliable lesson visuals

For imported Expo quiz/education games, missing or meaningless image prompts are often a product/content issue, not just an asset-path issue. If the app uses a placeholder icon for every question or the web export fails to show prompt images, consider replacing question images with rendered lesson cards instead of hunting for unavailable assets.

Pattern:

- Move quiz content into a data module such as `codology/data/basic13Questions.js` so tests can assert content coverage separately from UI.
- For code-learning games, render a styled `Code Picture`/code-card (`View` + monospace `Text`) rather than `<Image source={require('../assets/...')}>`. This makes the visual prompt deterministic in Expo web and more useful for students.
- Include language labels, short task text, code snippets, multiple-choice answers, and kid-friendly hints/tips in each question object.
- Add source-check tests that assert required curriculum coverage (for example, all Basic 13 IDs), both target languages, and absence of old static asset references.
- After deploy, verify the alias returns HTTP 200 and inspect the deployed JS bundle for expected content strings and absence of the removed asset path when browser automation is unavailable.

Example bundle probe:

```bash
python - <<'PY'
import re, urllib.request
html=urllib.request.urlopen('https://<alias>.vercel.app', timeout=30).read().decode(errors='ignore')
for src in re.findall(r'<script[^>]+src="([^"]+)"', html):
    url='https://<alias>.vercel.app'+src if src.startswith('/') else src
    js=urllib.request.urlopen(url, timeout=30).read().decode(errors='ignore')
    print('Basic 13' in js, 'Code Picture' in js, '../assets/' in js, len(js))
PY
```

## Tracking

After each redeploy, update both:

- `/opt/data/HeRmEz/projects/README.md` tracker row and legacy URL section.
- `/opt/data/HeRmEz/projects/VERCEL_TRIAGE.md` with exact URLs, verified checks, fixes made, and remaining blockers.
