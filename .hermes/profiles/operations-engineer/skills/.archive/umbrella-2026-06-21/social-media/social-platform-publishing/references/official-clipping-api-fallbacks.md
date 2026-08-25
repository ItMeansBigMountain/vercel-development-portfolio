# Official clipping API fallbacks for YouTube source-acquisition blocks

Use this when a Viral Radar / Shorts pipeline cannot acquire source media because a VPS/headless downloader hits YouTube bot verification (`Sign in to confirm you’re not a bot`).

## Durable lesson

Do not keep retrying raw `yt-dlp` from the VPS as the default path. Treat direct YouTube downloading as an explicit opt-in fallback, not the normal automation route.

Preferred automation order:

1. **Local/owned source file first** — use an existing `SOURCES/.../*.mp4`, Google Drive file, S3/public MP4, or other permissioned direct media URL.
2. **Official clipping/import API next** — submit the YouTube/public video URL to a provider that officially supports URL import and returns rendered clips.
3. **Only then opt into direct downloader fallback** — require an explicit env/config flag such as `VIRAL_RADAR_ALLOW_DIRECT_YOUTUBE_DOWNLOAD=1`, plus cookies/proxy/PO-token support if appropriate.

## Providers verified as relevant

### OpusClip API

Docs show:

- Base URL: `https://api.opus.pro/api`
- Create project: `POST /clip-projects`
- Fetch clips: `GET /exportable-clips?q=findByProjectId&projectId=...`
- Auth: `Authorization: Bearer <API_KEY>`
- Optional org header for multi-org accounts: `x-opus-org-id: <ORG_ID>`
- Supports public imports from YouTube, Google Drive, Vimeo, Zoom, Rumble, Twitch, Facebook, LinkedIn, X, Dropbox, Riverside, Loom, Frame.io, Medal.tv, and public S3 MP4 links.

Implementation pattern:

- Submit `videoUrl` from the reviewed manifest.
- Add `renderPref.layoutAspectRatio = "portrait"`.
- If a human-reviewed clip window exists, pass curation range around that window.
- Persist provider job state under project `STATE/` so later cron runs can poll instead of duplicating jobs.
- Download `uriForExport`/export URL only after it exists, then upload via the normal YouTube uploader.

### Choppity API

Docs show:

- Base URL: `https://api2.choppity.com/v1`
- API-key auth header: `Authorization: Key <secret>-<teamId>`
- Supports public URL input, local uploads up to 5GB via presigned upload, AI clip generation, full-quality MP4 rendering, and webhooks.
- Webhook events include `asset.analysis.succeeded`, `asset.analysis.failed`, `project.render.succeeded`, `project.render.failed`, `post.published`, `post.scheduled`, and `post.failed`.

Implementation pattern:

- Use Choppity for URL/upload-driven clipping when OpusClip is unavailable or unsuitable.
- Prefer webhook/poll state over long blocking cron runs.
- Verify exact endpoint names from the user’s account docs before spending credits.

## Pipeline patch pattern

For a daily upload script:

- Add an `external_clip_provider.py` helper.
- Load env keys without printing values.
- Provider priority should be configurable, e.g. `VIRAL_RADAR_SOURCE_PROVIDER=opus,choppity`.
- Direct downloader fallback should be guarded by an explicit flag, e.g. `VIRAL_RADAR_ALLOW_DIRECT_YOUTUBE_DOWNLOAD=1`.
- If the provider returns a completed MP4, pass that MP4 into the normal upload function.
- If the provider submits a job but no MP4 is ready, report `pending` with a state file path; do not claim upload success.
- If no provider key is configured, report the missing provider config as the active blocker.

## Reporting pattern

Keep Discord reports short:

- “I disabled direct VPS YouTube downloading by default.”
- “Current source path is official provider import: OpusClip → Choppity.”
- “Next blocker: set `OPUS_CLIP_API_KEY` or `CHOPPITY_API_KEY/CHOPPITY_KEY`.”
- “Direct downloader only runs if explicitly enabled with `VIRAL_RADAR_ALLOW_DIRECT_YOUTUBE_DOWNLOAD=1`.”

Do not describe the bot-verification issue as Hermes or Discord being considered a bot. The blocked step is specifically public video URL → source media acquisition.
