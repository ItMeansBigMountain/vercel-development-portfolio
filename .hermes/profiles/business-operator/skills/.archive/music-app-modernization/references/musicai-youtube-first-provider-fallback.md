# MusicAI YouTube-first provider fallback

Session learning: when Spotify and SoundCloud are blocked by account/subscription requirements, do not stall MusicAI modernization. Keep the one-account/multi-OAuth architecture, but make YouTube/YouTube Music the active provider and mark blocked providers as roadmap/TODO.

## Provider blockers observed

- Spotify OAuth redirect can be correct while the app still fails after code exchange because the Spotify app/account is in development-mode and API calls require Premium/allowlisted users. Treat this as an account/product-access blocker, not necessarily a code bug.
- SoundCloud API app registration/use may require SoundCloud Artist Pro / paid access. Do not push SoundCloud as the core MVP provider when the user does not want the subscription.
- YouTube OAuth worked and is a practical MVP source for playlists/video titles.

## Recommended product pivot

1. Landing page CTA should prefer `Connect YouTube / log in`.
2. Keep Spotify and SoundCloud provider cards in the hub, but label them `Roadmap` or equivalent, with blocker copy.
3. Dashboard should treat YouTube playlists as the primary music-taste source.
4. Use YouTube playlist metadata and sampled playlist item titles as a first-pass signal for vibe tags: chill, hype, nostalgic, romantic, focused, sad, discovery, etc.
5. Keep no-login lyric/text analyzer prominent as the low-friction demo.
6. Keep one-account/multi-provider token architecture intact so Spotify/SoundCloud can be enabled later without reworking identity.

## YouTube OAuth scope note

For playlist scanning, request YouTube scopes explicitly, e.g.:

```txt
openid email profile https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/youtube.force-ssl
```

Then call:

- `GET https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&mine=true&maxResults=...`
- `GET https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=...&maxResults=...`

Use token refresh/durable encrypted storage before real users.
