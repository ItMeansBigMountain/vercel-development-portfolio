# MusicAI YouTube OAuth + Vercel setup notes

Session learning from wiring Google/YouTube credentials into the Vercel-hosted MusicAI Flask preview.

## Selected MusicAI provider stack

For this user's MusicAI project, keep the provider roadmap focused on:

- Spotify
- Apple Music / MusicKit
- YouTube / YouTube Music via Google OAuth + YouTube Data API v3
- SoundCloud

Do not reintroduce Deezer or Last.fm into provider cards, env templates, docs, or key checklists unless the user explicitly reverses that decision.

## Required Google values

From a Google OAuth web client JSON, extract only:

- `web.client_id` -> `GOOGLE_CLIENT_ID`
- `web.client_secret` -> `GOOGLE_CLIENT_SECRET`

Expected redirect URI for the deployed MusicAI app:

```txt
https://musicai-rouge.vercel.app/providers/youtube_music/callback
```

Optional local redirect URI:

```txt
http://localhost:5000/providers/youtube_music/callback
```

## Local env handling

Add/update these in `.env` without committing secrets:

```txt
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

Verify `.env` is ignored before proceeding:

```bash
git check-ignore -q .env && echo '.env is gitignored.'
```

## Vercel CLI pattern

For Production/Development, non-interactive env addition worked with stdin or `--value`:

```bash
TOKEN="${VERCEL_TOKEN:-${VERCEL_API_TOKEN:-}}"
printf '%s' "$GOOGLE_CLIENT_ID" | npx vercel env add GOOGLE_CLIENT_ID production --token "$TOKEN"
printf '%s' "$GOOGLE_CLIENT_SECRET" | npx vercel env add GOOGLE_CLIENT_SECRET production --token "$TOKEN"
printf '%s' "$GOOGLE_CLIENT_ID" | npx vercel env add GOOGLE_CLIENT_ID development --token "$TOKEN"
printf '%s' "$GOOGLE_CLIENT_SECRET" | npx vercel env add GOOGLE_CLIENT_SECRET development --token "$TOKEN"
```

Preview envs may prompt for a git branch even with `--yes`/`--value`; if the task only needs the production URL, do not get blocked on preview envs. Verify with:

```bash
npx vercel env ls --token "$TOKEN" | grep -E 'GOOGLE_CLIENT_(ID|SECRET)|name'
```

Then redeploy:

```bash
npx vercel deploy --prod --yes --token "$TOKEN"
```

## Vercel Flask preview route pitfall

If `api/index.py` is a lightweight Vercel entrypoint, routes defined only in the legacy `musicAI.py` app are not available in production. Provider cards can render with `/providers/youtube_music/connect` but return 404 unless the Vercel entrypoint also defines connect/callback routes or imports/registers the relevant blueprint.

Minimal verification:

```bash
curl -sS https://musicai-rouge.vercel.app/healthz
# expect: "google_youtube": true

python3 - <<'PY'
import urllib.request, urllib.error
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None
opener = urllib.request.build_opener(NoRedirect)
try:
    opener.open('https://musicai-rouge.vercel.app/providers/youtube_music/connect', timeout=20)
except urllib.error.HTTPError as e:
    print('status', e.code)
    print('location', e.headers.get('Location','')[:220])
PY
# expect status 302 and Location beginning https://accounts.google.com/o/oauth2/v2/auth?...client_id=...
```

## Security note

If a client secret is pasted into Discord/chat, add it immediately but recommend rotating it in Google Cloud after confirming the OAuth flow, because the pasted secret should be treated as exposed.
