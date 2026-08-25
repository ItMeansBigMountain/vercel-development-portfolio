# MusicAI lyrics-first Watson insight pipeline

Use this reference when restoring or extending MusicAI song/playlist analysis so it behaves like the legacy app instead of only scanning YouTube titles.

## Durable lesson

For MusicAI, a visible analysis page is not enough. The user expects the old pipeline:

1. Accept a YouTube URL or plain song query.
2. Resolve a clean `artist` + `title` from the query or YouTube video title.
3. Search a lyrics provider, historically Genius.
4. Fetch full lyrics text.
5. Send the lyric text to IBM Watson NLU.
6. Preserve both modern UI fields and legacy buckets:
   - `averageEmotion`
   - `sentiment_frequencies`
   - `entityfrequencies`
   - `keywordfrequencies`
   - `conceptfrequencies`
   - `subjectsfrequencies`
   - `relationsfrequencies`
7. Only fall back to title/metadata analysis when lyrics cannot be found.

## Implementation pattern

- Keep Genius as the first resolver/search source when `GENIUS_API_KEY` is configured.
- Genius search returns metadata and the source URL; Genius HTML scraping can fail in production/serverless even when `/healthz` says `genius: true`.
- Add a second lyrics fallback such as `lyrics.ovh` before giving up to metadata-only analysis.
- Cap lyric text before Watson if needed for serverless latency/noise, but still make the analyzed source explicit: `lyrics` vs `metadata`.
- Cache key/version must include the analyzer version and input hash. Bump the analyzer version whenever switching from title-only to lyrics-first analysis so stale metadata-only rows are bypassed.
- For playlist analysis, reuse the same per-song lyrics-first analyzer and aggregate from item-level results rather than doing one playlist-level prompt.

## UI requirements

Modernized MusicAI result pages should show the legacy detail in consumer-friendly cards:

- source badge: `lyrics analyzed` or `metadata analyzed`
- lyric line count and lyric preview
- sentiment and emotion bars
- topics/concepts talked about
- keywords
- entities
- subjects
- relations
- cache/new-call state

For playlists, show how many tracks found lyrics and aggregate topics/entities/subjects/relations across the analyzed tracks.

## Verification checklist

Run a real song query end to end, not only a health check. Example expectations:

```txt
POST /api/analyze-song {"query":"Drake - Passionfruit", "refresh": true}
result.analyzer_version == lyrics-watson-vN
result.analysis.source == watson_nlu
result.analysis.analyzed_text_source == lyrics
result.analysis.lyrics_found == true
result.analysis.lyrics_line_count > 0
result.analysis.nlu_summary has averageEmotion, keywordfrequencies, conceptfrequencies, subjectsfrequencies, relationsfrequencies
```

If production returns `metadata` for a song that resolves locally with lyrics, inspect provider-specific logs and add/verify the fallback lyrics provider before shipping.

## Pitfalls

- Do not call a song scan complete if it only analyzes `Drake - Passionfruit` as a title. The user explicitly remembered and wanted lyrics→Watson analysis.
- `/healthz` proving `genius: true` only means credentials are present; it does not prove lyric fetch/scrape works.
- Do not drop the legacy Watson frequency buckets when redesigning the UI. The user values the “topics talked about and all that” details.
- Stale cache can hide a fixed analyzer. Bump the version and offer a fresh re-analyze action.
