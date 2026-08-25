---
name: music-app-modernization
description: "Modernize music apps: multi-provider OAuth, music APIs, unified schemas, AI/music intelligence UX."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [music, oauth, api-integration, flask, ux, ai-music]
    related_skills: [spotify, popular-web-designs, humanizer]
---

# Music App Modernization

## When to use

Use this skill when improving an existing music app or designing a new consumer music product that integrates streaming services, lyrics providers, music metadata, listening history, recommendations, music recognition, or AI music analysis.

This is broader than controlling Spotify playback. It covers product architecture, provider selection, OAuth strategy, UI modernization, and normalized music data models.

## User-specific guidance

- The user may reference **MusicAI**, a legacy Flask app under `/opt/data/HeRmEz/legacy-projects/MusicAI`.
- MusicAI was observed as a Flask app branded **“SPOTTY AI”** using Spotify OAuth, Genius lyrics/API, IBM Watson NLU, templates/static assets, and local `user_tokens.json` token storage.
- The user wants MusicAI to move beyond Spotify, support multiple popular music vendors, look more modern, and use APIs that make the app more interesting to normal consumers.
- For **MusicAI specifically**, the selected provider stack is Spotify, Apple Music/MusicKit, YouTube/YouTube Music, and SoundCloud. The user explicitly excluded Deezer and Last.fm; do not reintroduce them into MusicAI provider cards, env templates, callbacks, docs, or key checklists unless the user reverses that decision.
- Current MusicAI product direction: **YouTube/YouTube Music is the primary working provider** for playlist-based vibe scanning. Spotify and SoundCloud should remain architected as roadmap/TODO connectors, not primary blockers, until Spotify Premium/dev-mode access and SoundCloud paid API access are worth resolving.
- If Spotify is blocked by Premium/dev-mode requirements and SoundCloud is blocked by paid API/subscription access, pivot the working MVP to YouTube/YouTube Music playlists while keeping Spotify/SoundCloud as roadmap provider cards and preserving the one-account/multi-OAuth architecture.
- Keep brainstorming concise and list-first unless the user asks for implementation detail.
- When a playlist-driven MusicAI feature pulls playlists successfully, do not stop at playlist metadata. The user expects the app to analyze every song individually and then aggregate those individual analyses into an overall playlist/taste read, with caching so repeated scans avoid unnecessary analyzer/API calls.

## Provider/API menu

### Streaming and user-library providers

Prioritize these for broad consumer value:

1. Spotify — keep as one provider, not the whole product identity. For MusicAI, park as roadmap if dev-mode/Premium/tester restrictions block API calls.
2. Apple Music / MusicKit — major platform support; library and playback ecosystem.
3. YouTube / YouTube Music via YouTube Data API — broad catalog, videos, playlists, creator/music discovery. For MusicAI, this is currently the primary working provider: use OAuth playlists and playlistItems as the core taste/vibe source.
4. SoundCloud — indie artists, likes, tracks, creator ecosystem. For MusicAI, park as roadmap if SoundCloud requires paid Artist Pro/API access.
5. Deezer — tracks, playlists, albums, user library.
6. Last.fm — listening history, scrobbles, artist similarity; often easier than full streaming OAuth.
7. Audius — independent/Web3 music discovery.

### Music intelligence and metadata

- MusicBrainz — open metadata backbone.
- ListenBrainz — open listening history/scrobble ecosystem.
- Genius — lyrics and annotations; useful but not enough alone.
- Musixmatch / LRCLIB — lyrics and synced lyrics options.
- Bandsintown / Ticketmaster — concerts and event discovery.
- Chartmetric / Songstats — serious artist/platform analytics if paid API access is available.

### Audio recognition and analysis

- AudD or ACRCloud — Shazam-like recognition.
- ShazamKit — Apple ecosystem recognition.
- Essentia / Essentia.js and librosa — local audio features, genre/mood/tempo analysis.
- Cyanite.ai — mood/tagging/similarity if API access is available.

