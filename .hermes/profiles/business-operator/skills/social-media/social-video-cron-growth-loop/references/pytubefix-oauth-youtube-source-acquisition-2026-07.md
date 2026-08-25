# PyTubeFix OAuth source acquisition — 2026-07

Use this when YouTube source acquisition is blocked by cloud/VPS bot checks and the user explicitly does **not** want yt-dlp.

## Durable result from session

- `pytube`, old `youtube_dl`, `pafy`, direct `innertube`, `you-get`, Node `@distube/ytdl-core`, and public Invidious mirrors all still hit `LOGIN_REQUIRED` / `Sign in to confirm you're not a bot` from the VPS.
- `pytubefix` with OAuth device login succeeded for a blocked Hamza source URL after the user authorized the device flow as the **Classical Echos** Google/YouTube account.
- The successful source was downloaded as a progressive MP4 stream (`itag=18`, 360p) and verified by file size/ffprobe.

## Token location

The reusable OAuth token was copied to:

```text
/opt/data/secrets/pytubefix-classical-echos/tokens.json
```

Keep it private (`0600`). Do not paste token contents into chat or commit them.

## Manual probe pattern

```bash
/opt/data/venvs/viral-radar/bin/python - <<'PY'
from pytubefix import YouTube
url = 'https://www.youtube.com/watch?v=VIDEO_ID'
yt = YouTube(
    url,
    client='WEB',
    use_oauth=True,
    allow_oauth_cache=True,
    token_file='/opt/data/secrets/pytubefix-classical-echos/tokens.json',
)
stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
if stream is None:
    stream = yt.streams.get_highest_resolution()
path = stream.download(output_path='/tmp/pytubefix-source-test')
print({'title': yt.title, 'itag': stream.itag, 'resolution': getattr(stream, 'resolution', None), 'path': path})
PY
```

## Existing project script support

`viral-clip-radar/scripts/download_youtube_source.py` was patched to accept:

```bash
--try-pytubefix \
--oauth \
--pytubefix-client WEB \
--pytubefix-token-file /opt/data/secrets/pytubefix-classical-echos/tokens.json
```

A known-good smoke test:

```bash
python3 scripts/download_youtube_source.py 'https://www.youtube.com/watch?v=2xUiBnse4x0' \
  --outdir /tmp/vr-pytubefix-token-test \
  --logdir /tmp/vr-pytubefix-token-log \
  --skip-cleanup \
  --try-pytubefix \
  --oauth \
  --pytubefix-client WEB
```

## Pitfalls

- If the process prints a Google device code and waits for Enter, use `terminal(..., pty=true, background=true)` or a script file; stdin via heredoc can EOF before the user authorizes.
- Kill stale device-login processes before starting a new one, so the user does not authorize an expired/old code.
- For this user, Classical Echos is approved for this downloader/device-login functionality.
- If the user says not to use yt-dlp, do not merely rely on fallback order that tries yt-dlp first. Add or use an explicit no-yt-dlp path so the run honors the workflow preference.
- OAuth device login may carry account risk; prefer the user's approved Classical Echos account and avoid personal/main accounts unless explicitly directed.
