# Viral Radar Performance Learnings

Last updated: `2026-08-27T01:08:42.132834+00:00`

## Metrics status

- Live YouTube metrics are fetched with OAuth tokens from the same upload lane/account, not a generic API key.
- This preserves private/unlisted visibility and prevents mixing channel accounts.
- Token/account errors:
  - `/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json`: RefreshError: ('invalid_grant: Token has been expired or revoked.', {'error': 'invalid_grant', 'error_description': 'Token has been expired or revoked.'})

## viral-clip-radar

- Uploads logged: 477 total; 459 public/metric-eligible.
- Live metrics unavailable for metric-eligible videos in this snapshot; inspect token/account errors above.

## Operating rule for future Viral Radar runs

- Before clipping the next influencer video, read this file and avoid repeating low-signal titles/hooks.
- Double down on topics whose public videos beat the channel median views and comments.
- Treat missing metrics as a setup issue, not as proof the content failed.