### AI layer

- LLMs for taste summaries, playlist explanations, mood reports, and music-personality descriptions.
- Vector DBs such as pgvector, Pinecone, or Weaviate for cross-provider song/artist/lyric similarity.
- Agent frameworks only when there are real multi-step workflows, e.g. “build me a workout playlist from liked songs plus recent YouTube listens.”

## Recommended modernization sequence

1. Rebrand from provider-specific identity, e.g. `SPOTTY AI`, to neutral **MusicAI** or another cross-platform name.
2. Add a provider registry/abstraction before implementing every OAuth flow. For legacy Flask apps, a single `providers.py` with a `MusicProvider` dataclass is an acceptable first slice; larger apps can evolve to:
   - `providers/base.py`
   - `providers/spotify.py`
   - `providers/apple_music.py`
   - `providers/youtube.py`
   - `providers/soundcloud.py`
   - other provider modules only when they are actually in scope
3. Make the home/connection UI dynamic from provider metadata: required env vars, scopes, connection URL, feature flags, connected/available/coming-soon state, and setup copy.
4. Create or update `.env.example` early with all planned provider credentials so the user can prepare API apps when needed. For SoundCloud, include `SOUNDCLOUD_CLIENT_ID`, `SOUNDCLOUD_CLIENT_SECRET`, and `SOUNDCLOUD_CALLBACK_URL`; current SoundCloud OAuth uses OAuth 2.1 + PKCE, not a bare legacy authorization-code exchange.
5. Replace file-based `user_tokens.json` with database-backed encrypted token storage. For Vercel demos, `/tmp` SQLite is only an ephemeral fallback; real OAuth token persistence should use durable Postgres/Neon or equivalent and a health endpoint that reports backend/durability without exposing secrets.
6. Normalize identity before normalizing music data: create one internal account ID that can link multiple provider identities, then store provider tokens per `(account_id, provider)`. Use session state for the internal MusicAI account ID, not a provider-specific user ID.
7. Normalize provider data into a common schema: `User`, `ProviderAccount`, `Artist`, `Track`, `Album`, `Playlist`, `ListenEvent`, `Lyrics`, `AudioFeature`, `Insight`.
7. Build a modern connection screen with vendor cards: connected/disconnected state, scopes requested, last synced, reconnect/remove actions.
8. For Flask apps targeting Vercel, add a lightweight deployment entry point before deep feature work:
   - `api/index.py` should avoid importing heavy legacy analysis modules at module load.
   - Add `/healthz` that verifies minimal readiness and provider/env status.
   - If provider cards link to `/providers/<provider>/connect`, make sure the lightweight Vercel entrypoint also defines those connect/callback routes or imports/registers the provider blueprint; routes that exist only in the legacy local Flask app will 404 in production.
   - For MusicAI specifically, `/` should behave as an OAuth account/provider hub where users create/resume an account and connect Spotify, YouTube, SoundCloud, and later Apple Music. Do not leave successful callbacks landing on a placeholder JSON message.
   - Lazy-load heavyweight services such as Watson, lyrics analysis, or audio-processing clients only inside routes that need them.
9. Add cached per-item playlist analysis for playlist-driven providers before calling the product complete:
   - playlist cards should have an explicit action such as `Analyze every song`,
   - each playlist item should be normalized and analyzed individually,
   - playlist summaries should aggregate item-level sentiment/emotion/keyword/concept results into averages/counts,
   - cache keys should include user, provider, item type, provider item ID, analyzer version, and input hash.
   - See `references/youtube-playlist-analysis-cache.md` for the YouTube-first pattern.
