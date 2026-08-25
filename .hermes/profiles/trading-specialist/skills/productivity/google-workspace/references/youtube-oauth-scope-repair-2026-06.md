# YouTube OAuth scope repair notes — 2026-06

Use when YouTube upload tokens refresh but metadata/channel reads, analytics, or faceless-channel uploads fail due to missing or stale scopes.

## Scope set for YouTube channel automation

For the user's YouTube upload/metadata/readiness workflows, request the full channel automation scope set together:

- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.force-ssl`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

`youtube.upload` alone can upload but is not enough for channel identity verification, metadata edits, private reads, or analytics. Tokens with old/broad/stale scopes can refresh-fail with `invalid_scope`; generate a fresh profile-specific auth URL and exchange the newest redirect URL.

## Profile-specific pending state

When generating several YouTube reauth URLs in one session, keep separate pending files per channel/profile so redirects exchange into the correct token path. Example profile directories used in this workspace:

- `/opt/data/secrets/youtube-classicalechos/`
- `/opt/data/secrets/youtube-trapiistan/`
- `/opt/data/secrets/faceless-youtube-channel/`
- `/opt/data/secrets/youtube-main/`

## Verification after exchange

After saving the token:

1. Refresh the token with the exact requested scope list.
2. Call YouTube `channels().list(part='id,snippet', mine=True)`.
3. Report the channel title/id and stored scopes.
4. Only then mark upload/metadata/analytics readiness.

## User-facing flow

Send the auth URL as a single line per profile. Tell the user the browser may land on `localhost:5000` and fail; that is expected. They should copy the entire redirected URL from the address bar and send it back with a label like `faceless: http://localhost:5000/?code=...`.

For newsletter/faceless video generation retries, the working URL generator is the project helper:

```bash
cd /opt/data/HeRmEz/projects/faceless-youtube-channel
python3 scripts/youtube_oauth.py auth-url
```

This writes pending PKCE state under `/opt/data/secrets/faceless-youtube-channel/youtube_oauth_pending.json` and prints the consent URL with upload, force-ssl, readonly, and analytics-readonly scopes. After the user returns the labeled localhost callback, exchange with the same helper and then retry the newsletter video pipeline only after token/channel verification succeeds.
