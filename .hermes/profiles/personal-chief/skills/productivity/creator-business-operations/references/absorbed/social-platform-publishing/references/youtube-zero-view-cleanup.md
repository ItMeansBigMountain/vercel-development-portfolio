# YouTube zero-view cleanup workflow

Use this when the user asks to delete videos with zero views across their YouTube automation channels.

## Safety pattern

1. Refresh metrics first with the metrics monitor for the relevant upload tokens.
2. Build a candidate list from the latest metrics snapshot, using `youtube.statistics.viewCount == "0"` only.
3. Group candidates by the OAuth token/channel that owns the video. Do not assume one token can delete every channel's videos.
4. Delete with YouTube Data API `videos().delete(id=...)` using a token that has `youtube.force-ssl` and owns the channel.
5. Verify deletion with `videos().list(id=...)`; no returned item means the video is gone/inaccessible to that owner token.
6. Write an audit JSON with candidate IDs/titles/channel, deletion result, verification status, and any errors.
7. Never paste token paths or token contents verbatim in chat; report counts and audit path.

## User-specific notes from 2026-06 cleanup

- Metrics may include multiple channels. `Sosai Oyama` uploads used `/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json`.
- One `Classical Echos` zero-view video required the Classical Echos token instead: `/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json`.
- A post-delete `videos().list()` immediately after `delete()` can sometimes still return an item for a few IDs, but a later batch verification with the owner token is the source of truth.
- The user gave direct approval to delete all zero-view videos; still verify the set from live/current metrics before executing.

## Reusable script location

A project-side helper was created at:

`/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/delete_zero_view_videos.py`

Typical use:

```bash
# Dry-run/audit candidates
/opt/hermes/.venv/bin/python /opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/delete_zero_view_videos.py

# Execute deletion after the user asks for it
/opt/hermes/.venv/bin/python /opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/delete_zero_view_videos.py --execute
```

Default audit path:

`/opt/data/HeRmEz/projects/_ops/youtube-automation/delete-zero-view-audit.json`
