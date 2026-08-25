# Faceless YouTube Automation on VPS

Use this reference when the user wants a faceless YouTube channel built with Hermes rather than Claude/Claude Code, especially for discipline/self-improvement channels using one existing YouTube account.

## Proven project shape

- Project directory: create the app/pipeline under the user's workspace projects directory, not as a loose script.
- Dashboard: deploy a lightweight Vercel dashboard for monitoring project status, generated scripts, candidates, and upload history.
- Production: run rendering/upload on the VPS/headless environment; do not depend on GUI editing tools.
- First uploads: always upload as `private` unless the user explicitly asks otherwise.
- Visual style for low-cost faceless videos: kinetic text, simple diagrams, captions, waveform/progress animations, and stock-free generated backgrounds instead of expensive image/video generation APIs.
- Voice/audio: free/cheap TTS first (for example Edge TTS or Piper) unless the user asks for a paid voice provider.

## OAuth upload pattern

For automated YouTube uploads, service accounts are usually not the right credential. Use user OAuth with the `youtube.upload` scope and store a refreshable token in a secrets directory outside the repo.

Recommended helper scripts:

- `scripts/youtube_oauth.py` — generate auth URL, exchange returned code/redirect URL, and check token validity.
- `scripts/upload_youtube.py` — upload MP4s with privacy defaulting to `public` for approved automation lanes; private/unlisted only when explicitly requested or required by YouTube/API compliance.

Recommended token location pattern:

```text
/opt/data/secrets/<project-name>/youtube_upload_token.json
```

Do not commit OAuth client secrets, access tokens, or refresh tokens. When documenting outputs, redact secrets.

## OAuth client setup checklist

If no working OAuth client exists, have the user create or provide a Google OAuth client:

1. Open Google Cloud Console → APIs & Services → Credentials.
2. Select or create a project.
3. Enable **YouTube Data API v3**.
4. Create **OAuth Client ID → Web application**.
5. Add redirect URI:

```text
http://localhost:5000/
```

6. Download the client secret JSON and place it in a secure path on the VPS, or have the user upload it.
7. Generate the auth URL from the VPS helper script.
8. User approves once, then pastes back the full localhost redirect URL or code.
9. Exchange it for the persistent token and immediately run a token check.

Headless PKCE pitfall: `google-auth-oauthlib` may auto-generate a `code_verifier` when generating the auth URL. If the exchange happens in a separate process, persist that `code_verifier` in the pending OAuth state and set `flow.code_verifier` before `fetch_token()`. For localhost redirects during CLI exchange, set `OAUTHLIB_INSECURE_TRANSPORT=1` only for the token exchange command.

## Deleted/stale OAuth client pitfall

A saved pickle/token can fail with Google's `deleted_client` refresh error. Treat that as evidence that the OAuth client behind the token is gone or invalid; do not keep retrying the old token. The fix is to create/provide a replacement OAuth client, enable YouTube Data API v3 for that project, add the localhost redirect URI, and run a fresh user OAuth flow.

## Headless PKCE OAuth pitfall

`google-auth-oauthlib` may auto-generate a PKCE `code_verifier` when creating an auth URL for a web OAuth client. In a headless VPS flow, the auth URL and token exchange often run as separate CLI invocations. Persist the pending OAuth state **including** `state`, `redirect_uri`, `client_secret` path, `token` path, and `code_verifier` in a `0600` secrets file outside the repo, then restore `flow.code_verifier` before calling `fetch_token`. If the exchange fails with `InvalidGrantError: Missing code verifier`, regenerate a fresh auth URL after adding this persistence; old codes cannot be reused.

For localhost redirect URLs in CLI exchanges, set `OAUTHLIB_INSECURE_TRANSPORT=1` only for the exchange command/process so oauthlib accepts `http://localhost:5000/`.

## Trend-to-video loop

A minimal headless loop should:

1. Ingest trends from RSS/blog feeds, YouTube Data API public reads, curated channels, or manual prompts.
2. Score ideas by niche fit, recency, emotional hook, and feasibility for kinetic visuals.
3. Generate a short script in the channel tone.
4. Generate voiceover/TTS.
5. Render kinetic text/diagrams with ffmpeg or a small Python/Node renderer.
6. Export MP4 and verify with `ffprobe`/preview frames.
7. Upload as private using OAuth.
8. Record title, description, tags, source inputs, privacy status, and video ID in the dashboard/log.

## Discipline/self-improvement niche defaults

For a stoic masculine discipline channel, default to:

- Hooks around dopamine, focus, fatherlessness, food/weed discipline, no-college self-improvement, masculine responsibility, and first-gen ambition when consistent with the user's brand direction.
- Serious tone; avoid jokey captions unless requested.
- Strong but not fake certainty. Prefer practical scripts with a clear behavioral takeaway.
