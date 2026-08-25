# Viral Radar strict discovered-source procedure (2026-07)

Session learning from repeated user corrections around Viral Radar uploads.

## Core rule

Viral Radar must not upload placeholders. It must not use NASA/JPL/space/Mars/Perseverance, `unknown` creators, evergreen filler, stock filler, old queue items, or unrelated fallback manifests to satisfy a minimum upload count.

The procedure is:

1. Discover videos from the defined creator/influencer watchlist via the Viral Radar data pipeline.
2. For each influencer video found in that pipeline run, clip that exact source video.
3. Create/upload at least 10 public Shorts for that exact influencer video; allow up to 50 if duration/transcript quality supports it.
4. If the exact source cannot be acquired/rendered/uploaded, report the blocker and/or queue that exact rendered clip. Do not substitute another source.
5. If YouTube returns `uploadLimitExceeded`, keep the failed real rendered clip + metadata in `UPLOAD_QUEUE` for retry, but do not let old/stale queued items satisfy a new discovered video's 10-clip minimum.

## Workflow details

- Discovery-triggered runs should process each discovered plan independently, not run one global candidate pool that can drift to an older manifest.
- Use strict mode/env defaults:
  - `VIRAL_RADAR_STRICT_DISCOVERED_ONLY=1`
  - `VIRAL_RADAR_UPLOAD_QUEUE_FIRST=0` for discovery-triggered new-source runs
  - `VIRAL_RADAR_MIN_UPLOADS=10`
  - `VIRAL_RADAR_MIN_CLIPS_PER_LONGFORM=10`
  - `VIRAL_RADAR_MAX_CLIPS_PER_SOURCE=50`
  - `VIRAL_RADAR_DAILY_UPLOAD_CAP=100` unless the user explicitly asks for conservative throttling
- Queue-first behavior is acceptable for a retry/resume job, but not for a new source discovery job where it would mask failure to clip the newly found video.
- When the user says to “look back” for not-successfully-uploaded videos, identify real creator source videos below 10 successful uploads, skip Shorts/placeholder sources that cannot produce 10 distinct clips, expand/render missing clips from the exact source, and queue/upload those exact clips.

## Pitfalls

- Do not describe a minimum as satisfied by unrelated uploads from the same day.
- Do not use old top-up scripts unless they explicitly skip placeholder/evergreen sources and preserve exact-source semantics.
- Do not keep retrying the same clip/title into the queue; dedupe queue entries by `(source_url, selected_hook, title)`.
- Do not publish internal planning labels such as “clip 1” or “the part people will replay.”
- Do not add hashtags to the title. Put `#Shorts`, `#ViralRadar`, and topic hashtags in description/tags based on the actual title/transcript/context.
