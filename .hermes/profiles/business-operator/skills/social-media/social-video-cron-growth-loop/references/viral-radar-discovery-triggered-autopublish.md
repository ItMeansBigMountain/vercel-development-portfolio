# Viral Radar discovery-triggered auto-publish cron pattern

Use when the user wants a creator watchlist/discovery cron to publish automatically when it finds a new video, not merely report discovery.

## Desired behavior

When `poll_watchlist.py` finds new creator videos, the cron should:

1. Print the new video(s) and plan paths for the user.
2. Extract the exact discovered `Plan:` directories from the poll output.
3. Export them as `VIRAL_RADAR_PRIORITY_PLANS` for the uploader.
4. Run `FORCE_UPLOAD=1 python3 /opt/data/scripts/viral_radar_daily_upload.py`.
5. The uploader should prioritize those newly discovered plans before older reviewed manifests.
6. If a discovered plan only has `source_metadata.json`, auto-create a minimal `clip_manifest.json` so the job can immediately attempt source download -> vertical render -> public upload.
7. Only fall back to older source-ready reviewed manifests after the newly found plans fail/source-block.

## Wrapper pattern

In `/opt/data/scripts/creator_watchlist_clip_upload.sh`, after printing discovery output:

```bash
PRIORITY_PLANS="$(printf '%s\n' "$DISCOVERY_OUTPUT" | awk '/^  Plan: /{sub(/^  Plan: /, ""); print}' | paste -sd ':' -)"
if [[ -n "$PRIORITY_PLANS" ]]; then
  export VIRAL_RADAR_PRIORITY_PLANS="$PRIORITY_PLANS"
fi

FORCE_UPLOAD=1 python3 /opt/data/scripts/viral_radar_daily_upload.py
```

## Uploader pattern

`viral_radar_daily_upload.py` should include helpers that:

- parse `VIRAL_RADAR_PRIORITY_PLANS` as an `os.pathsep`-separated list;
- accept either plan directories or direct `clip_manifest.json` paths;
- if a plan directory has no manifest but has `source_metadata.json`, create a minimal manifest with:
  - creator/channel name;
  - source title/url/video id;
  - `source_file` under `SOURCES/<video_id>/source.mp4`;
  - one short clip from `00:00:00` to up to `00:00:58` for Shorts, or a short opening segment for long-form fallback;
  - hook text derived from creator + title.

The renderer adds hook overlay when subtitles are absent, and the uploader adds source attribution, so the auto-generated manifest is still a transformed clip attempt rather than a raw reupload.

## Verification

Run:

```bash
python3 -m py_compile /opt/data/scripts/viral_radar_daily_upload.py
bash -n /opt/data/scripts/creator_watchlist_clip_upload.sh
```

Also smoke-test manifest generation in Python if needed by importing the script and setting `VIRAL_RADAR_PRIORITY_PLANS` to a known watchlist plan directory.

## Pitfalls

- Do not let the discovery cron select an unrelated older manifest first; users expect "found a video" to mean "try that video now".
- Do not mark discovery-only work as success when no upload was attempted. `no_agent` jobs should stay silent on no new videos and report a product-level status on new videos.
- Do not report a blocker until the uploader has exhausted source acquisition for priority plans and then source-ready fallbacks.
- Keep Opus/provider fallback disabled unless configured; prefer local/direct/archive/source-download ladders already documented in the Viral Radar source-acquisition references.
