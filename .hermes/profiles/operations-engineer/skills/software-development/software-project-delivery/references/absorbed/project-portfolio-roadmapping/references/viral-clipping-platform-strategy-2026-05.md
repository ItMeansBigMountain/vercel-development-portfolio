# Viral Clipping Platform Strategy — 2026-05

Use this reference when the user wants to build a project around discovering viral long-form videos, clipping them into shorts, and operating a separate clipping channel from their personal/high-ticket channel.

## Core product distinction

Separate the clipping engine/channel from the personal high-ticket YouTube channel:

```text
personal high-ticket channel = original story, authority, trust, offer leverage
viral clipping channel/tool = trend arbitrage, source discovery, clip production experiments
```

## Recommended execution strategy

Prefer a **code-first API platform with human review** over a browser-clicking-only workflow.

```text
YouTube Data API / seed channels
  -> candidate scoring
  -> transcript + metadata analysis
  -> OpusClip API or alternate clipping API
  -> clip review queue
  -> manual approval / edits
  -> scheduled publishing
  -> performance feedback loop
```

Use browser automation as a fallback for account setup, dashboard validation, UI-only tools, visual QA, or first-pass MVP validation — not as the durable production engine.

## Why code-first wins

- Repeatable and schedulable.
- Can score/filter before spending clipping credits.
- Safer credential handling through env vars/secrets instead of logged-in browser state.
- Scales from a few videos to many candidates/day.
- Easier to maintain state: candidate DB, job queue, clip status, approvals, publish log, analytics.
- Can evolve into an internal tool or SaaS.

## Browser/operator workflow tradeoffs

Browser control is useful for early experiments and non-API services, but is brittle for production:

- Captchas/2FA/session expiry interrupt automation.
- UI changes break flows.
- Slow for high-volume recurring work.
- Harder to track state and errors.
- Higher credential/session risk.

## OpusClip API notes

OpusClip has an API suitable for a clipping backend. Public docs observed in this session described:

- create clipping projects from long-form videos
- query generated clips
- brand templates
- social posting
- webhooks
- censor jobs
- `1 credit = 1 minute` of video processing
- standard rate limit around `30 requests/minute/API key`
- max video limits around `10 hours` / `30GB`
- up to `50` simultaneous running projects

Always verify current pricing/access before implementation because API availability and plan restrictions can change.

## MVP build order

1. Pick working project/tool name; suggested name was **ClipCurrent**.
2. Add YouTube API key and fetch trending videos by region/category.
3. Add seed creator/channel list and scan latest long-form uploads.
4. Store candidates in SQLite with source URL, creator, topic, duration, stats, score, and risk notes.
5. Generate a daily top-candidates report.
6. Add OpusClip API integration for one approved video.
7. Add webhook/polling for completed clip jobs.
8. Add a review dashboard/queue.
9. Delay auto-publishing until the workflow proves quality and risk controls.

## Human-in-the-loop rule

Automate discovery, scoring, clipping, and draft metadata. Keep manual approval for:

- final clip selection
- misleading-context checks
- copyright/takedown risk judgment
- channel voice/titles/captions
- publish decisions

## Naming options

Recommended platform/tool name: **ClipCurrent**.

Other viable names:

- TrendSlicer
- ViralForge
- SignalClips
- HookMill
- CurrentCuts
- Viraloop
- ClipRadar
