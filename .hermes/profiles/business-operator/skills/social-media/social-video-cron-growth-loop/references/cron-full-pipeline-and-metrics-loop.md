# Cron full-pipeline + metrics loop reference

Use this reference when converting social-video cron jobs from simple upload scripts into full research → asset generation → render → publish → learn pipelines.

## Pattern learned

Script-only cron (`no_agent=true`) is good for deterministic watchdogs, but it is the wrong shape when every run must make creative decisions. For content generation, update the cron job to `no_agent=false`, attach the relevant skills, enable at least `web`, `terminal`, and `file`, and make the prompt self-contained.

## Faceless/video quality pause rule

If a video cron has produced low-quality/static/generic uploads, pause it immediately and keep it paused until one manually reviewed sample proves the full path works: realistic voice, relevant B-roll, clean public metadata, upload verification, and safe cleanup. Do not resume a daily social-video cron just because OAuth works or a renderer script exits successfully.

The job prompt should require:

1. Run the metrics monitor first.
2. Read the persistent performance learnings file.
3. Research current content opportunity.
4. Pick a fresh hook/topic, checking upload logs for duplicates.
5. Run the deterministic render/upload script with explicit env vars.
6. Verify real upload JSON contains a platform ID/URL.
7. Report concise result with blocker if upload failed.

## Local implementation pattern

Metrics loop:

```bash
python3 /opt/data/scripts/youtube_metrics_monitor.py --json
```

Performance file:

```text
/opt/data/HeRmEz/projects/_ops/social-growth/PERFORMANCE_LEARNINGS.md
```

Faceless fresh-topic upload:

```bash
FACELESS_TOPIC='<researched topic/hook>' \
FACELESS_RESEARCH_JSON='<compact JSON research brief>' \
FORCE_UPLOAD=1 \
python3 /opt/data/scripts/faceless_daily_upload.py
```

Viral Radar fresh reviewed-clip upload:

```bash
FORCE_UPLOAD=1 python3 /opt/data/scripts/viral_radar_daily_upload.py
```

## Scheduling defaults

Use Central Time for this user's Texas/US audience until analytics prove otherwise.

- YouTube Shorts primary windows: **2–4 PM CT** and **8–10 PM CT**.
- TikTok cross-posting reference: **7–9 PM weekdays**.
- Instagram Reels reference: **11 AM–1 PM** and **7–9 PM**.

Split multiple channels across different high-signal windows so they are not competing for the same slot.

## Monitoring caveat

Live YouTube metrics should be fetched with the OAuth token/account that uploaded the video, not a generic cross-account API key. The YouTube Data API is already enabled for the user's current lane; if token access fails, the monitor should still parse upload logs and write a setup note, but future agents must not interpret missing live metrics as content failure.

## Duplicate guard

Content cron scripts should avoid public duplicates by default. If no fresh reviewed clips/assets exist, report the blocker and produce a research/discovery note instead of reposting the same public Short. Only allow duplicates behind an explicit env override such as `VIRAL_RADAR_ALLOW_DUPLICATE=1`.

## Upload verification rule

Do not say a video posted unless the upload script returned a real video ID/URL. If the script failed, report the stage plus stdout/stderr/error tail.