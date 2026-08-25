# TikTok/Instagram Native Upload Pivot for Clipping Projects

Use this note when a clipping workflow hits YouTube upload restrictions or the user explicitly rejects Zapier/webhook/broker workflows.

## Session lesson

The user corrected the direction: drop Zapier completely for the clipping project and look into TikTok + Instagram uploads when YouTube causes issues. Do not keep steering the user back to Zapier once this preference is stated.

## Preferred pivot

1. Keep the local render pipeline independent: produce verified vertical MP4 artifacts first.
2. Try TikTok native upload first:
   - TikTok Content Posting API.
   - User OAuth token with `video.publish` scope.
   - Use `SELF_ONLY` for unaudited/private pilots.
   - Prefer direct `FILE_UPLOAD` from the rendered MP4 when available.
   - Query creator info before execution to confirm allowed privacy levels.
3. Try Instagram native publishing second:
   - Meta/Instagram content publishing API.
   - Requires Instagram professional account, Meta app, access token, and Instagram user ID.
   - Standard Reels flow needs a public `video_url` reachable by Meta; if no public URL exists, build/choose hosting or implement resumable upload later.
4. Keep YouTube as optional private-upload fallback, not a blocker.
5. Use manual review packets while OAuth/API credentials are incomplete: JSON/CSV/Markdown queue from rendered clips.
6. Broker APIs are fallback only if native TikTok/Instagram setup stalls or proves unreliable.

## Credential handling pattern

Store TikTok app credentials in a non-committed env file, e.g.:

```bash
/opt/data/secrets/viral-clip-radar-tiktok.env
/opt/data/HeRmEz/projects/viral-clip-radar/.env
```

Expected keys:

```bash
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TIKTOK_ACCESS_TOKEN=
TIKTOK_REFRESH_TOKEN=
META_APP_ID=
META_APP_SECRET=
META_ACCESS_TOKEN=
INSTAGRAM_USER_ID=
META_GRAPH_VERSION=v23.0
```

Always `chmod 600` credential files and verify by checking presence/length/status only — never print secrets.

## Implementation pattern

Add dry-run-first upload helpers before real API calls:

- `upload_to_tiktok.py`: builds TikTok `/v2/post/publish/video/init/` payload, defaults to dry-run, `--execute` required for real calls.
- `upload_to_instagram.py`: builds Meta `/{ig-user-id}/media` container payload, defaults to dry-run, `--execute --poll --publish` required for real publishing.

Smoke-test with a generated 1-second 1080x1920 MP4 and assert dry-run JSON shape before asking the user for more credentials.
