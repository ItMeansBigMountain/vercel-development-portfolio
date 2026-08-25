# Viral Radar metrics, title, and channel-routing lessons (2026-07)

Use this when maintaining Viral Radar cron prompts, upload scripts, or reporting.

## Metrics are for the growth loop, not vanity reporting

The metrics precheck should do more than prove OAuth works. Its output should feed the next content decisions:

- Identify which uploaded clips, creators, topics, and hook styles are winning.
- Prefer future source discovery and backlog selection toward recent winners.
- Avoid duplicate recent titles and avoid spending quota on repeatedly weak creator/topic patterns.
- Update `/opt/data/HeRmEz/projects/_ops/social-growth/PERFORMANCE_LEARNINGS.md` with concise learnings.
- Report operational health separately from content learning: e.g. OAuth status, video IDs seen, stats fetched, and blockers.

Current limitation: the usual YouTube Data API metrics cover surface stats like views/likes/comments. Retention/watch-time needs YouTube Analytics access to be wired and verified.

## Title rule: unique and true to the clip

Every public Viral Radar title must be:

- Unique across uploads.
- True/specific to the actual clip/source video/transcript.
- Catchy if the source supports it, but not misleading or disconnected.
- Free of hashtags; hashtags belong in description/tags.

Avoid using generic repeated titles as the whole title, such as:

- `The Uncomfortable Truth Hiding Here`
- `The Money Mistake That Looks Smart`
- `This Sounds Wrong Until It Clicks`

Those can be used only as a suffix/context phrase after a source-specific title, e.g. `Chris Williamson: Most Think Mastering Something — The Uncomfortable Truth Hiding Here`.

## Queue/backlog priority

If Viral Radar has rendered clips queued or a backlog of videos to clip, the operating goal is to finish uploading all queued real clips using the configured failovers until the queue is empty or a real YouTube/source blocker is reached. Do not reserve capacity for faceless/newsletter work while Viral Radar real clips remain.

## Discord channel routing

Viral Radar cron messages should deliver to the YouTube automation channel/session when the user asks for `#youtube-automation` routing. Use explicit `discord:<channel_id>` delivery for both:

- Creator discovery feeder for Viral Radar.
- Daily Viral Radar / Creator clip generation + upload.

Do not change Robinhood/trading cron routing as part of Viral Radar routing changes unless the user explicitly asks.