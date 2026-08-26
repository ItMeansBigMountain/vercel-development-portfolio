# Viral Radar creator long-form release lane — 2026-06

Use this reference when the user asks to turn long-form creator/influencer videos into scheduled Viral Radar Shorts.

## Current release contract

- Release cadence: daily at **12:15 PM Central**.
- Cron expression in UTC during CDT: `15 17 * * *`.
- Primary cron job: `bce8ebabac36` / `Daily Viral Radar / Creator clip generation + upload`.
- Project: `/opt/data/HeRmEz/projects/viral-clip-radar`.
- Daily uploader script: `/opt/data/scripts/viral_radar_daily_upload.py`.
- Metrics preflight: `/opt/data/scripts/youtube_metrics_monitor.py --json`.

## Creator pool

The current Viral Radar creator pool includes:

- Andrew Huberman
- Chris Williamson
- Greg O'Gallagher / Kinobody
- Andrew Tate / TateSpeech / Cobratate
- GG33
- Luke Belmar / Capital Club
- Nate Belmar / Mr Belmar
- Alex Hormozi
- Hamza / Hamza Unfiltered

Treat all creator sources as source material for transformative clips, not raw reuploads.

## Discovery and seeding pattern

When expanding or refreshing the queue:

1. Use the YouTube Data API with the lane's OAuth token to discover recent long-form videos. This avoids relying on `yt-dlp` for metadata, which is more likely to hit cloud-IP bot checks.
2. Seed one or more `clip_manifest.json` files under `CLIP_PLANS/<date>-<creator>-<title>-<video_id>/`.
3. Include `source_metadata.json` and `edit_notes.md` with source attribution, duration, status, and the transformative standard.
4. Use conservative candidate clip windows inside the body of the video; do not pretend timestamps are human-reviewed unless they were reviewed.
5. Keep each manifest's `source_file` under project disposable source folders such as `SOURCES/<video_id>/source.mp4`.

Local seeding helper created for this lane:

```bash
python3 /opt/data/HeRmEz/projects/viral-clip-radar/scripts/seed_latest_longform_manifests.py --clips-per-video 2 --max-videos-per-channel 50
```

If a creator's official uploads playlist is missing or has no recent long-form videos, use a YouTube Data API search fallback and mark the manifest as search-fallback seeded.

When YouTube source downloads hit cloud-IP bot checks, use human-style web discovery before giving up: search for official creator reposts on Facebook/LinkedIn/owned sites, prefer official Facebook video URLs when available, and download those with yt-dlp into `SOURCES/<creator-source>/source.mp4`. Then seed a normal `clip_manifest.json` with `source_url` pointing to the official repost and `source_file` pointing to the local MP4. This worked for Alex Hormozi official Facebook and Kinobody official Facebook without Google cookies.

## Daily upload behavior

The daily uploader should:

1. Pick the next fresh unuploaded manifest clip.
2. Download or restore source media.
3. Render a 1080x1920 Short with hook/context overlay and captions when available.
4. Upload public using the correct YouTube upload token/account.
5. Log the returned YouTube ID/URL before cleanup.
6. Clean generated media only after verified upload.

## Pitfalls

- Do not revive the old NASA-only evergreen default unless no creator manifests exist and the user explicitly wants that fallback.
- Do not report a release as successful unless YouTube returned a real video ID/URL.
- If YouTube source download hits bot checks, report the exact blocker and log path; do not invent a replacement upload.
- Metrics must be fetched from the same OAuth account/token that uploaded the video.
- Auto-seeded clip windows are candidates, not human-reviewed quote selections; label them accordingly until review/transcript work happens.
