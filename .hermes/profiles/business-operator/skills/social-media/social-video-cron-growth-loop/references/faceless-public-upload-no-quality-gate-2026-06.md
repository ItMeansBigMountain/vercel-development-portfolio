# Faceless/newsletter public-upload policy — 2026-06

Use this when operating the user's faceless newsletter/video upload lanes.

## User correction captured

The user explicitly corrected the prior rule that public upload only happens after quality gates pass. Current policy:

- Always upload generated faceless/newsletter videos as **public** by default.
- Do **not** block upload on subjective/production quality gates, review gates, missing premium providers, or imperfect media checks.
- Former gates may emit warnings for diagnostics, but they should not stop render/upload.
- Keep the cleanup safety boundary: source/newsletter emails are trashed only after YouTube returns a verified `video_id` and upload logging succeeds.

## Implementation pattern

- Upload commands should pass `--privacy public`.
- Provider readiness or visual/audio/dimension checks should warn rather than `raise`/`SystemExit` when the output can still be uploaded.
- Avoid final reports like “not uploaded because quality gates did not pass” for this lane. Report public upload status or the true hard blocker, such as auth failure, source unavailable, render crash, or YouTube API rejection.

## Known project files updated in the session

- `/opt/data/HeRmEz/projects/faceless-youtube-channel/scripts/run_trend_video.py`
- `/opt/data/HeRmEz/projects/faceless-youtube-channel/scripts/newsletter_batch_upload.py`
- `/opt/data/HeRmEz/projects/faceless-youtube-channel/docs/newsletter-video-quality-standard.md`
