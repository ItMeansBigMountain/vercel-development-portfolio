# Viral Radar queue drain, failover, and render fixes (2026-07)

Use this when draining Viral Radar rendered upload queues or creator clip-plan backlogs.

## User-corrected operating goal

If there is a Viral Radar queue/backlog of videos to clip or queued clips to upload, the goal is to finish uploading all of them, using configured failovers as needed. Do not reserve upload capacity for faceless/newsletter jobs while real Viral Radar clips remain.

Order of work:

1. Replay `UPLOAD_QUEUE` rendered clips first.
2. If queue is empty but clip plans remain, continue source acquisition → render → upload.
3. Stop only when the queue/backlog is empty or a real blocker is reached, such as all configured upload-capable accounts hitting YouTube daily upload limits or source acquisition requiring cookies/proxy/local source.

## Manual drain commands

Queue-size targeted drain:

```bash
q=$(find /opt/data/HeRmEz/projects/viral-clip-radar/UPLOAD_QUEUE -maxdepth 1 -name '*.upload.json' 2>/dev/null | wc -l)
FORCE_UPLOAD=1 \
VIRAL_RADAR_UPLOAD_QUEUE_FIRST=1 \
VIRAL_RADAR_MIN_UPLOADS="$q" \
VIRAL_RADAR_MAX_SOURCE_ATTEMPTS="$q" \
python3 /opt/data/scripts/viral_radar_daily_upload.py
```

Backlog/source drain:

```bash
FORCE_UPLOAD=1 \
VIRAL_RADAR_UPLOAD_QUEUE_FIRST=1 \
VIRAL_RADAR_MIN_UPLOADS=10 \
VIRAL_RADAR_MAX_SOURCE_ATTEMPTS=50 \
VIRAL_RADAR_DAILY_UPLOAD_CAP=100 \
python3 /opt/data/scripts/viral_radar_daily_upload.py
```

## Failover behavior to preserve

- Classical Echos first.
- Trapiistan/Sosai after Classical Echos upload-limit failure.
- fareed320 after Trapiistan/Sosai when active and verified.

Treat these as upload-limit markers that should trigger failover/queueing:

- `uploadLimitExceeded`
- `exceeded the number of videos`
- `daily upload limit`
- `quota exceeded for quota metric`
- `video uploads per day`
- `rateLimitExceeded`

If all configured accounts/projects hit upload limits, do not discard clips. Ensure the failed rendered clip and `.upload.json` stay in `UPLOAD_QUEUE` for retry after reset.

## Low-res vertical render fix

For already-vertical low-resolution sources such as `202x360`, scaling by height then cropping to `1080x1920` can fail because the scaled width remains too small. The renderer should scale-to-cover before crop:

```text
scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1
```

Use this instead of a simple `scale=-2:1920,crop=1080:1920` chain for mixed landscape/vertical sources.

## Verification pattern

After each run, check:

- `UPLOAD_QUEUE/*.upload.json` count
- `UPLOAD_QUEUE/*.mp4` count
- latest `UPLOADS/youtube_uploads.jsonl` URLs
- YouTube auth health if upload/auth behavior changed

A clean run with `UPLOAD_QUEUE` empty but clip plans still present means the next concrete step is another source→render→upload backlog run, not stopping.
