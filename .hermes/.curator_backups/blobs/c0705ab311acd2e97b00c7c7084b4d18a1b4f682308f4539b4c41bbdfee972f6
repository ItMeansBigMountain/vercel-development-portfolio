# Viral Radar Google API + source acquisition fallback pattern — 2026-06

Use this for the user's Viral Radar creator-clipping lane when building daily automated Shorts from influencer long-form videos.

## Durable workflow

- Discover latest long-form candidate videos with Google/YouTube Data API through the channel's OAuth token, not scraping. This avoids yt-dlp bot checks during discovery and preserves channel/account identity.
- Store durable candidate state under the project, usually `CLIP_PLANS/*/source_metadata.json`, `clip_manifest.json`, and `edit_notes.md`.
- Select a fresh manifest/clip at run time; do not raw-reupload. Every clip needs vertical framing plus hook/context/captions or overlay framing and source attribution.
- Upload with the intended YouTube account's OAuth token explicitly. For the current Viral Radar influencer lane, the user asked for Classical Echos uploads, so use `/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json` unless they override it.
- Metrics should be fetched with the same OAuth account/token that uploaded the video.

## Source acquisition fallback order

1. Reuse an existing source file in the project cache if present.
2. Use `fallback_source_url` / direct media URL if the manifest has one.
3. Try the project downloader with yt-dlp, PO-token/bgutil support, and explicit logs.
4. Try a verified Opus Clips/API export only if credentials and an actual API/export contract are configured.
5. If all source paths fail, stop safely and report the exact stage, source URL, and log path. Never claim upload success without a returned YouTube `video_id`.

## Known cloud-IP pitfall and fix pattern

On VPS/cloud IPs, YouTube source downloads may fail with bot checks. Do **not** encode this as “YouTube download is impossible.” The fix is one of:

- provide a logged-in `youtube-cookies.txt` and pass it to yt-dlp;
- use a residential proxy;
- use a rights-safe direct source/mirror URL;
- use a real Opus Clips export/API path;
- upload source MP4s to Google Drive and pull them via Google Drive API.

The lesson is the fallback ladder and truthful blocker reporting, not that the downloader is permanently broken.

## Reset/persistence rule

Document the active pipeline in the project `WORKFLOWS/` directory and keep cron prompts self-contained. Future runs should be able to recover from reset using:

- cron job config;
- project `CONFIG/watchlist_channels.json`;
- project `CLIP_PLANS/` manifests;
- upload logs;
- workflow docs.
