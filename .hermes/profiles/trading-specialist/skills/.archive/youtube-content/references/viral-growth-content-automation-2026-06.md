# Viral Growth Content Automation Pattern — 2026-06

Use this when the user asks to make content automation projects more viral, choose upload timing/frequency, improve faceless YouTube visuals, or replace Opus Clip with cheaper/free API-driven tooling.

## Posting cadence defaults

Use audience local time. For this user's current US/Texas audience assumption, default to Central Time until analytics prove otherwise.

- YouTube Shorts: test 2–4 PM and 8–10 PM; 1 Short/day minimum during a 30-day sprint, 2/day only if quality stays high.
- TikTok: test 7–9 PM weekdays first; secondary tests 7–9 AM Tue/Thu/Fri and Saturday 3–5 PM.
- Instagram Reels: test 11 AM–1 PM and 7–9 PM; also test Wed 12 PM, Wed 6 PM, Thu 9 AM.
- Minimum viable consistency: 3–5 short-form posts/week; below that learning is too slow.
- Do not batch-dump several uploads at once. Schedule them into separate peak windows and, when possible, post when the user can reply to early comments.

## Viral loop to encode in projects

Automation should store and test:

- platform and intended local timezone,
- planned publish window/cohort,
- hook formula,
- source/attribution,
- privacy/draft state,
- upload ID/URL,
- cleanup status,
- analytics feedback for retention, shares, saves, comments, and repeatable audience language.

## Faceless YouTube graphics

Prefer cheap/free graphics that look intentional instead of generic AI stock footage:

- Kinetic typography with large 2–5 word hooks.
- Diagram scenes: ladders, meters, split screens, funnels, checklists, timelines, identity-conflict maps.
- Receipt overlays: calendar blocks, fake terminal/build logs, habit scorecards, food/weed/dopamine counters, job-search boards.
- Minimal faceless silhouettes/mascot motifs; avoid uncanny faces.
- Dark navy/black background, white text, cyan for systems, green for proof, orange/red for temptation/friction, yellow for wins.
- Pattern interrupts every 2–4 seconds; captions always burned in for silent autoplay.

## Free / API-friendly Opus-like stack

Prefer a code-first clipping/rendering pipeline over browser-only tools:

```text
source video
-> transcript or Whisper transcription
-> LLM/highlight scoring
-> clip_manifest.json
-> ffmpeg vertical render + burned captions
-> private/draft upload
-> cleanup generated media after returned platform ID/URL
```

Evaluate open-source candidates only if they clearly beat the existing pipeline:

- SupoClip-style self-hosted Opus alternatives.
- Vinci Clips-style AI clipping platforms with backend APIs.
- Smaller Whisper/caption CLI editors for captioning, not necessarily full production.
- Shotstack or similar developer video APIs only if local ffmpeg becomes a bottleneck or cloud/dashboard rendering is needed.

Native publishing preference:

- YouTube Data API: private upload baseline.
- TikTok Content Posting API: SELF_ONLY/draft first.
- Instagram Graph API: Reels after professional account and public video URL/resumable upload path exist.
- Broker APIs are fallback, not core, unless native setup is too slow and the broker proves reliable with returned IDs/status polling.

## Cleanup rule

After a successful upload returns a platform ID/URL:

1. Log the upload result first.
2. Delete only allowlisted generated assets: per-job `videos/<job>` workspaces, `EXPORTS/`, `TMP/`, `SOURCES/`, `DOWNLOADS/`, `RAW_VIDEO/`, scratch frames/audio.
3. Preserve source metadata, scripts, clip manifests, subtitles, upload logs, review notes, and attribution.
4. Provide `--keep-workspace`, `--keep-source`, or `--no-cleanup` escape hatches for debugging.

## Project update pattern

When applying this to existing projects, add a shared playbook/reference doc plus short pointers in each project README/workflow file. Then smoke-test with dry-run upload and script compilation rather than merely documenting the plan.