10. For OAuth-backed dashboards, separate app-session persistence from provider-token persistence:
   - Flask sessions should store only the internal MusicAI account ID and be made permanent for a configurable period,
   - encrypted provider tokens should stay in durable Postgres/Neon,
   - every provider dashboard/playlist route should refresh expired access tokens from stored refresh tokens before forcing reconnect.
   - See `references/musicai-persistent-youtube-auth.md` for the YouTube/Google pattern.
11. Add a durable profile and manual song-scanner layer alongside provider playlists:
   - profile card with connected providers and provider avatar/meme fallback,
   - public or logged-in `/analyze-song` flow that accepts YouTube URLs or song names,
   - for MusicAI, preserve the legacy lyrics-first pipeline where possible: resolve song/artist, fetch lyrics through Genius or a fallback lyrics API, run lyrics through Watson NLU, and expose legacy frequency buckets for topics/entities/keywords/concepts/subjects/relations,
   - shared cached analysis infrastructure for manual song scans and playlist item scans,
   - analyzer normalization that keeps sparse song-title scans from caching/rendering all-zero emotion bars.
   - See `references/musicai-profile-meme-and-song-analysis.md`, `references/musicai-short-title-analysis-normalization.md`, and `references/musicai-lyrics-first-watson-insights.md`.
12. Add consumer-facing insights before complex automation:
   - music personality
   - mood over time
   - cross-platform taste comparison
   - “your week in music”
   - under-the-radar artist discovery
   - concerts/events near you
13. Add AI recommendation and playlist generation after the normalized data layer is reliable.

## OAuth architecture guidance

- Use a one-account/many-provider model for MusicAI-style apps: one internal app account links Spotify, YouTube/Google, SoundCloud, Apple Music, and future providers, instead of creating a separate app identity per OAuth provider.
- Use OAuth Authorization Code + PKCE where providers support it.
- Store provider, access token, refresh token, expiry, scopes, and account ID separately per user/provider.
- Keep the browser session focused on the internal account ID; make it persistent for the desired login window, then load encrypted provider tokens from durable storage on each dashboard/API request.
- Refresh expired access tokens server-side from stored refresh tokens before telling the user to reconnect.
- Encrypt tokens at rest; never commit token files, `.env`, or provider secrets.
- Make scopes visible in the UI so users understand what each vendor connection enables.
- Gracefully support providers that do not expose full OAuth/library access by using API keys, public metadata, or import flows.

## UI direction

Move away from old Bootstrap landing pages toward a modern consumer dashboard:

- Lead with provider-neutral positioning: track the mood, feel, and vibe of playlists/listening across multiple music vendors, then explain what the user's taste says about them.
- Keep a no-login lyric/text analyzer visible as the primary frictionless demo if the legacy app already has one.
- Keep a single-song analyzer available for users who want to paste a YouTube URL or type a song name and scan songs one by one; share cache logic with playlist analysis. For MusicAI, this should be lyrics-first when possible: fetch lyrics, run Watson NLU, and show topics/entities/keywords/concepts/subjects/relations rather than only title metadata.
- Treat profiles as part of the core product: show provider connections, account identity, and a profile picture. Use provider avatars when available, but preserve the fun meme-generator fallback so profiles do not feel empty.
- Dark/music-forward visual system with album-art gradients.
- Provider connection cards.
- “Taste profile” and “mood map” cards.
- Playlist/artist insight panels.
- Mobile-first layout.
- Clear privacy copy: what data is read, what is stored, how to disconnect.

## Pitfalls

