# MusicAI selected provider stack

Session learning: the user explicitly narrowed MusicAI's streaming/provider roadmap.

## Selected providers for MusicAI

- Spotify — existing core provider; keep working, but no longer the product identity.
- Apple Music / MusicKit — desired provider; requires Apple Developer Team ID, Key ID, and MusicKit `.p8` private key.
- YouTube / YouTube Music — desired provider; use Google OAuth plus YouTube Data API v3.
- SoundCloud — desired provider; requires SoundCloud developer app/client credentials and may be approval-gated.

## Explicitly excluded for MusicAI

- Deezer — do not add provider cards, env vars, callbacks, roadmap steps, or setup instructions unless the user reverses this.
- Last.fm — do not add provider cards, env vars, callbacks, roadmap steps, or setup instructions unless the user reverses this.

## Required env/callback checklist

- Google/YouTube:
  - `GOOGLE_CLIENT_ID`
  - `GOOGLE_CLIENT_SECRET`
  - Callback: `/providers/youtube_music/callback`
- Apple Music:
  - `APPLE_TEAM_ID`
  - `APPLE_KEY_ID`
  - `APPLE_PRIVATE_KEY`
- SoundCloud:
  - `SOUNDCLOUD_CLIENT_ID`
  - `SOUNDCLOUD_CLIENT_SECRET`
  - Callback: `/providers/soundcloud/callback`

## Implementation pitfall

When editing MusicAI provider registry, homepage copy, health checks, env templates, docs, and deployment status, update all of them together so excluded providers do not reappear in the UI or key checklist.
