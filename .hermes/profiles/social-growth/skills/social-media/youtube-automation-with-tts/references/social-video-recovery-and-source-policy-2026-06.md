# Social video recovery and source policy — 2026-06

Use this when the user says to complete stopped social/video jobs, replay failed newsletter runs, or fix Viral Radar after auth/source failures.

## Durable lessons

- Distinguish **auth/upload** from **source acquisition**. A YouTube OAuth token can verify uploads/metrics while `yt-dlp` still fails because YouTube wants browser cookies or a non-cloud IP.
- If the user explicitly says not to use paid clipping/provider keys, do not keep surfacing missing `OPUS_CLIP_API_KEY`, `CHOPPITY_API_KEY`, `VIZARD_API_KEY`, `KLAP_API_KEY`, or `MUAPI_API_KEY` as the main blocker. Disable external-provider fallback by default and report `blocked_source` with allowed fixes: cookies, residential proxy, local/Drive MP4, or direct official source URL.
- When replaying newsletter backlog after script fixes, avoid leaving cron jobs concurrently producing duplicate uploads. Check/stop active manual and cron runs before bulk upload, then verify the upload log and trash only the source emails with returned `video_id`s.
- If a user corrects a creator source as wrong, remove it from the active watchlist and quarantine existing generated clip plans so the selector cannot keep choosing stale plans.

## Operational pattern

1. Inventory paused/stopped social jobs with `cronjob list`.
2. Repair auth first and verify with metrics/upload-token probes.
3. Run newsletter backlog separately from Viral Radar:
   - Newsletter lane can use stock visuals + approved TTS fallback.
   - Viral Radar needs actual creator source media and must not fall back to stock footage for creator clipping.
4. For newsletter upload scripts launched as subprocesses, use the same Python environment that has Google API dependencies; prefer `sys.executable`/the active venv over bare `python3`.
5. For optional local TTS fallback, resolve `edge-tts` via `shutil.which('edge-tts')` or the active venv path rather than assuming it is on PATH.
6. After verified YouTube uploads, trash only the corresponding Gmail source messages.
7. For Viral Radar source failures, run the hardened downloader first; if it still returns bot/sign-in checks and provider keys are out of scope, stop with `blocked_source` rather than looping provider-key advice.

## Reporting style

Keep the report short:

- what was fixed;
- exact uploaded URLs/video IDs;
- which emails were trashed after upload;
- which crons remain paused and why;
- next required input for blocked source acquisition.
