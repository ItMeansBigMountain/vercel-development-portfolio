# YouTube playlist analysis + caching pattern

Use this when a music app currently pulls YouTube/YouTube Music playlists but only shows playlist metadata, and the user expects every playlist item to be analyzed individually and as an aggregate.

## Product behavior

- Dashboard playlist cards should expose an explicit action such as `Analyze every song`.
- A per-playlist route can be shaped as `/youtube/playlist/<playlist_id>/analysis`.
- The route should:
  1. load YouTube playlist metadata,
  2. page through `playlistItems` with `part=snippet,contentDetails`,
  3. normalize each public video/song item into a provider-neutral track object,
  4. analyze every item individually,
  5. show per-song cards,
  6. aggregate individual analyses into a playlist-level taste/vibe read.

## Practical first version

YouTube Data API usually gives video metadata, not full song lyrics/audio. A reliable first ship is to analyze cleaned video/title metadata, while clearly documenting that the next upgrade is richer artist/title parsing plus lyrics/audio metadata when a source is available.

Clean common title noise before analysis:

- `(official video)` / `[official video]`
- `(official audio)` / `[official audio]`
- `(lyrics)` / `[lyrics]`
- `(lyric video)`
- `music video`

## Aggregation model

For each analyzed item, collect at least:

- sentiment label
- emotion scores: `sadness`, `joy`, `fear`, `disgust`, `anger`
- keywords
- concepts/themes
- analyzer source
- cache hit/new marker

For the playlist aggregate, compute:

- count of tracks analyzed
- cache hits vs new analysis calls
- average emotion scores across tracks
- dominant emotion by max average
- sentiment counts and dominant sentiment
- top keywords/concepts by frequency
- mood/vibe tags inferred from titles plus aggregate labels

## Cache design

Do not repeatedly call Watson/LLM analyzers for unchanged playlist items. Store per-item results in durable storage.

Recommended cache key:

```txt
user_id
provider
item_type          # e.g. track
item_id            # YouTube video ID when available
analyzer_version   # bump when analysis prompt/model/schema changes
input_hash         # hash of cleaned title/text used for analysis
```

Recommended fields:

```txt
input_text
analysis_json
created_at
updated_at
hits
```

Important: include both `analyzer_version` and `input_hash` so stale analyses do not survive schema/prompt changes or title/text changes.

## UI affordances

- Show `cached` vs `new` on individual song cards.
- Show cache hit/new analysis counts at the top of the playlist report.
- Provide a `Re-analyze fresh` action that bypasses cache for the current run and updates stored results.
- Cap max playlist items for a first version (e.g. 100-150) to avoid accidental runaway API/analyzer usage.

## Verification

Local unit-style smoke:

- monkeypatch the analyzer function to increment a counter,
- analyze two unique tracks,
- analyze them again,
- assert the analyzer call count did not increase on the second pass,
- assert aggregate averages and cache-hit counts are correct.

Browser/API smoke:

- unauthenticated playlist analysis route redirects/protects access,
- dashboard playlist card includes the analysis CTA when playlist IDs are present,
- health still reports durable encrypted storage.
