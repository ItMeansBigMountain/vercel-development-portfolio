# MusicAI one-account / multi-OAuth dashboard pattern

Session learning from turning MusicAI from a Spotify-branded lyric analyzer into a provider-neutral music intelligence hub.

## Product direction

- Landing page should sell cross-provider music intelligence: track the mood, feel, and vibe of playlists across multiple vendors, then give feedback and analysis on the user's music taste.
- Preserve the no-login text/lyric analyzer as the lowest-friction demo while making account login the path to richer dashboard insights.
- Dashboard should make one MusicAI account feel like a hub: connected providers, liked music, playlists, albums, recent plays, top tracks/artists, and plain-English taste feedback.
- The user explicitly wants liked music, playlists, and albums visible on the dashboard.

## Architecture pattern

- Use an internal `musicai_accounts` table (or equivalent) where one `account_id` can map to multiple provider identities.
- Store provider tokens per `(account_id, provider)` with encrypted access/refresh tokens, expiry, scopes, and provider user ID.
- During each OAuth callback, resolve an existing internal account from the session if present; otherwise link/create based on provider ID.
- Session should carry the internal MusicAI account ID (e.g. `musicai_user_id`) rather than treating each provider login as a separate app user.
- Keep provider connect routes distinct, e.g. `/providers/spotify/connect`, `/providers/youtube_music/connect`, `/providers/soundcloud/connect`, and keep callback states provider-specific.

## Spotify dashboard slice

For a first real dashboard, Spotify can populate most visible sections if scopes include:

- `user-library-read` for liked tracks and albums
- `playlist-read-private` for playlists
- `user-top-read` for top tracks/artists
- `user-read-recently-played` for listening history

Use these sections to generate a simple taste profile before building deeper ML: genre/artist clustering, vibe tags, recent mood, mainstream/indie balance, and playlist diversity.

## Durable storage on Vercel

- Encrypted SQLite in `/tmp` is only an ephemeral demo fallback on Vercel; use Vercel Postgres/Neon before real user token persistence.
- Health endpoints should expose redacted storage status: backend type, durable boolean, encryption readiness, and missing env keys by name only.
- Prefer app-specific env aliases alongside standard DB vars, e.g. `MUSICAI_DATABASE_URL`, `MUSICAI_TOKEN_DB`, and `DATABASE_URL`.
- Do not print or document connection strings, OAuth secrets, or API keys; use `[REDACTED]` in notes.
- If Neon provisioning is blocked by Vercel marketplace terms, treat it as an account/legal blocker and resume after the user accepts or explicitly authorizes terms acceptance.

## File hygiene

- Avoid generic token-module names if project `.gitignore` patterns ignore `*token*`; use a name like `musicai_secure_store.py` for durable storage logic.
- Keep token store modules out of tracked secret paths, but ensure the source code itself is tracked.
