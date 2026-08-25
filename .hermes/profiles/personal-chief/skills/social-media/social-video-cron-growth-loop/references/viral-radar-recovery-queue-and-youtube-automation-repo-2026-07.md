# Viral Radar recovery queue + YouTube automation repo consolidation (2026-07)

Use this when the user asks to recover Viral Radar clips that were found/rendered but not successfully uploaded, or asks to consolidate the YouTube automation codebases.

## Upload failure interpretation

- `uploadLimitExceeded` means the upload side is blocked by YouTube/account limit, not that clip generation should be abandoned.
- Render/prepare real source clips and queue them for later upload; do not substitute placeholders to make progress look successful.
- For the user, treat "not successfully uploaded" as: creator/source has fewer than the required minimum successful public uploads, so make/queue missing clip videos from that creator/source.

## Recovery queue pattern

1. Count successful uploads by `source_url` from Viral Radar upload logs.
2. Find real creator long-form manifests below the target minimum.
3. Skip:
   - NASA/JPL/space/Mars/Perseverance/unknown evergreen filler.
   - YouTube Shorts when the request is to make a minimum batch per long-form source; Shorts usually cannot produce 10 distinct clips.
4. Prefer source-ready manifests first; if source is missing, use the existing source acquisition ladder.
5. Expand the manifest to at least 10 clips where the source duration supports it.
6. Render the real vertical/captioned clips.
7. Queue each rendered clip with upload metadata in `UPLOAD_QUEUE/` if YouTube upload is blocked or deliberately deferred.
8. Verify every queued metadata file points to an existing rendered file.
9. Report concise counts by creator/source, plus blockers.

Useful local command from this session:

```bash
VIRAL_RADAR_RECOVERY_TARGET_MIN=10 \
VIRAL_RADAR_RECOVERY_MAX_SOURCES=8 \
VIRAL_RADAR_RECOVERY_MAX_RENDERS=80 \
python3 /opt/data/scripts/viral_radar_prepare_recovery_queue.py
```

The script prepares/queues only; it does not publish. Upload replay remains subject to YouTube's current upload limit.

## Consolidated YouTube automation repo pattern

If asked to make a repo for the automation codebases:

- Create/use `/opt/data/HeRmEz/projects/youtube-automation` as the consolidated child repo.
- Include:
  - `faceless-youtube-channel/`
  - `viral-clip-radar/`
  - `shared-scripts/`
  - `legacy-existing/` if files already existed at that path.
- Exclude generated media, sources, upload queues, analytics/logs, tokens, credentials, caches, and large media files.
- Verify with file listing/searches before commit: internal files present, no `*.mp4`, no `*token*` files, no unexpectedly large files.
- Push the child repo first, verify local SHA equals remote SHA, then add/update it as a parent HeRmEz submodule.
- Use `git submodule absorbgitdirs` when converting an existing nested worktree to a proper submodule.

The user explicitly asked to "ls/check internal files" for this class of work, so do a real file inventory and report what was checked.