# Google Cloud Text-to-Speech fallback for faceless/newsletter videos

Use this when ElevenLabs free credits are low/exhausted or ElevenLabs TTS fails but the video pipeline still needs realistic-enough narration.

## When to use

- ElevenLabs `/v1/user/subscription` shows too few remaining characters for the planned narration.
- ElevenLabs returns 402/payment/limit/voice errors during rendering.
- The user has enabled Google Cloud Text-to-Speech and wants a free-tier/stable API fallback.

## Provider order for this user's pipeline

1. ElevenLabs for final premium narration when credits are available.
2. Google Cloud Text-to-Speech as the production fallback.
3. Local `ffmpeg`/`flite` only as an emergency/review fallback.

## Auth and configuration

Use service-account credentials via one of:

- `GOOGLE_APPLICATION_CREDENTIALS`
- `GOOGLE_TTS_CREDENTIALS`

Default voice used in the faceless channel renderer:

- `GOOGLE_TTS_LANGUAGE=en-US`
- `GOOGLE_TTS_VOICE=en-US-Neural2-J`
- optional: `GOOGLE_TTS_SPEAKING_RATE=1.0`
- optional: `GOOGLE_TTS_PITCH=0.0`

The direct REST endpoint is:

```text
POST https://texttospeech.googleapis.com/v1/text:synthesize
Authorization: Bearer <service-account access token>
Content-Type: application/json
```

Minimal payload:

```json
{
  "input": {"text": "Narration text"},
  "voice": {"languageCode": "en-US", "name": "en-US-Neural2-J"},
  "audioConfig": {"audioEncoding": "MP3", "speakingRate": 1.0, "pitch": 0.0}
}
```

The response returns base64 `audioContent`; decode it to `.mp3`.

## Live verification pattern

Before trusting setup, run a real synthesize call and verify decoded audio is over 1000 bytes. This session's smoke test succeeded with Google TTS enabled and produced ~23 KB for a short phrase.

## Pipeline integration notes

For `/opt/data/HeRmEz/projects/faceless-youtube-channel/scripts/run_graphic_video.py`, fallback order is:

```python
if not elevenlabs_tts(spoken, audio):
    if not google_tts(spoken, audio):
        audio = sd / f"{idx:02d}.wav"
        fallback_tts(spoken, audio)
```

For preflight, do not fail the TTS gate just because ElevenLabs is exhausted if Google TTS live synthesis succeeds. Report ElevenLabs and Google TTS separately.

## Pitfalls

- Enabling the API in the console is not enough; verify with a live synthesize request using the same credentials the renderer will use.
- Do not spend ElevenLabs characters during a fallback smoke test if the goal is to verify Google TTS specifically.
- Do not treat local `flite` output as production-quality narration; keep it emergency/review-only unless the user explicitly accepts it.