- Do not design the app as Spotify-only if the user asks for MusicAI modernization.
- Do not promise every provider has the same OAuth or catalog access; music APIs vary heavily.
- Do not store OAuth tokens in JSON files for a production app.
- Do not use employer/company data or proprietary patterns when building consumer music/finance/cloud side projects.
- Do not over-explain API options when the user asks for a simple list; provide a concise ranked list first, then offer to implement.
- When provider OAuth secrets are pasted into chat, treat them as exposed: add them only to ignored local env files and Vercel/env managers, never commit them, then recommend rotating the secret after confirming the flow.
- For MusicAI Google/YouTube setup, extract `web.client_id` and `web.client_secret` from the Google OAuth JSON into `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`; verify `/healthz` reports `google_youtube: true` after Vercel redeploy.
- For MusicAI Spotify setup, the production callback URL is `https://musicai-rouge.vercel.app/login/`; `/login/` should redirect to Spotify when no code is present and exchange/store the token when Spotify returns with `code`.
- For MusicAI SoundCloud setup, the production callback URL is `https://musicai-rouge.vercel.app/providers/soundcloud/callback` and the local callback is `http://localhost:5000/providers/soundcloud/callback`. SoundCloud uses OAuth 2.1 + PKCE: generate/store a `code_verifier`, send the S256 `code_challenge` on authorize, and include `code_verifier` in the token exchange. SoundCloud docs currently say app/API-key registration requires Artist Pro.
- For MusicAI on Vercel, an OAuth callback error `unable to open database file` usually means SQLite is writing to the read-only app bundle. Use `/tmp/musicai_tokens.db` only for testing, then move to durable Postgres before real user data collection.
- For MusicAI, do not re-add Deezer or Last.fm after the user's correction; keep provider setup focused on Spotify, Apple Music, YouTube/YouTube Music, and SoundCloud.
- For MusicAI, when Spotify is blocked by Premium/dev-mode/tester requirements and SoundCloud requires paid API access, pivot the working product to YouTube playlists instead of continuing to chase paid blockers. Keep Spotify/SoundCloud as roadmap connectors in the architecture and UI.
- For a YouTube-first MusicAI MVP, scan `playlists` and `playlistItems` via the YouTube Data API, then infer first-pass vibe tags from playlist titles/descriptions and sample video titles. Be transparent that this is a title/metadata-based vibe scan until richer audio/lyrics metadata is added.
- If the user decides Spotify/SoundCloud access blockers are not worth solving now, do not keep pushing those integrations. Make YouTube playlists the active product path, mark Spotify/SoundCloud as roadmap/TODO, and keep the architecture ready for later.
- When deploying a modernization slice, give the user the live test URL, backup location, configured env status, missing API keys, exact OAuth callback URLs, and local smoke-test results in concise bullets.
- Before shipping/pushing MusicAI changes, run practical due diligence: Playwright smoke tests for homepage/provider positioning, `/healthz` durable storage, Watson analyzer API/page behavior, and provider OAuth redirect/scopes. See `references/musicai-smoke-test-and-ship.md`.
- For YouTube-first playlist scanning, users may expect deeper functionality than playlist listing: implement a per-playlist analysis route that fetches playlist items, analyzes each item individually, caches each analysis, and aggregates emotion/sentiment/keyword results. See `references/youtube-playlist-analysis-cache.md`.
- For MusicAI YouTube auth, durable token storage is not enough if Flask uses a non-permanent browser session. Set a permanent session for the internal account ID, store/refresh Google token expiry metadata in the durable token store, and call a refresh guard from dashboard/playlist routes. See `references/musicai-persistent-youtube-auth.md`.
- For MusicAI profiles, do not remove the funny meme-generator experience during modernization. Use provider profile images when present, but fall back to a generated meme/avatar if no image is available or the external meme API fails.
- For MusicAI manual analysis, keep a direct `/analyze-song` style flow that accepts YouTube URLs or plain song names, analyzes one song at a time, and reuses the same cache/analyzer infrastructure as playlist item scans. See `references/musicai-profile-meme-and-song-analysis.md`.
- For MusicAI song analysis, do not regress from the legacy lyrics→Watson behavior to title-only metadata scans. Resolve artist/title, fetch lyrics via Genius and a fallback lyrics API when needed, run the lyric text through Watson, expose the legacy topic/entity/keyword/concept/subject/relation frequency buckets, and clearly label any metadata-only fallback. See `references/musicai-lyrics-first-watson-insights.md`.
- For MusicAI song-title or playlist-item analysis, do not treat a successfully rendered page as proof the analyzer worked. Assert non-zero/meaningful emotion payloads; short titles can make Watson omit optional fields and can otherwise cache all-zero fallback rows. Normalize sparse title analysis and bump the analyzer cache version after fixing. See `references/musicai-short-title-analysis-normalization.md`.
- A `/healthz` boolean that only checks whether an API key is present is not proof the provider works. For MusicAI, verify Watson with a real `/api/analyze-text` POST; if the key is invalid, keep the no-login demo alive with a transparent local fallback and document that Watson credentials need rotation/fix.
- In legacy projects, preserve existing line endings such as CRLF where practical to avoid noisy diffs.
- If a repo already has unrelated uncommitted changes, avoid committing modernization work until the user approves or the changes can be cleanly separated.

