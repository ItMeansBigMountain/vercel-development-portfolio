# Vercel Flask Music App Deployment Pattern

Session-derived notes from modernizing a legacy Spotify-only Flask app into provider-neutral MusicAI and deploying it on Vercel.

## Useful pattern

- For legacy Flask apps with heavy imports, create a lightweight Vercel entry point at `api/index.py` instead of importing the full app at module load.
- Add a `/healthz` route that checks minimal app readiness and provider/env status without loading expensive music analysis modules.
- Lazy-load heavyweight services such as IBM Watson NLU, lyrics analyzers, or audio-processing clients only when the route actually needs them.
- Keep the public base URL explicit via env, e.g. `MUSICAI_PUBLIC_BASE_URL`, and set OAuth callback URLs from that value.
- Add `vercel.json` with Python function routing before deploy verification.

## Provider rollout pattern

- First deploy a stable modern shell and provider registry with clear states: connected, available-unconfigured, planned/coming-soon.
- Make unconfigured providers visible but honest; tell the user exactly which env vars/API apps are needed before connection flows can work.
- Keep Spotify/Genius/Watson working while adding Google/YouTube, Last.fm, Apple Music, SoundCloud, etc. as incremental adapters.

## Token storage pattern

- Replace `user_tokens.json` with database-backed token storage before adding more providers.
- Store tokens per user/provider with refresh token, expiry, scopes, external account ID, and timestamps.
- Encrypt at rest. If Python crypto dependencies are unavailable in a constrained deployment environment, an `openssl` subprocess fallback can be used as an interim implementation, but document the dependency and plan for managed DB/KMS later.
- Do not commit token DBs or secret env files.

## Verification checklist

- Confirm production homepage loads.
- Confirm `/healthz` returns JSON and does not time out.
- Confirm provider registry renders expected provider status.
- Confirm Vercel environment variables exist for current providers.
- Confirm OAuth provider dashboards include production callback URLs.

## Common callback/env vars

- Spotify callback: `https://<app-domain>/login/`
- YouTube callback: `https://<app-domain>/providers/youtube_music/callback`
- Last.fm callback: `https://<app-domain>/providers/lastfm/callback`
- Google/YouTube: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- Last.fm: `LASTFM_API_KEY`, `LASTFM_SHARED_SECRET`
