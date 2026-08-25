# Clipping + Upload Pilot Notes

Use this when asked to prove end-to-end capability by clipping a supplied YouTube/Rumble video and uploading a test clip to YouTube.

## Preflight sequence

1. Create or reuse a candidate workspace under the project, e.g. `CLIP_PLANS/<date>-<slug>/`, before editing/uploading.
2. Fetch lightweight metadata first (`oEmbed`, browser page, or platform API) so the workspace has title, creator, source URL, and attribution even if media download fails.
3. Attempt transcript/metadata with `yt-dlp` or transcript helper, but expect cloud-hosted environments to trigger YouTube bot checks.
4. Before promising upload, verify user OAuth token exists for YouTube upload scope:
   - token path commonly used in this workspace: `~/.hermes/youtube_upload_token.json`
   - required scope: `https://www.googleapis.com/auth/youtube.upload`
   - service-account JSON is not sufficient for normal channel uploads.
5. Upload only as `private` for the first pilot.

## Common blockers and fixes

### YouTube download/transcript bot check

Typical errors:

```text
Sign in to confirm you’re not a bot. Use --cookies-from-browser or --cookies for the authentication.
YouTube is blocking requests from your IP / cloud provider.
pytubefix.exceptions.BotDetection: This request was detected as a bot
```

Fix pattern:

- First install/update the free downloader stack when using uv-managed tools: `uv tool install yt-dlp --force --with bgutil-ytdlp-pot-provider`. Verify with `yt-dlp -v URL` that bgutil PO-token providers appear.
- First try current `yt-dlp` plus PO-token provider/plugin (`bgutil-ytdlp-pot-provider`), a JS runtime (`--js-runtimes node:/usr/local/bin/node` when Node exists), and `--extractor-args 'youtube:player_client=mweb;youtubepot-bgutilscript:server_home=/opt/data/bgutil-ytdlp-pot-provider/server'`.
- Try `pytubefix` as the maintained pytube-style replacement, but know that cloud IPs can still trigger BotDetection even with `client='WEB'` / automatic node PO token.
- If a rights-safe official media mirror exists (NASA/Wikimedia/Internet Archive/creator download page), use it as a fallback after logging the YouTube block; preserve the original YouTube URL and attribution in metadata.
- Use `yt-dlp --cookies /path/to/youtube-cookies.txt ...`, or
- use `yt-dlp --cookies-from-browser chrome ...` when a browser profile is available, or
- use a residential proxy if the blocker is cloud-IP reputation, or
- use a phone-side/Pythonista downloader: iPhone residential/mobile network often succeeds where the server IP fails.

Do not summarize this as "YouTube does not work"; the durable lesson is: cloud IPs often require cookies, OAuth, residential proxy, or phone-side download automation.

### Upload OAuth missing

Typical error:

```text
Missing YouTube user OAuth token: ~/.hermes/youtube_upload_token.json. Uploads require user OAuth with https://www.googleapis.com/auth/youtube.upload.
```

Fix pattern:

- Generate a user OAuth token from a Google OAuth client-secret JSON.
- Keep upload scripts gated behind that token.
- Publish private first and report the real uploaded video URL only after the API returns an ID.

## Clip geometry

For landscape long-form sources converted to vertical shorts, prefer:

```text
scale=-2:1920,crop=1080:1920
```

This scales to full vertical height before center-cropping and avoids invalid crop errors caused by `scale=1080:-2,crop=1080:1920` on 16:9 inputs.

## Artifact cleanup rule

For VPS clipping workflows, add a self-cleaning mechanism before doing repeated downloads/exports. Keep large local media out of git and enforce retention such as: sources 48h, exports 7d, logs 14d, emergency cleanup when free disk is low. Verify cleanup with both dry-run and a real deletion test before reporting it as active.

## Reporting rule

If the clip cannot be downloaded or uploaded due to auth/cookies, still save:

- candidate metadata
- transcript/download/upload error logs
- exact next required input, e.g. cookies file, local source video, OAuth client secret

But do not claim a successful clip or upload until a real artifact/upload URL exists.