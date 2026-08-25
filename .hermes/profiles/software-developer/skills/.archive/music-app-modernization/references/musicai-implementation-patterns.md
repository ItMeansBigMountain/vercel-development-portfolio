# MusicAI implementation patterns

Session-derived implementation notes for modernizing a legacy Spotify-only Flask music app into a cross-provider MusicAI product.

## Useful pattern

- Start with a provider registry before building every OAuth flow. A small `MusicProvider` dataclass/registry lets the landing page and connection cards become dynamic from environment/config state.
- Keep the first UI pass provider-neutral: brand around `MusicAI`, not Spotify, and show planned providers as cards with connected/available/coming-soon state.
- Use env var presence to activate provider cards, but do not treat env vars as a substitute for OAuth implementation.
- Create `.env.example` early with every planned provider key/scope variable so the user can prepare vendor apps later.
- Preserve legacy line endings (CRLF if already present) when editing old projects to avoid noisy diffs; if diffs turn whole-file noisy, normalize only the files being intentionally committed and re-check the staged diff.
- If the repo has unrelated uncommitted changes, do not commit modernization work until the diff is separated or the user approves mixing changes. If the user approves a PR branch, create a feature branch from `origin/main`/`origin/master`, stage only modernization files, commit, push, and leave unrelated changes untouched.

## Token/OAuth migration pattern

- Replace `user_tokens.json` with one encrypted row per `(user_id, provider)` in SQLite or the app DB. Store provider, provider account ID, access token, refresh token, expiry, scopes, metadata, created/updated timestamps.
- Require `MUSICAI_TOKEN_SECRET` or a strong `FLASK_SECRET_KEY`; add token DB files to `.gitignore` and document the secret in `.env.example`.
- Provider OAuth adapters should expose `start_provider_oauth(provider_id)` and `complete_provider_oauth(provider_id, args, user_id)` so Flask routes stay provider-neutral.
- For Last.fm, use API-key session auth: `auth.getToken` → redirect to `https://www.last.fm/api/auth/` with callback → `auth.getSession`; sign API calls with sorted params + shared secret MD5.
- For YouTube/Google, use Authorization Code flow with `openid email profile` plus `https://www.googleapis.com/auth/youtube.readonly`, `access_type=offline`, state validation, and userinfo lookup for provider account metadata.
- If `cryptography` is not installed in a constrained legacy environment, an OpenSSL AES-256-CBC/PBKDF2 subprocess fallback can keep tokens encrypted until dependencies are installed; still keep `cryptography` in requirements for normal deployments.

## Good first implementation slice

1. Add `providers.py` or `providers/` abstraction with provider metadata, env-var requirements, scopes, feature flags, and connection URLs.
2. Update the Flask home route to pass provider registry data to templates.
3. Replace old provider-specific landing page with a modern connection grid and neutral hero copy.
4. Add CSS tokens for a modern dark/glass/music-forward visual system.
5. Add `.env.example` covering Spotify, Apple, Google/YouTube, SoundCloud, Deezer, Last.fm, Audius, Genius/Musixmatch/LRCLIB, AudD/ACRCloud, and analytics/intelligence APIs.
7. Verify encrypted token storage with a local round-trip using a throwaway DB and secret.

## Pitfalls

- Do not imply Apple Music, YouTube Music, Spotify, SoundCloud, Deezer, and Last.fm all expose equivalent user-library/listening-history APIs.
- Do not block UI modernization on full OAuth completion; provider cards can communicate capability/state honestly.
- Do not leave token storage as local JSON when moving toward multi-provider auth; plan encrypted database-backed storage early.
