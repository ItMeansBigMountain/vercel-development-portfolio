# Cron-Activated Video Upload Pipelines — 2026-06 Session Notes

Use this when the user asks to turn content automation projects into scheduled upload pipelines, especially in the HeRmEz workspace.

## Durable pattern

1. **Wrap project-specific pipelines in small script-only cron entrypoints** under `/opt/data/scripts/` rather than putting long shell commands directly in the cron prompt.
   - Example names used: `faceless_daily_upload.py`, `viral_radar_daily_upload.py`.
   - Run from the project `workdir` and set `no_agent=true` so stdout is delivered verbatim.
2. **Align cron schedules to target audience windows in Central time.** Hermes cron stores schedules in UTC, so convert intentionally.
   - 2:45 PM CT = `45 19 * * *` during CDT.
   - 7:15 PM CT = `15 0 * * *` during CDT.
   - Use these for public YouTube Shorts uploads unless the user explicitly requests private/unlisted review mode.
3. **Use public uploads for approved automation lanes.** The cron should upload approved faceless newsletter videos and Viral Clip Radar clips as `public` unless the user explicitly asks for private/unlisted review mode. Report returned `video_id` / URL.
4. **Delete media only after confirmed upload.** Treat a returned YouTube upload status/video ID as the safe point to delete generated MP4s and temporary workspaces. Preserve upload logs, manifests, metadata, and `.done` markers.
5. **Add Central-time duplicate protection.** After a successful daily upload, write a marker such as `STATE/<pipeline>_YYYY-MM-DD.done` using `America/Chicago`; on later same-day cron runs, print `skipped_already_ran_today` and exit 0. Support `FORCE_UPLOAD=1` for manual override.
6. **Verify with real execution.** Do not stop at cron creation. Run the wrapper directly, confirm upload URLs in `UPLOADS/youtube_uploads.jsonl`, and search disposable media folders to ensure `EXPORTS/*.mp4`, `SOURCES/*.mp4`, or per-video workspaces were actually removed.

## Implementation pitfalls discovered

- If a subprocess flag value starts with a dash, pass it as `--flag=value` rather than `--flag`, `-value`. Example: `--suffix=-cron`; otherwise argparse may treat `-cron` as an option and fail with `argument --suffix: expected one argument`.
- When parsing JSON from child render/upload tools, don't assume the final line alone is JSON. Child tools often pretty-print multi-line JSON. Implement a small `parse_json_output()` that finds the JSON object in stdout and parses the full object.
- If a cron run failed before a script fix, removing and recreating the cron job can clear misleading stale status when the fixed script has already been verified directly.
- A manual activation can produce duplicate private uploads if followed immediately by cron-run verification. After manual success, write the same day's `.done` marker so the next scheduled run skips.

## HeRmEz project lanes this applies to

- `faceless-youtube-channel`: render one discipline/self-improvement faceless graphic video, upload public unless private review is explicitly requested, delete generated video workspace after upload.
- `viral-clip-radar`: download reviewed rights-safe source if needed, render approved 9:16 captioned clips, upload public unless private review is explicitly requested, delete generated source/export media after upload.

Keep the skill at the class level: this reference is a reusable cron/upload/cleanup pattern, not a one-off upload log.