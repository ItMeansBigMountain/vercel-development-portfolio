# TikTok/Instagram Upload Pivot for Clipping Projects (2026-06)

Use this reference when YouTube upload/private-mode restrictions are slowing a clipping project and the user wants to focus on TikTok + Instagram instead.

## Workflow correction captured

If the user says to drop Zapier/broker/glue tooling, remove it from the clipping plan and stop recommending it as a near-term path. Treat it as out of scope until the user reopens it.

## Preferred target order

1. **Rendered MP4 artifact first** — produce and verify local clips independent of any platform.
2. **TikTok native pilot** — best first non-YouTube target because TikTok Content Posting API supports direct `FILE_UPLOAD` from a local MP4 as well as `PULL_FROM_URL`.
3. **Instagram native pilot** — use Meta/Instagram Graph content publishing for Reels, but remember Meta needs a public `video_url` unless implementing resumable upload.
4. **YouTube fallback** — keep private upload available, but do not let YouTube API restrictions block TikTok/Instagram progress.
5. **Broker fallback only** — if native app/OAuth setup is too slow, test one social-posting broker; do not keep multiple SaaS tools in the core plan.

## TikTok implementation pattern

Create a dry-run-first helper that:

- Loads `.env` without printing secrets.
- Accepts `--file` for local MP4 `FILE_UPLOAD` and `--video-url` for `PULL_FROM_URL`.
- Defaults to dry-run unless `--execute` is passed.
- Uses `SELF_ONLY` for pilots because unaudited TikTok clients are restricted to private visibility.
- Supports `--check-creator` before posting to query creator info and valid privacy levels.
- Requires `TIKTOK_ACCESS_TOKEN` with `video.publish` scope for execution.

Example command shape:

```bash
python3 scripts/upload_to_tiktok.py \
  --file EXPORTS/test-short.mp4 \
  --caption "Private TikTok upload pilot #clips" \
  --privacy SELF_ONLY
```

## Instagram implementation pattern

Create a dry-run-first helper that:

- Loads `.env` without printing secrets.
- Accepts `--video-url` rather than a local file for the first version.
- Defaults to dry-run unless `--execute` is passed.
- Redacts access tokens in dry-run output.
- Creates the media container, optionally polls status, then publishes only if `--publish` is explicit.
- Requires `META_ACCESS_TOKEN` and `INSTAGRAM_USER_ID` for execution.

Example command shape:

```bash
python3 scripts/upload_to_instagram.py \
  --video-url "https://example.com/test-short.mp4" \
  --caption "Instagram Reels upload pilot #clips"
```

## Documentation update pattern

When making this pivot in a repo:

- Update the publishing launch plan so TikTok/Instagram are first-class targets.
- Remove Zapier/broker language if the user explicitly dropped it.
- Keep manual review packets as a bridge while tokens are not ready.
- Update `.env.example` with TikTok and Meta/Instagram fields, but never commit real tokens.
- Run smoke tests with a generated MP4 and dry-run payload assertions before claiming the scripts work.
