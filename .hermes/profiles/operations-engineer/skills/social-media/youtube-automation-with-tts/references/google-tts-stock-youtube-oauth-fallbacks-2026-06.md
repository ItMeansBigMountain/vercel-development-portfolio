# Google TTS, stock visuals, and YouTube OAuth fallback lessons — 2026-06

Use this for the user's faceless/newsletter YouTube pipeline when ElevenLabs credits are low, visual providers are being checked, or YouTube channel OAuth scopes are being repaired.

## TTS fallback policy

- ElevenLabs remains preferred for final narration when credits are healthy.
- Probe ElevenLabs subscription before rendering long videos; if remaining credits are below the narration length plus a reserve, skip ElevenLabs rather than burning the last credits on tests.
- Google Cloud Text-to-Speech is the production fallback. In the current pipeline it uses `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_TTS_CREDENTIALS`, default voice `en-US-Neural2-J`, and the REST endpoint `https://texttospeech.googleapis.com/v1/text:synthesize` with a service-account access token.
- Keep local `ffmpeg/flite` as emergency/review-only fallback, not as final public narration unless explicitly approved.

## Stock visual provider policy

- Do not require Higgsfield/Sora/AI-video auth for the standard faceless/newsletter path.
- Primary visual path: Pexels when `PEXELS_API_KEY` is configured.
- Acceptable fallback: vetted stock/manual/Mixkit-style clips/images fetched or staged with ordinary tools such as `curl`, with a source manifest when possible.
- Quality gate should check for usable stock visuals, not an authenticated AI-video provider, unless the user explicitly asks for AI-generated B-roll.

## YouTube OAuth repair pattern

For channel upload/metadata/analytics readiness, request and verify this scope set together:

- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.force-ssl`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

Headless callback exchange may require `OAUTHLIB_INSECURE_TRANSPORT=1` when the redirect URL is `http://localhost:5000/...`.

After exchanging a callback, always verify channel identity with `channels().list(mine=true, part='id,snippet,statistics,status')` before declaring a lane ready. Token path names can be misleading: a "faceless" token may actually resolve to the Sosai Oyama channel if that was the selected YouTube identity during consent.

## Upload token routing pitfall

Shared upload helpers often default to a generic token path. Faceless-channel scripts should pass the intended token explicitly, e.g. `/opt/data/secrets/faceless-youtube-channel/youtube_upload_token.json`, so uploads do not silently route to the default/shared channel.
