# HeRmEz Shared YouTube Upload Method (2026-06)

Session learning: the user wants this OAuth pattern treated as the canonical way Hermes uploads to YouTube across multiple automation projects.

## Canonical pattern

Use **user OAuth**, not service accounts, for YouTube channel uploads.

Shared project-level docs/scripts created in the HeRmEz workspace:

```text
/opt/data/HeRmEz/projects/_ops/youtube-automation/YOUTUBE_UPLOAD_METHOD.md
/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/youtube_oauth.py
/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py
```

Canonical secrets path:

```text
/opt/data/secrets/youtube-main/youtube_client_secret.json
/opt/data/secrets/youtube-main/youtube_upload_token.json
/opt/data/secrets/youtube-main/youtube_oauth_pending.json
```

## OAuth setup checklist

1. Google Cloud Console → OAuth Client ID → **Web application**.
2. Enable **YouTube Data API v3**.
3. Add redirect URI:

```text
http://localhost:5000/
```

4. Generate auth URL from the helper.
5. User opens it and pastes the full returned `http://localhost:5000/?code=...` URL.
6. Exchange with localhost HTTP allowed only for that process:

```bash
OAUTHLIB_INSECURE_TRANSPORT=1 python3 youtube_oauth.py exchange 'FULL_LOCALHOST_URL'
```

7. Verify with `youtube_oauth.py check`.
8. Upload public by default with `upload_youtube.py` for approved automation lanes; use private/unlisted only when the user explicitly requests review mode or when YouTube/API compliance forces it.

## Headless PKCE pitfall

For web OAuth clients, `google-auth-oauthlib` can generate a PKCE `code_verifier` during auth URL creation. In headless VPS workflows, auth URL generation and token exchange often happen in different CLI processes. Persist the pending OAuth state including:

- `state`
- `redirect_uri`
- client secret path
- token path
- `code_verifier`

Restore `flow.code_verifier` before `fetch_token()`. If the exchange fails with `InvalidGrantError: Missing code verifier`, regenerate a new auth URL after adding this persistence; old auth codes cannot be reused.

## Visibility rule

Current user preference: **do not upload YouTube automation videos as private by default.** For the user's approved automation lanes, especially faceless newsletter videos and Viral Clip Radar, upload as `public` unless the user explicitly asks for `private`, `unlisted`, or a scheduled YouTube `publishAt` release.

Daily faceless Shorts and Viral Clip Radar cron uploads should use `--privacy public` and still keep cleanup gated on a returned YouTube video ID.

Do not wait for per-upload approval for approved automation lanes. Produce the artifact, upload it publicly, log the result, and report the video ID/URL.

## Scheduled backlog release rule

Current user preference is **not** to upload backlog videos as private. Prefer immediate `--privacy public` uploads for approved backlog items. If the user explicitly asks for YouTube scheduled release via `publishAt`, note that YouTube's API requires `status.privacyStatus=private` with `publishAt` until release time; otherwise avoid `publishAt` and use Calendar/cron scheduling to upload publicly at the target time. Log each upload in the lane's `UPLOADS/youtube_uploads.jsonl`, delete generated media only after the returned video ID, and update Google Calendar with release/upload timing.

## Shorts classification checklist

Official docs do **not** expose a separate `youtube.shorts.insert` endpoint or a `shorts=true` flag in the YouTube Data API. Upload Shorts through the normal YouTube Data API `videos.insert` endpoint with OAuth scope `https://www.googleapis.com/auth/youtube.upload`, `part=snippet,status`, and a regular video resource. YouTube classifies qualifying videos as Shorts based on the file/metadata. Keep our lane default as: 9:16 or square/taller-than-wide video, 3 minutes or less, `#Shorts` in title/description, `private` or scheduled-private first. Google documents that Shorts up to three minutes can be uploaded via YouTube Studio/app; for 1-3 minute Shorts, any active Content ID claim can globally block the Short, so prefer claim-safe/royalty-free audio and transformed source material.

For YouTube Shorts lanes, do not just upload a small/vertical-looking video. Verify the rendered MP4 before upload:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,duration,sample_aspect_ratio,display_aspect_ratio,pix_fmt,r_frame_rate \
  -of json EXPORT.mp4
```

Required: `1080x1920`, `display_aspect_ratio=9:16`, `sample_aspect_ratio=1:1`, `pix_fmt=yuv420p`, normal frame rate such as 30fps, and duration under YouTube's Shorts limit. The render filter should force square pixels, e.g. `scale=-2:1920,crop=1080:1920,setsar=1`, and encode with `-pix_fmt yuv420p`.

When uploading Shorts, include `#Shorts` in the title or description and a `shorts` tag. Avoid angle brackets like `<60` or `<=60` in YouTube descriptions; the API can reject them as `invalidDescription`.

## Production-over-setup rule

For this user's YouTube automation lanes, setup is not considered done until at least one real/private pilot artifact has been rendered and uploaded. After OAuth and scripts are working, keep iterating toward actual content output rather than stopping at docs, stubs, or plans.

Minimum proof for a lane:

- exported MP4 exists,
- private YouTube upload succeeded,
- returned video ID/URL is reported,
- metadata is appended to the lane's `UPLOADS/youtube_uploads.jsonl`.

## Project lanes recorded in HeRmEz

The workspace portfolio doc is:

```text
/opt/data/HeRmEz/projects/YOUTUBE_AUTOMATION_PORTFOLIO.md
```

Current lanes:

- `faceless-youtube-channel`: newsletter email → script → ElevenLabs voice → Pexels/Hugging Face visuals → public YouTube/social upload; do not default to private.
- `viral-clip-radar`: transformative creator-video clipping/radar lane; scout long-form creators such as Andrew Huberman, clip the source video, render full-frame 1080x1920 9:16 square-pixel MP4s with transcription/captions, and upload public unless private/unlisted review is explicitly requested. Do **not** add stock footage by default; this lane clips source videos.
- `youtube-high-ticket-leverage`: personal story/authority/future offer channel; can use shared headless text-video renderer for origin drafts.
- `tweet_video_generator`: active repair lane, not just archive. Route final `output.mp4` through the canonical shared public uploader unless a private/unlisted review mode is explicitly requested; remove hardcoded Twitter/X credentials in favor of environment variables.

## Canonical pilot upload evidence from the setup session

Known-good private upload IDs from the initial consolidation session:

- Faceless YouTube Channel: `gSghO62fL5M`
- Viral Clip Radar: `lLDXJIZQEqo`
- YouTube High-Ticket Leverage: `tohDKZndsvk`
- tweet_video_generator: `BEV1F-jo0Hc`

Treat these as verification that the shared OAuth token and uploader worked at least once; for future sessions, still run a fresh smoke test or inspect the latest upload log before assuming current readiness.
