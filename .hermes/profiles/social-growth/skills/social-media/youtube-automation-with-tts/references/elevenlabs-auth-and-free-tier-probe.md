# ElevenLabs auth + free-tier probe

Use this when ElevenLabs returns `401 Unauthorized`, `missing_permissions`, or `402 Payment Required` during faceless video/TTS work.

## Durable lessons

- ElevenLabs API auth uses the exact HTTP header `xi-api-key`; do not use `Authorization: Bearer` for the REST calls used here.
- In this user's Hermes environment, prefer the env key alias `EllevenLabsKey` before older aliases (`ELEVENLABS_API_KEY`, `XI_API_KEY`, `ELEVEN_API_KEY`). Older aliases may exist with restricted scopes and can shadow the fresh key if checked first.
- Key presence is not readiness. Always run a live probe.
- A key can pass `/v1/models` but fail `/v1/user` with `missing_permissions`; use `/v1/user` or `/v1/user/subscription` when checking account readiness/credit state.
- `402 Payment Required` during TTS may be voice/model/plan related, even when auth is valid. Try a free-tier-friendly public voice and a current low-latency model before declaring auth broken.

## Recommended probe sequence

1. Load env and select key in this order:
   1. `EllevenLabsKey`
   2. `ELEVENLABS_API_KEY`
   3. `XI_API_KEY`
   4. `ELEVEN_API_KEY`
2. Probe:
   - `GET https://api.elevenlabs.io/v1/user`
   - `GET https://api.elevenlabs.io/v1/user/subscription`
   - `GET https://api.elevenlabs.io/v1/voices`
   - `GET https://api.elevenlabs.io/v1/models`
3. For a TTS smoke test, use `xi-api-key`, `Content-Type: application/json`, and `Accept: audio/mpeg`.
4. If configured voice fails, test a known free-tier-friendly voice such as `CwhRBWXzGAHq8TQ4Fs17` (Roger) with `eleven_flash_v2_5`.

## Minimal Python probe pattern

```python
import json, os, urllib.request, urllib.error

key = (os.getenv("EllevenLabsKey") or os.getenv("ELEVENLABS_API_KEY")
       or os.getenv("XI_API_KEY") or os.getenv("ELEVEN_API_KEY"))
headers = {"xi-api-key": key, "Content-Type": "application/json"}

for url in [
    "https://api.elevenlabs.io/v1/user",
    "https://api.elevenlabs.io/v1/user/subscription",
    "https://api.elevenlabs.io/v1/voices",
    "https://api.elevenlabs.io/v1/models",
]:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(url, "OK", r.status)
    except urllib.error.HTTPError as e:
        print(url, "HTTP", e.code, e.read().decode(errors="replace")[:300])

voice = "CwhRBWXzGAHq8TQ4Fs17"
payload = json.dumps({
    "text": "Hermes ElevenLabs smoke test passed.",
    "model_id": "eleven_flash_v2_5",
    "voice_settings": {"stability": 0.4, "similarity_boost": 0.75},
}).encode()
req = urllib.request.Request(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
    data=payload,
    headers=headers | {"Accept": "audio/mpeg"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=60) as r:
    audio = r.read()
print("tts bytes", len(audio))
```

## Code policy for renderers

- Use `EllevenLabsKey` first when selecting a key.
- Use `eleven_flash_v2_5` unless a higher-quality paid-plan model is verified live.
- Default/fallback to a known available free-tier voice if a legacy/default voice returns payment or voice access errors.
- Report auth, subscription, model/voice, and AI B-roll provider readiness separately. Do not collapse every ElevenLabs failure into “invalid key”.
