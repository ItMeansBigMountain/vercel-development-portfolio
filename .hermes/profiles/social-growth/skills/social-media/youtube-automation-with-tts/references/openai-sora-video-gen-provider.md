# OpenAI Sora via Hermes video generation provider

Use this reference for the user's faceless/newsletter video pipeline when AI B-roll should come from OpenAI Sora instead of Higgsfield/FAL-first fallbacks.

## Core lesson

A ChatGPT subscription can expose Sora in the ChatGPT UI, but cron/Hermes automation needs programmatic API access. Prefer a Hermes `video_gen` provider plugin backed by `OPENAI_API_KEY` with OpenAI Videos/Sora API access.

Do not treat Higgsfield as the primary provider just because its CLI exists on the machine. For this user's pipeline:

1. Preferred: Hermes `video_generate` using `video_gen.provider: openai-sora`.
2. Fallbacks: FAL/Replicate/Runway/Pika/Luma/Comfy/Higgsfield only if OpenAI/Sora is unavailable or explicitly requested.

## Hermes plugin shape

Hermes video-generation providers live under:

```text
plugins/video_gen/<name>/
```

A Sora provider should:

- subclass `agent.video_gen_provider.VideoGenProvider`
- register in `register(ctx)` with `ctx.register_video_gen_provider(...)`
- expose provider name such as `openai-sora`
- implement text-to-video and optional first-frame image-to-video through OpenAI's Videos API
- return `success_response(video=<local mp4 path or URL>, model=..., provider='openai-sora', ...)`

Config:

```yaml
video_gen:
  provider: openai-sora
  model: sora-2
```

Enable the `video_gen` toolset and restart Hermes/gateway so plugin discovery happens.

## OpenAI Videos API flow

OpenAI's Sora Videos API is asynchronous:

1. `POST /v1/videos`
2. Poll `GET /v1/videos/{video_id}` until `status == completed`
3. Download `GET /v1/videos/{video_id}/content`
4. Save MP4 under Hermes cache or project video workspace

Useful model defaults:

- `sora-2` for fast iteration / social clips
- `sora-2-pro` for 1080p or production-quality clips

For Shorts, default to `9:16`, short durations, and prompt for the user's dark high-contrast particle/cinematic visual style.

## Preflight behavior

Newsletter video preflight should check for:

- ElevenLabs live TTS success (the user's key alias is `EllevenLabsKey`)
- `OPENAI_API_KEY` or equivalent OpenAI key with Videos/Sora API access
- YouTube uploader readiness

If `OPENAI_API_KEY` is absent, report the blocker as “need OpenAI API/Sora video access for cron automation,” not “Higgsfield unauthenticated.”
