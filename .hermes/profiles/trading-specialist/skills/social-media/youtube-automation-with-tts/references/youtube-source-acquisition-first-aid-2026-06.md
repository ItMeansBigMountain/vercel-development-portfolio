# YouTube source acquisition first-aid — 2026-06

Use this when Viral Clip Radar / creator clipping cannot acquire source media from a YouTube URL and the user asks to fix the current stack before paid clipping APIs.

## Durable lesson

Do not jump straight from a `yt-dlp` bot-check error to paid API providers. First harden the existing source acquisition path, then prove whether the blocker is still YouTube authentication/IP reputation.

## Current local pattern

Primary downloader:

```text
/opt/data/HeRmEz/projects/viral-clip-radar/scripts/download_youtube_source.py
```

Daily upload wrapper:

```text
/opt/data/scripts/viral_radar_daily_upload.py
```

The robust order should be:

1. Use existing local/cached source MP4 if present.
2. Use archive/fallback direct MP4 URL if present.
3. Try the current local downloader before paid clipping APIs.
4. Only after local acquisition fails, try external providers such as Opus/Choppity/Vizard/Klap/MuAPI.

## Downloader hardening checklist

- Update `yt-dlp` first:

```bash
uv tool upgrade yt-dlp || python3 -m pip install --user -U yt-dlp
```

- Try multiple YouTube clients rather than one default:

```text
mweb,web_safari,tv,ios,android
```

- Use bgutil/PO-token provider if installed:

```text
/opt/data/bgutil-ytdlp-pot-provider/server
```

- Use a JS runtime only when available, e.g. Node. Current yt-dlp accepts `--js-runtimes node` reliably; `node:/path` may show `JS runtimes: none` in verbose output even when Node exists:

```text
--js-runtimes node
```

- If yt-dlp says `Remote component challenge solver script (node) was skipped` or `n challenge solving failed`, allow the official EJS remote component for that run:

```bash
yt-dlp --remote-components ejs:github --js-runtimes node ...
```

This can turn a bot-check/cookies failure into a successful authenticated download once fresh cookies are present.

- Accept env-driven authentication/proxy inputs without printing secrets:

```text
YOUTUBE_COOKIES_FILE
YTDLP_COOKIES_FILE
YTDLP_COOKIES_FROM_BROWSER
YTDLP_PROXY
HTTPS_PROXY
HTTP_PROXY
YTDLP_PLAYER_CLIENTS
```

- Log each client attempt separately so failures are diagnosable:

```text
yt-dlp-download-1-mweb.log
yt-dlp-download-2-web_safari.log
...
```

## Honest result handling

If every client still returns:

```text
Sign in to confirm you’re not a bot. Use --cookies-from-browser or --cookies for the authentication.
```

Then the scripts are not the blocker anymore. The remaining fixes are:

- provide exported YouTube cookies from a logged-in browser;
- configure `YTDLP_COOKIES_FROM_BROWSER=chrome` only if a logged-in browser exists on the same machine;
- use a residential proxy via `YTDLP_PROXY`;
- provide a local/Drive/source MP4;
- or use an official clipping/import provider.

Do not present this as `yt-dlp is broken`. Present it as YouTube requiring authenticated/proven human session or non-cloud network path for this URL/IP.

## Viral Radar wrapper behavior

If the user explicitly wants to fix the current stack, make sure `/opt/data/scripts/viral_radar_daily_upload.py` tries the local downloader before external APIs. Only disable direct downloader with an explicit env such as:

```text
VIRAL_RADAR_DISABLE_DIRECT_YOUTUBE_DOWNLOAD=1
```

## Reporting style

Keep Discord report short:

- what was patched;
- exact smoke command/result;
- whether source media was acquired;
- if blocked, name the missing proof path: cookies, proxy, local source, or external API.
