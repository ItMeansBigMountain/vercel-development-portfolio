# Viral Radar upload limits, queueing, and placeholder-source rules (2026-07)

Session learning from Viral Radar upload-limit testing and user corrections.

## YouTube upload limits: maximize but queue on block

- YouTube Data API docs list `videos.insert` in the Video Uploads quota bucket with a documented default ceiling of **100 upload calls/day**.
- YouTube can still return a separate channel/account upload blocker such as `The user has exceeded the number of videos they may upload` before/independent of visible Google Cloud quota.
- User preference for Viral Radar: **do not self-throttle based on a guessed lower cap**. Probe toward the documented 100/day limit and only stop when YouTube actually blocks/rate-limits the channel.
- When YouTube blocks, queue the rendered MP4 plus metadata for the next run instead of deleting it.
- Queue path: `/opt/data/HeRmEz/projects/viral-clip-radar/UPLOAD_QUEUE/`.
- Next run must upload queued clips first before rendering more.
- Include queue counts in reports: `queued_replay_uploaded_count`, `remaining_queue_count`, daily cap, uploaded count, and blocker details.

## Queue hygiene

- Queue metadata must preserve title, description, tags, privacy, creator, source URL/title, hook, and last upload error.
- Prevent duplicate queued items by signature: source URL + selected hook + title.
- If a duplicate failed render is already queued, delete only the duplicate local render and keep the existing queued item.

## Placeholder/filler source rule

User correction: **"stop uploading the space placeholders. upload the real thing or dont upload it"**.

For Viral Radar:

- Do not use NASA/JPL/space/Mars/Perseverance or other evergreen filler as a substitute for influencer content.
- Do not use `unknown` creator or generic evergreen placeholder clips to satisfy upload minimums.
- Upload real influencer/creator clips or report/queue/block; do not fill slots with placeholder material.
- Existing helper behavior should treat NASA, unknown, and old evergreen fallback creators as excluded unless the user explicitly sets an override such as `VIRAL_RADAR_ALLOW_EVERGREEN_FALLBACK=1`.

## Operational pattern

1. Upload queued clips first.
2. Generate/render real influencer clips only.
3. Upload as each clip is created.
4. If upload succeeds, log the returned video ID/URL and clean generated export.
5. If upload fails due to YouTube limit or other upload error, move MP4 + metadata into `UPLOAD_QUEUE/`.
6. Continue/probe until the documented cap or actual YouTube blocker is reached; never silently report success after placeholder uploads.
