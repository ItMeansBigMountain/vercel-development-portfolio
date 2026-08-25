# Google TTS + stock visual fallback lessons — 2026-06

Use for the user's faceless/newsletter YouTube pipeline when ElevenLabs credits are low or AI video providers are unavailable.

## Durable workflow correction

The user's intended visual stack is **stock visuals**, not Higgsfield/Sora as a hard requirement:

1. Pexels stock video/images when `PEXELS_API_KEY` is configured.
2. Stock/manual fallback such as Mixkit-style downloaded clips when Pexels is unavailable.
3. Only use Higgsfield/Sora/text-to-video when the user explicitly asks or a specific video warrants it.

Do **not** block the newsletter/faceless quality gate just because Higgsfield is unauthenticated or AI video provider keys are missing if stock visuals are available.

## TTS fallback order

For this pipeline, use:

1. ElevenLabs when live probe succeeds and enough characters remain.
2. Google Cloud Text-to-Speech via `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_TTS_CREDENTIALS`.
3. Local `ffmpeg/flite` only as emergency/review fallback.

Google Cloud TTS smoke pattern:

- Use service-account credentials from `GOOGLE_APPLICATION_CREDENTIALS`/`GOOGLE_TTS_CREDENTIALS`.
- Request `https://texttospeech.googleapis.com/v1/text:synthesize` with an OAuth bearer token from `google.oauth2.service_account` and scope `https://www.googleapis.com/auth/cloud-platform`.
- Default voice used successfully: `en-US-Neural2-J`.
- Decode `audioContent` base64 and verify output bytes > 1000.

## ElevenLabs credit preservation

Before calling ElevenLabs for scene-by-scene narration, check `/v1/user/subscription` and compare remaining characters to `len(text) + reserve`.

- Default reserve used: `ELEVENLABS_MIN_REMAINING_CHARS=500`.
- If low, write a small marker such as `elevenlabs_skipped_low_credits.txt` and fall through to Google TTS.
- This prevents smoke tests from burning the final free-tier characters.

## Preflight behavior

Preflight should report these separately:

- ElevenLabs status and remaining/free-tier reset data.
- Google TTS status with voice and sample audio bytes.
- Stock visual provider status: `pexels` if key exists, otherwise `mixkit/manual-stock-fallback` when generic download tooling is available.
- AI video provider/Higgsfield status may be informational, but must not be a blocker for stock-first workflows.