## References

- `references/musicai-provider-landscape.md` — session-specific API/provider shortlist and modernization notes.
- `references/musicai-implementation-patterns.md` — implementation slice and pitfalls from converting a legacy Spotify-only Flask app toward provider-neutral MusicAI.
- `references/vercel-flask-musicai-deployment.md` — deploy/verify pattern for Flask music apps on Vercel, including lazy-load entry points, health checks, env vars, and OAuth callback reminders.
- `references/musicai-selected-provider-stack.md` — user correction narrowing MusicAI to Spotify, Apple Music, YouTube/YouTube Music, and SoundCloud while excluding Deezer and Last.fm.
- `references/musicai-youtube-vercel-oauth.md` — Google OAuth JSON extraction, Vercel env CLI pattern, production route verification, and secret-rotation note for MusicAI YouTube setup.
- `references/musicai-oauth-hub-and-provider-callbacks.md` — root account/provider hub requirements, Spotify/YouTube/SoundCloud callback URLs, Vercel env CLI pattern, `/tmp` SQLite workaround, and durable DB warning.
- `references/musicai-soundcloud-oauth-pkce.md` — SoundCloud OAuth 2.1 + PKCE setup for MusicAI, including endpoints, callback URLs, env vars, profile fetch, verification, and pitfalls.
- `references/musicai-one-account-multi-oauth-dashboard.md` — one-account/multi-provider identity mapping, dashboard sections for liked music/playlists/albums/recent plays/top music, taste feedback, Vercel durable-storage notes, and token-store file hygiene.
- `references/musicai-youtube-first-vibe-scan.md` — pivot pattern when Spotify/SoundCloud are blocked by paid/API access: make YouTube playlists the active MusicAI provider, infer vibe tags from playlist/video metadata, and keep other providers as roadmap connectors.
- `references/musicai-youtube-first-provider-fallback.md` — pivot pattern when Spotify/SoundCloud are blocked by Premium/paid API access: make YouTube playlists the active vibe-scan source while keeping roadmap connectors architected.
- `references/youtube-playlist-analysis-cache.md` — implement per-song YouTube playlist analysis, playlist-level aggregation, and durable cache keys to avoid repeated Watson/LLM analyzer calls.
- `references/musicai-persistent-youtube-auth.md` — persistent Flask app sessions plus Google/YouTube access-token refresh using durable encrypted provider-token storage.
- `references/musicai-profile-meme-and-song-analysis.md` — profile/provider connection card, meme-avatar fallback, manual `/analyze-song` flow, shared cache strategy, and verification checklist.
- `references/musicai-short-title-analysis-normalization.md` — prevent short song-title scans and stale cached fallback rows from rendering all-zero emotion fields; includes Watson optional-field parsing and regression checks.
- `references/musicai-lyrics-first-watson-insights.md` — restore/preserve MusicAI's legacy lyrics-first analysis pipeline: Genius/fallback lyrics API → Watson NLU → emotion/topic/entity/keyword/concept/subject/relation UI and verification checks.
