# ClipCurrent / Viral Clip Radar — API vs Browser Strategy

Session context: user wanted to evaluate whether a clipping-platform project should be implemented as code using APIs or operated manually/browser-driven by Hermes with credentials.

## Durable takeaways

- Prefer a **code-first pipeline with human review** for any repeatable clipping operation.
- Use browser automation for account setup, dashboard validation, first-run experiments, and fallback tasks where an API is unavailable.
- Do not build the core workflow around browser clicking: it is brittle, slow, hard to audit, and poor for credential/state management.
- Keep publishing human-in-the-loop until clip quality, rights risk, and channel voice are proven.

## Recommended architecture

```text
trend collectors
  YouTube Data API / seed channels / X-social signal
        |
        v
candidate DB
  source URL, creator, duration, stats, topic, score, risk
        |
        v
scoring engine
  virality, view velocity, long-form fit, clip density, niche fit
        |
        v
clip job queue
  OpusClip API or alternate clipping backend
        |
        v
review dashboard
  approve/reject, titles, captions, attribution, risk notes
        |
        v
publishing queue
  YouTube Shorts/Reels/TikTok after approval
        |
        v
analytics feedback
```

## OpusClip API finding

The user suspected OpusClip might not have an API. Research found it does expose an API for automated clipping workflows.

Useful documented capabilities:

- create a clipping project from long-form video
- query generated clips
- brand templates
- social posting
- webhooks
- censor jobs
- credits: `1 credit = 1 minute` of video processing
- standard rate limit around `30 requests/minute`
- high input limits such as multi-hour / large video processing

## YouTube credential pattern

For public trend/video metadata, prefer a **YouTube Data API key**.

For authenticated channel actions such as uploads, private analytics, or managing a channel, plan for **user OAuth**. Google service-account JSONs can be useful for Google Cloud/Workspace automation, but YouTube channel operations are user-account centered.

When a service-account JSON is found, do not print key material. Report only safe metadata: path, project ID, service-account email, file mode, and whether a private key exists.

## Project documentation pattern

For this class of new product idea, create durable artifacts inside the project repo rather than only chatting:

- `PRODUCT_DIRECTION.md`
- `DATA_SOURCES.md`
- `EXECUTION_STRATEGY.md`
- `INBOX/candidates.csv`
- `TEMPLATES/clip_plan.md`
- `WORKFLOWS/clip_pipeline.md`

Recommended name from the session: **ClipCurrent** for the platform/tool, while the public channel name can be chosen by niche later.
