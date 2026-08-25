# MusicAI OAuth hub + provider callback notes

Session-derived implementation notes for the MusicAI Flask/Vercel modernization.

## Selected provider stack

For this project, keep the live provider scope focused on:

- Spotify
- YouTube / YouTube Music via Google OAuth + YouTube Data API v3
- SoundCloud
- Apple Music / MusicKit later

Do not reintroduce Deezer or Last.fm unless the user explicitly reverses scope.

## Product flow correction

The root URL should not just be a marketing page or JSON placeholder. The desired base experience is an account/provider hub:

1. User lands on `/`.
2. User can create/resume a MusicAI account through OAuth.
3. User can connect multiple music services from the same hub.
4. App stores provider tokens per user/provider.
5. App later syncs albums, playlists, liked/saved songs, top artists/tracks, recent listening, and service-specific metadata into a cross-platform taste profile.

For the Vercel lightweight entrypoint (`api/index.py`), mirror any provider connect/callback routes exposed by provider cards. If cards link to `/providers/<provider>/connect`, those routes must exist in the Vercel app, not only the legacy local Flask app.

## Callback URLs

Production callbacks used in this project:

```txt
SPOTIFY_CALLBACK_URL=https://musicai-rouge.vercel.app/login/
GOOGLE / YouTube redirect=https://musicai-rouge.vercel.app/providers/youtube_music/callback
SOUNDCLOUD_CALLBACK_URL=https://musicai-rouge.vercel.app/providers/soundcloud/callback
MUSICAI_PUBLIC_BASE_URL=https://musicai-rouge.vercel.app
```

Local optional callbacks:

```txt
http://localhost:5000/login/
http://localhost:5000/providers/youtube_music/callback
http://localhost:5000/providers/soundcloud/callback
```

## Vercel env CLI pattern

Use `--value`, `--yes`, and `--force` to avoid interactive env prompts:

```bash
TOKEN="${VERCEL_TOKEN:-${VERCEL_API_TOKEN:-}}"
npx vercel env add SPOTIFY_CLIENT_ID production --value "$SPOTIFY_CLIENT_ID" --yes --force --token "$TOKEN"
npx vercel env add SPOTIFY_CLIENT_SECRET production --value "$SPOTIFY_CLIENT_SECRET" --yes --force --token "$TOKEN"
npx vercel env add SPOTIFY_CALLBACK_URL production --value 'https://musicai-rouge.vercel.app/login/' --yes --force --token "$TOKEN"
npx vercel env add MUSICAI_PUBLIC_BASE_URL production --value 'https://musicai-rouge.vercel.app' --yes --force --token "$TOKEN"
npx vercel env add MUSICAI_TOKEN_DB production --value '/tmp/musicai_tokens.db' --yes --force --token "$TOKEN"
```

When adding Preview env vars, Vercel CLI may still prompt for a git branch; prefer production first for live validation, or pass a branch intentionally.

## Serverless token storage gotcha

Vercel serverless cannot write SQLite DBs into the deployed app bundle. If an OAuth callback fails with:

```json
{"error":"unable to open database file","ok":false,"provider":"youtube_music"}
```

then the token store is probably trying to write `musicai_tokens.db` in a read-only working directory. For short-term testing, default `MUSICAI_TOKEN_DB` to `/tmp/musicai_tokens.db` when `VERCEL` is present, and/or set that env var explicitly.

Important: `/tmp` is ephemeral. It is acceptable for proving OAuth works, but not for real user accounts. Before collecting real albums/playlists/songs across providers, move provider token storage and synced library data to a durable database such as Neon Postgres, Vercel Postgres, or Supabase Postgres.

## SoundCloud implementation notes

Expected env vars:

```txt
SOUNDCLOUD_CLIENT_ID=
SOUNDCLOUD_CLIENT_SECRET=
SOUNDCLOUD_CALLBACK_URL=https://musicai-rouge.vercel.app/providers/soundcloud/callback
```

Connect URL shape:

```txt
https://secure.soundcloud.com/authorize?client_id=...&redirect_uri=...&response_type=code&state=...
```

Token exchange endpoint:

```txt
https://secure.soundcloud.com/oauth/token
```

Profile probe after token exchange:

```txt
GET https://api.soundcloud.com/me
Authorization: OAuth <access_token>
```

SoundCloud API/app access may be approval-gated; if credentials are absent, the route should return a clear `SOUNDCLOUD_CLIENT_ID is not configured` style message rather than silently failing.

## Verification checklist

After env updates and deploy:

```bash
curl -sS https://musicai-rouge.vercel.app/healthz
```

Expected configured booleans once keys exist:

```json
{
  "spotify": true,
  "google_youtube": true,
  "soundcloud": true,
  "apple_music": false
}
```

Route checks:

- `/` renders the account/provider hub.
- `/login/` without a code redirects to Spotify OAuth.
- `/providers/youtube_music/connect` redirects to Google OAuth.
- `/providers/soundcloud/connect` redirects to SoundCloud OAuth once SoundCloud keys are present.
- Successful callbacks redirect to `/Dashboard`, not a placeholder JSON response.
