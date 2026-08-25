# Flask + Spotify OAuth on Vercel

Use this when deploying a legacy Flask app to Vercel that starts Spotify OAuth from a server-rendered page.

## Durable lessons

- Spotify redirect URI comparison is exact. The value in the Spotify Developer Dashboard must match the app's `redirect_uri` exactly, including scheme, host, path, and trailing slash.
- Do not hand-concatenate Spotify authorize URLs. Use query encoding (`urllib.parse.urlencode` in Python) so `redirect_uri` becomes percent-encoded and scope spaces become `+`/`%20`.
- Strip trailing whitespace from the joined scope string before encoding. A trailing space in `scope` can make the generated authorize URL fragile.
- For Flask, support both `/login/` and `/login` routes when practical, but keep the configured `SPOTIFY_CALLBACK_URL` to one canonical exact URI.
- If the production Vercel alias is the user-facing URL, the callback should usually be that alias, not the per-deployment preview URL.
- A post-callback Spotify API failure can look to the user like the login button simply refreshed the app if the callback handler catches the error and redirects to `/`. Do not silently redirect home after token/profile fetch failures; render an error page with the provider HTTP status and log the response body server-side with secrets redacted.
- Add a temporary, secret-free OAuth diagnostic endpoint for production debugging. It should expose only booleans and derived values such as `spotify_client_id_present`, `spotify_client_secret_present`, configured callback URL, generated redirect URI, callback-match boolean, response type, scope count, and scope names. Do not expose client secrets, auth codes, access tokens, refresh tokens, or Authorization headers.
- Add callback correlation logging before asking the user to retry OAuth: generate a short `request_id`, log sanitized callback args (`code` as `[present]`), token exchange HTTP status/body on failures, and provider profile-fetch HTTP status/body on failures. Then stream Vercel logs while the user performs the sign-in. This turns vague “refresh/403” reports into a precise boundary failure.
- Start OAuth apps with the minimum read-only scopes needed for the current demo. Broad playback/write/streaming scopes can trigger Spotify approval/access failures and make debugging look like a redirect-loop problem. Add scopes only when a verified feature needs them.
- Do not store OAuth token caches in the deployed project directory on Vercel serverless. Use `/tmp/...` for an MVP ephemeral cache, or a real database/session store for durable accounts.
- As of current Spotify Web API docs, newly-created apps start in development mode and the app owner must have an active Spotify Premium account for development-mode API requests to function. A successful OAuth code exchange followed by `GET /v1/me` returning `403` with body `Active premium subscription required for the owner of the app...` is not a Vercel or redirect bug; it is a Spotify app/account-status blocker. The app may also need each tester added under Users Management/allowlist. Surface this exact provider body to the user instead of continuing to tweak scopes or redirect URLs.

## Known-good Python pattern

```python
import urllib.parse

scopes = [
    'user-read-email',
    'user-read-private',
    'playlist-read-private',
]
spotty_full_permission = ' '.join(scopes)

def spotify_authorize_url(response_type='code'):
    params = {
        'client_id': spotify_client_id,
        'response_type': response_type,
        'redirect_uri': spotify_callback_url,
        'scope': spotty_full_permission.strip(),
    }
    return 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params)

@app.route('/login/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login_callback():
    ...
```

## Verification checklist

1. Fetch the live app homepage and extract the Spotify authorize URL.
2. Confirm the raw URL contains a percent-encoded redirect URI, e.g. `redirect_uri=https%3A%2F%2Fexample.vercel.app%2Flogin%2F`.
3. Confirm the raw URL contains no literal spaces.
4. Parse the query string and confirm `redirect_uri` decodes to the exact dashboard value.
5. Request the Spotify authorize URL with redirects allowed. If correct, it should go to Spotify login/consent, not a plain text `redirect_uri: Not matching configuration` page.

## Vercel runtime-log workflow for OAuth callbacks

- Prefer `vercel logs <specific-deployment-url> --expand --since 10m` when inspecting just-added callback instrumentation; the production alias may summarize requests, while the concrete deployment URL tends to show the expanded function output reliably.
- Use `vercel logs <specific-deployment-url> --expand --follow` while the user retries sign-in, with watch targets mentally focused on callback boundaries such as `OAUTH_CALLBACK_START`, `OAUTH_TOKEN_EXCHANGE_RESPONSE`, and `SPOTIFY_API_RESPONSE`.
- If testing a synthetic callback, hit `/login/?error=access_denied&error_description=manual_test` to verify the route logs and renders an error page without needing a real Spotify account.
- Vercel may classify dependency `SyntaxWarning`s as `error` level even when the HTTP status is 200. Treat those as noise unless they correlate with failed requests.

## Spotify development-mode 403 pattern

Current Spotify documentation states that newly-created apps begin in development mode. In that mode:

- the **app owner** must have an active Spotify Premium account for API requests to function;
- up to 5 authenticated Spotify users can test the app;
- each tester must be added in the app's Users Management/allowlist;
- users may be able to complete OAuth without being allowlisted, but API requests using their token can still return `403`.

Diagnostic signature:

```text
OAUTH_CALLBACK_START ... args={'code': '[present]'}
OAUTH_TOKEN_EXCHANGE_RESPONSE ... status=200 body=[success]
SPOTIFY_API_RESPONSE ... endpoint=https://api.spotify.com/v1/me status=403 body=Active premium subscription required for the owner of the app. When the subscription status changes, it can take a few hours before requests are allowed again.
```

Interpretation: login and token exchange are working. The next action is in the Spotify Developer Dashboard/account, not code. Ask the owner to ensure the developer app owner account has Premium, wait a few hours after any subscription change, and add tester accounts under Users Management. Only continue code debugging if the provider body changes.

## Vercel deployment notes

For Python Flask on Vercel, a minimal serverless entrypoint works well:

```python
# api/index.py
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from musicAI import application as app
application = app
```

```json
{
  "version": 2,
  "builds": [{ "src": "api/index.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "api/index.py" }]
}
```

When redeploying with secrets from a local ignored `.env`, pass required production values through `npx vercel --prod --env KEY="$KEY" ...` or set them in Vercel project settings. Never print or commit the values.
