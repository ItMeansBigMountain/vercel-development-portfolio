# Viral Radar backlog cron conversion and specialist routing (2026-07)

Use this reference when repurposing an existing content backlog cron without mixing YouTube lanes.

## Safe in-place conversion

1. Inspect the existing job completely: name, prompt, skills, script, workdir, schedule, delivery, enabled state.
2. Keep the job ID and schedule unless the user asks otherwise; replace every lane-specific field.
3. Set the Viral Radar root explicitly and add a startup guard that requires its expected `CLIP_PLANS` and uploader paths.
4. Remove Gmail/newsletter/faceless skills and references. A string-level separation check should reject `faceless-youtube-channel`, `run_faceless_video.sh`, newsletter profile names, and newsletter processing.
5. Drain rendered `UPLOAD_QUEUE` first. If empty, process outstanding reviewed/discovered plans. Preserve queue items on failed uploads.
6. Use the common upload lock, normalized duplicate check, and registry-driven failover accounts. Do not implement a second independent uploader.
7. Report queue before/after, uploads/URLs, failover account used, and exact blocker.
8. Route the result to the YouTube automation Discord channel.
9. Enable the converted job only after shell syntax and separation checks pass. Re-list cron jobs and verify the separate faceless generation job is still paused.

## Known-good local shape

- Converted job: `f02334d43494`
- Wrapper: `/opt/data/scripts/viral_radar_backlog_drain.sh`
- Workdir: `/opt/data/HeRmEz/projects/viral-clip-radar`
- Runner: `/opt/data/scripts/viral_radar_daily_upload.py`
- Delivery: Discord YouTube automation channel
- Queue behavior: `VIRAL_RADAR_UPLOAD_QUEUE_FIRST=1`
- Source policy: `VIRAL_RADAR_STRICT_DISCOVERED_ONLY=1`

## Discord routing rule

General should receive only the daily stand-up/orchestrator report. Route social-video jobs to YouTube automation, trading jobs to trading, backups/dev jobs to coding, email/life jobs to personal, and red-team watchdogs to security/redteam. Re-list jobs after bulk updates; `origin` is not acceptable for specialist reports when it resolves to General.

## Auth watchdog UX

When a YouTube profile fails token refresh or channel verification, generate a fresh OAuth URL for that exact profile. Include the expected channel/account and callback format. Ask the user to return the full `http://localhost...` callback URL so it can be exchanged and verified. Keep secrets/tokens out of reports.
