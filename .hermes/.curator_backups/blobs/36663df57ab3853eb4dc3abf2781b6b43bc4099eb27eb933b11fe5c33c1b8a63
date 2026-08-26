# YouTube device-login reauth for downloader/source acquisition

Use this when YouTube source acquisition fails with login/auth errors such as:

- `Sign in to confirm you're not a bot`
- `LOGIN_REQUIRED`
- `BotDetection`
- `RefreshError`, expired cached device token, or pytubefix OAuth prompts again

This is separate from YouTube upload OAuth. Upload/metadata tokens still use `google_reauth_workflow.py youtube-auth-url` / `youtube-exchange`. Downloader/source acquisition uses a pytubefix device-login token.

## Current user-approved account

Use the **Classical Echos** Google/YouTube account for downloader/device-login functionality.

Cached token path:

```bash
/opt/data/secrets/pytubefix-classical-echos/tokens.json
```

Keep it private:

```bash
chmod 700 /opt/data/secrets/pytubefix-classical-echos
chmod 600 /opt/data/secrets/pytubefix-classical-echos/tokens.json
```

## Reauth flow

1. Start a pytubefix OAuth probe in a PTY/background process:

```bash
/opt/data/venvs/viral-radar/bin/python /opt/data/HeRmEz/projects/viral-clip-radar/TMP/pytubefix_oauth_probe.py
```

2. Read the emitted device code, e.g.:

```text
Please open https://www.google.com/device and input code ABC-DEF-GHIJ
```

3. Tell the user to open `https://www.google.com/device`, sign in as **Classical Echos**, enter the code, and approve.

4. After the user says `done`, submit Enter to the waiting process.

5. Verify success. Expected output includes a title, stream, and downloaded file path:

```text
TITLE ...
STREAM <Stream: itag="18" ...>
DOWNLOADED /tmp/yt-alt/pytubefix-oauth/<title>.mp4
```

6. Persist the refreshed token:

```bash
mkdir -p /opt/data/secrets/pytubefix-classical-echos
cp /opt/data/venvs/viral-radar/lib/python3.11/site-packages/pytubefix/__cache__/tokens.json \
  /opt/data/secrets/pytubefix-classical-echos/tokens.json
chmod 600 /opt/data/secrets/pytubefix-classical-echos/tokens.json
```

7. Smoke-test without yt-dlp:

```bash
python3 /opt/data/HeRmEz/projects/viral-clip-radar/scripts/download_youtube_source.py \
  'https://www.youtube.com/watch?v=2xUiBnse4x0' \
  --outdir /tmp/vr-pytubefix-token-test \
  --logdir /tmp/vr-pytubefix-token-log \
  --skip-cleanup \
  --no-ytdlp \
  --try-pytubefix \
  --oauth \
  --pytubefix-client WEB \
  --pytubefix-token-file /opt/data/secrets/pytubefix-classical-echos/tokens.json
```

Success is product-level `downloaded: true` with method `pytubefix`.

## Pipeline integration

For Viral Radar, the daily uploader should call `scripts/download_youtube_source.py` with:

```bash
--no-ytdlp --try-pytubefix --oauth --pytubefix-client WEB
```

The default token file is already:

```bash
/opt/data/secrets/pytubefix-classical-echos/tokens.json
```

Set `VIRAL_RADAR_DISABLE_YTDLP=1` if any wrapper still calls the source downloader without `--no-ytdlp`.

## Reporting statuses

- `ok_device_login`: device-login reauth completed and token saved.
- `ok_source_download`: pytubefix downloaded the source MP4.
- `blocked_device_login`: user has not completed the Google device code flow, code expired, or wrong account was used.
- `blocked_source`: device token exists but YouTube still blocks the source; retry reauth, then consider residential proxy/local source.

## Pitfalls

- Do not confuse this with YouTube upload OAuth. Upload scopes/tokens do not fix source download bot checks.
- Do not use yt-dlp for this user's current Viral Radar source acquisition unless explicitly re-approved; use pytubefix OAuth first.
- Device codes expire quickly. If the user misses the window, kill the stale process and start a fresh one.
- If the user authorizes the wrong Google account, delete/regenerate the token and repeat with Classical Echos.
- Do not print token JSON contents in chat or logs.
