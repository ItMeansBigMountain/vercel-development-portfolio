# YouTube browser-cookie repair and full-loop verification

Use this when `yt-dlp` on a VPS reports YouTube bot checks and the user supplies a browser-extension JSON cookie export.

## Recovery procedure

1. Reproduce with direct `yt-dlp` and the project wrapper, preserving full stderr. Separate playback cookies from YouTube Data API OAuth; upload OAuth cannot repair media playback authentication.
2. Validate the JSON structurally without printing cookie values. Require an array of cookie objects with at least `domain`, `path`, `name`, and `value`; verify expected `.youtube.com` authentication-cookie names and expiration timestamps.
3. Convert to Netscape format securely. For each cookie, emit `domain`, include-subdomains flag, `path`, secure flag, integer expiry (`0` for session), `name`, and `value`. Prefix an HttpOnly domain with `#HttpOnly_`. Write atomically under `/opt/data/secrets/youtube-cookies/`, then chmod `0600`.
4. Remove the credential-bearing upload/cache copy after successful conversion and remove stale superseded jars. Never print cookie values or include them in logs.
5. Make the downloader auto-detect the real `yt-dlp` executable and JavaScript runtime (`shutil.which('node')`) rather than assuming a fixed path. Select the newest secured cookie jar deterministically and pass the configured PO-token provider/player clients.
6. Verify with a real download of the previously failing URL—not `--simulate` alone. Run `ffprobe` and require a readable audio/video container, expected duration, and nonzero size.
7. Resume the interrupted class-level workflow after the blocker is repaired: transcript/manifest creation, transformative vertical caption rendering, dimension/duration probes, public upload with account failover, URL-ledger verification, and safe cleanup. A downloader fix is not task completion when the user's original request was scout→clip→upload→cleanup.
8. Delete temporary verification media and logs that could reveal credential paths. Preserve manifests, subtitles, upload ledgers, retry queues, and diagnostics that contain no secrets.

## Pitfalls

- Browser-extension JSON is not accepted directly by `yt-dlp`; convert it to Netscape format.
- Fresh-looking expiry dates do not prove the session works; only a real media download does.
- Do not claim success from extraction metadata alone.
- Do not stop after fixing the blocker if the upstream user request remains unfinished.
