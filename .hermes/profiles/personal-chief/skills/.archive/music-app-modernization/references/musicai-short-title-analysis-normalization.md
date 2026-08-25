# MusicAI short-title analysis normalization

## Trigger

Use this when a MusicAI single-song or YouTube playlist analysis page renders successfully but the emotion bars/fields are all `0.0%` or empty, especially for short metadata-only inputs such as `Drake - Passionfruit` or YouTube Topic titles.

## Root cause pattern

Short song titles often provide sparse text. IBM Watson NLU may still return useful document-level `emotion` and `sentiment`, but omit optional sections such as `semantic_roles`, `categories`, or other feature arrays. Legacy parser code that indexes those optional keys directly can raise a `KeyError`, which makes the app treat Watson as failed and drop into a simplistic local fallback. If the fallback only scores obvious lyric words, title-only text can then cache an all-zero analysis.

## Fix pattern

1. Make Watson response parsing tolerant of missing optional fields:
   - `response.get('semantic_roles') or []`
   - `response.get('categories') or []`
   - `response.get('sentiment', {}).get('document', {}).get('label', 'neutral')`
   - entity/keyword sentiment fields should default to `neutral`.
2. Normalize analysis objects before rendering/caching:
   - expected keys: `joy`, `sadness`, `fear`, `disgust`, `anger`; optionally app-specific `energy`.
   - coerce numeric strings/None to bounded floats in `[0,1]`.
3. If every emotion value is zero for metadata-only text, use a transparent weak baseline/inferred profile rather than showing an empty card. The baseline should be visibly modest, not overconfident.
4. Bump the analyzer/cache version after changing normalization, e.g. `youtube-title-watson-v2`, so old cached zero rows are bypassed.
5. Keep the UI's "Re-analyze fresh" action so users can invalidate a stale cached item manually.

## Regression checks

- Direct analyzer check for `Drake - Passionfruit` returns at least one emotion value > 0.
- `/api/analyze-song` with `{query: 'Drake - Passionfruit', refresh: true}` returns `ok: true`, the new analyzer version, and non-zero `overall_emotion` values.
- Playlist aggregation over a mocked/real track result yields non-empty `average_emotion` and a non-`unknown` dominant emotion.
- Playwright smoke test for the single-song analyzer asserts at least one emotion value is non-zero, not just that the page rendered.

## Pitfall

Do not consider a rendered analysis page proof that analysis worked. Verify the payload values behind the bars; a cached all-zero result can look like a successful run unless tests assert non-zero or explicitly mark sparse-baseline behavior.
