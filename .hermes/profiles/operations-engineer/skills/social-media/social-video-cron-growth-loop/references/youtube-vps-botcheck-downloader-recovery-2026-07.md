# YouTube VPS bot-check and yt-dlp recovery

Use this when Viral Radar or creator-clip jobs fail with YouTube `LOGIN_REQUIRED`, `Sign in to confirm you're not a bot`, stale-cookie warnings, missing JavaScript runtime, or 403 responses from a cloud/VPS host.

## Recovery sequence

1. **Reproduce before changing anything.** Run both the project wrapper and direct `yt-dlp -v` against one known-blocked URL. Capture full stdout/stderr, executable path, yt-dlp version, Python version, optional libraries, proxy map, JS runtimes, player client, PO-token provider status, and exact exit codes. A wrapper's final JSON line is not enough.
2. **Separate three independent auth planes:**
   - YouTube Data API OAuth tokens authorize uploads/metadata and channel probes.
   - Browser cookies authenticate yt-dlp playback extraction.
   - pytubefix/device tokens belong to that downloader only.
   Repairing upload OAuth does **not** repair yt-dlp bot checks, and localhost callbacks from the Data API flow are not yt-dlp credentials.
3. **Correct local integration defects before blaming YouTube:**
   - Resolve the actual `yt-dlp` executable; do not assume `python -m yt_dlp` exists in the current Python environment.
   - Auto-detect Node with `shutil.which("node")`; do not hard-code `/usr/local/bin/node` or `/usr/bin/node`.
   - Pass the detected runtime explicitly with `--js-runtimes node:<resolved-path>`.
   - Confirm the bgutil server with a health probe and pass the real server home. A running provider does not by itself bypass a VPS IP bot check.
   - Try a bounded client set (`mweb`, `web_safari`, `tv`, `ios`, `android`) and retain per-client logs.
4. **Use cookies deliberately:**
   - Prefer a fresh direct **Netscape-format `cookies.txt`** export from the browser currently logged into YouTube. Store it under `/opt/data/secrets/...` with mode `0600`; never print cookie values.
   - If the user supplies JSON cookies, convert to Netscape format and include relevant `.youtube.com` and Google login domains when present.
   - Point `YOUTUBE_COOKIES_FILE` / `YTDLP_COOKIES_FILE` at the secured jar, or make the wrapper select the newest configured candidate.
   - If yt-dlp says the cookies were rotated/no longer valid, stop retrying libraries with that jar. Obtain a fresh export from the active browser session.
5. **Bound alternative tests.** One smoke test each is enough for bgutil + JS runtime, cookie jar, player clients, `curl_cffi` impersonation, and pytubefix. Repeatedly swapping downloader libraries cannot repair a rejected datacenter IP.
6. **If the VPS remains rejected with current cookies:** use a residential/mobile egress path, run acquisition on the user's logged-in machine/browser network, accept a local/Drive MP4, or use an official creator repost/direct source. Do not call an Archive/Rumble/Cobalt bypass a yt-dlp repair.
7. **Verify the actual repair.** Success requires the original URL to download through the intended wrapper, `ffprobe` to confirm nonzero duration and valid audio/video streams, and the test artifact to be removed afterward unless it is deliberately queued for clipping.

## Wrapper hardening pattern

A robust project wrapper should:

- auto-detect the yt-dlp executable and JS runtime;
- auto-select a configured cookie jar without exposing it in reports;
- preserve full command logs with credentials redacted;
- distinguish `stale_cookies`, `blocked_datacenter_ip`, `missing_js_runtime`, `extractor_failure`, and `download_ok`;
- try only a bounded client list;
- emit the exact next required input instead of generic fallback prose;
- never claim success based only on metadata extraction or a scheduler exit code.

## Known diagnostic signature

`yt-dlp` can be fully current and still fail on a VPS. A typical verbose trace is:

- current stable yt-dlp loads normally;
- player/API response is `LOGIN_REQUIRED`;
- cookies warn that they were rotated or no longer valid;
- Node and bgutil may be healthy;
- all tested player clients return the same bot confirmation.

That signature is an egress/session-trust blocker, not a package-version bug. The actionable fixes are fresh browser cookies tied to an active session or non-datacenter egress.

## Reporting rule

Report product status as `blocked_source` until a real media file downloads and passes `ffprobe`. Include the raw relevant error lines in a fenced block, summarize what was tried, and request exactly one missing input (fresh Netscape cookies or a residential proxy). Do not imply that upload OAuth reauthorization fixed playback extraction.
