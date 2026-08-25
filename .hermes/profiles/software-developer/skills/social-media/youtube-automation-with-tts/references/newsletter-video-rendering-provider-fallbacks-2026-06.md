# Newsletter video rendering provider fallbacks (2026-06)

Use this when operating the user's Classical Echos / faceless newsletter pipeline after the 2-minute quality correction.

## Current quality bar

- Classical Echos newsletter videos are not quick Shorts placeholders by default.
- Target **~120 seconds** per email-derived video; minimum quality gate: **110 seconds**.
- Use **multiple relevant stock clips** matched to the narration, normally **6+ distinct visual segments** and preferably ~10 for a 2-minute render.
- Do not upload one-clip videos, black-screen fallbacks, static text slides, or generic filler that does not follow the script beats.
- Source emails are trashed only after a verified YouTube upload ID is returned.

## Provider sequence

1. **ElevenLabs voice first** for final channel uploads.
   - Use env aliases in this order: `EllevenLabsKey`, `ELEVENLABS_API_KEY`, `XI_API_KEY`, `ELEVEN_API_KEY`.
   - Probe `/v1/user` and `/v1/user/subscription` when 401/402/quota errors appear; key presence alone is not readiness.
   - If the ElevenLabs account is near character limit, stop or produce review-only renders; do not silently upload lower-quality TTS as final.

2. **Pexels stock video first** for visuals when the key is valid.
   - Live-probe the API before a batch render.
   - If Pexels returns 401/403/quota failures, treat that as provider unavailability for the batch and switch to a vetted fallback rather than rendering black placeholders.

3. **Mixkit free stock-video fallback** is acceptable for review/final renders when Pexels is blocked, provided clips are relevant and license constraints are respected.
   - Mixkit pages may block default Python user agents; fetch with a browser-like `User-Agent`.
   - Extract direct MP4 URLs from page HTML, e.g. `https://assets.mixkit.co/videos/.../...-720.mp4`.
   - Useful category pages include datacenter, information-technology, artificial, robots, coding, hacker, internet, stock-market, investment, finance, gym, fitness, workout, running, statue, ancient, sunrise, and meditation.

4. **edge-tts fallback** may be used for local review builds only.
   - Label output clearly as review-only.
   - Do not upload edge-tts renders as final Classical Echos channel content unless the user explicitly approves the voice quality.

## Batch discipline

- Run render-only first (`--no-upload --keep-workspace`) when changing providers, duration, or script logic.
- Produce a manifest of final MP4s with duration, size, subject, and workspace path.
- Generate a contact sheet of preview frames for rapid visual review when many videos are rendered.
- Deduplicate repeated renders for the same email in the clean manifest; prefer ElevenLabs versions over review-fallback versions.
- Keep upload crons paused or in render-only mode if the final quality gate is not met.
