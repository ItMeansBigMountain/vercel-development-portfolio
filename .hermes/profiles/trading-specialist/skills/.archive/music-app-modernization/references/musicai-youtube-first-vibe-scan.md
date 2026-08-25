# MusicAI YouTube-first vibe scan pivot

## Context

During MusicAI modernization, Spotify login reached the callback but Spotify API calls were blocked by the app/account requiring Premium/dev-mode setup. SoundCloud API setup also required paid SoundCloud/Artist Pro access. The user chose to park both as future TODO connectors and make YouTube/YouTube Music the working core.

## Product direction

- Keep the one-account/multi-provider architecture.
- Make YouTube / YouTube Music the primary active provider when Google OAuth works.
- Label Spotify as `Roadmap` / future connector until Premium/dev-mode/tester requirements are worth solving.
- Label SoundCloud as `Roadmap` / future connector until paid API access is approved.
- Preserve no-login lyric/text analyzer as a fallback hook and demo path.

## Implementation pattern

1. Landing page CTA should point to `/providers/youtube_music/connect`, not Spotify.
2. Provider cards can still show Spotify/SoundCloud, but copy should make them future architecture, not current blockers.
3. Dashboard snapshot should prefer YouTube tokens over Spotify tokens when both exist.
4. Use YouTube Data API with OAuth token:
   - `GET https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&mine=true&maxResults=...`
   - For samples: `GET https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=...&maxResults=...`
5. Convert playlist names, descriptions, and sample video titles into a first-pass vibe profile.
6. Keep this honest as a lightweight MVP: title/description-based mood inference is useful for initial product feel, but deeper taste analysis should later add MusicBrainz/lyrics/audio features or richer metadata.

## Vibe inference starter buckets

Useful first-pass labels:

- `chill`: chill, lofi, sleep, calm, relax, rain, ambient, soft
- `hype`: hype, gym, workout, rage, party, turn up, bass, trap
- `nostalgic`: old, throwback, classic, nostalgia, retro, 90s, 2000s
- `romantic`: love, heart, r&b, slow jam, valentine, crush
- `focused`: study, focus, coding, work, deep, instrumental
- `sad`: sad, cry, heartbreak, alone, melancholy, breakup
- `discovery`: new, mix, indie, underground, discover, fresh

Fallback tags if nothing matches: `eclectic`, `playlist-led`, `video-native`.

## Pitfalls

- Do not keep pushing Spotify as the first CTA when Premium/dev-mode API access is the blocker.
- Do not tell the user to pay for SoundCloud just to keep parity; park it as roadmap unless they explicitly approve paid API access.
- When YouTube becomes primary, update homepage copy, dashboard labels, README/trackers, and provider card statuses together so future sessions do not drift back to Spotify-first.
- YouTube Music has no full public equivalent to Spotify library APIs; use YouTube Data API playlists/videos as the pragmatic available source.
