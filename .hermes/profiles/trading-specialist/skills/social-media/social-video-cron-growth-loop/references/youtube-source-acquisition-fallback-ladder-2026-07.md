# YouTube source acquisition fallback ladder — 2026-07

Use this when Viral Radar needs creator source media but YouTube downloads fail on a cloud/VPS IP.

## User correction

The user does not want Opus Clips and is scrapping that dependency. Do not produce `OPUSCLIP_API_KEY unset` / Opus fallback warnings as the normal path. Source acquisition should be resilient without Opus.

The user will not provide source videos for Viral Radar. Never ask for a local/Drive MP4 or imply that acquisition is waiting on the user. When a download fails, report that the automation must redownload the source, classify the failure, delete only verified corrupt/partial artifacts, and continue through automated fallbacks. The only user interaction that may be requested is account authorization, fresh browser cookies, or approval/configuration of infrastructure such as a proxy—not the video itself.

Before retrying any existing source artifact:

1. Run `ffprobe` and require a valid video stream, nonzero duration, and a plausible container.
2. Treat HTML saved as `.mp4`, zero-byte/truncated files, missing `moov` atoms, and incomplete downloader fragments as corrupt.
3. Delete corrupt media plus `.part`, `.ytdl`, and temporary fragments for that source, while preserving manifests, metadata, attribution, logs, and successfully rendered/queued clips.
4. Redownload to a temporary path, verify with `ffprobe`, then atomically move it into the manifest source path.
5. If every automated fallback fails, emit `blocked_source` with the exact URL, attempted methods, raw errors, corrupt files removed, and the next automated/infrastructure remedy. Do not ask the user to supply the media.

## Preferred fallback ladder

1. Use existing local/cached `source.mp4` if present.
2. Use manifest `fallback_source_url` or `archive_source` if it is a direct/video source.
3. Try the direct downloader stack, honoring the user's preference if they reject a tool:
   - If the user explicitly says not to use `yt-dlp`, skip it; do **not** keep cycling yt-dlp flags or let a fallback script try it first.
   - For the no-yt-dlp path, use `pytubefix` OAuth with the Classical Echos token file documented in `references/pytubefix-oauth-youtube-source-acquisition-2026-07.md`.
   - Default path when yt-dlp is allowed: `yt-dlp` with multiple clients: `mweb,web_safari,tv,ios,android`
   - bgutil/PO-token provider if present
   - Node JS runtime if present
   - env-driven cookies/proxy: `YOUTUBE_COOKIES_FILE`, `YTDLP_COOKIES_FILE`, `YTDLP_COOKIES_FROM_BROWSER`, `YTDLP_PROXY`, `HTTPS_PROXY`, `HTTP_PROXY`
   - When the user supplies exported cookies, convert to Netscape format, store under `/opt/data/secrets/` with `0600`, and smoke-test one blocked URL before replaying the cron. If yt-dlp says `provided YouTube account cookies are no longer valid`, a `.youtube.com`-only export is not enough or the session rotated; request a fresh export that includes Google/YouTube auth cookies from the active logged-in browser/session.
   - Python-only ladder: `pytubefix` clients `WEB,WEB_EMBED,ANDROID,IOS`; then `pytubefix` OAuth device flow (`use_oauth=True`, `allow_oauth_cache=True`) if the user is present and approves the Google device-code login; then `pytube`; then direct `innertube` API probe to classify `LOGIN_REQUIRED` vs actual stream availability. `youtube_dl`/`pafy` usually wrap stale extraction and are only quick probes, not likely durable fixes.
4. If YouTube still returns bot-check, search for creator-controlled reposts before declaring blocked:
   - `site:facebook.com <creator> <title keywords> video`
   - `site:facebook.com/<official page>/videos <topic>`
   - creator/brand sites, podcast pages, Instagram/Facebook reposts, or official short excerpts
5. Prefer official creator/page reposts over fan pages. If using a non-YouTube source, update manifest attribution (`source_url`, `source_url_original_youtube`, `source_attribution`) and keep clips transformative.
6. Only then report `blocked_source` with the missing proof/remedy path: refreshed cookies or OAuth, a residential proxy, another automated egress/downloader worker, an official creator repost, a direct/archive source, or a configured non-Opus provider. Never ask the user to provide the source video.

## Why this matters

Current metrics show Huberman/credible psychology sources perform better. The source strategy should prioritize credible voices and not treat creator diversity as more important than credible, high-retention psychology/self-control angles.

Interpretation:
- If the user has not constrained tools, a useful smoke test is to run a bounded set of queued manifests through the downloader with low-res format selection, then inspect attempts:

```bash
python3 scripts/download_youtube_source.py "$URL" \
  --outdir /tmp/vr-smoke \
  --logdir /tmp/vr-log \
  --skip-cleanup \
  --try-pytubefix \
  --try-pytube \
  --format '18/b[height<=360]/bv*[height<=360]+ba/b[height<=360]/b'
```

- If the user explicitly asks for another Python package / no `yt-dlp`, run the Python ladder directly instead of re-testing yt-dlp:

```bash
# Non-interactive probes: classify whether normal Python extractors can see streams.
python3 - <<'PY'
from pytubefix import YouTube
url = 'https://www.youtube.com/watch?v=VIDEO_ID'
for kwargs in [dict(client='WEB'), dict(client='WEB_EMBED'), dict(client='ANDROID'), dict(client='IOS')]:
    print('TRY pytubefix', kwargs)
    try:
        yt = YouTube(url, **kwargs)
        print('title', yt.title)
        print('streams', yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first())
    except Exception as e:
        print('ERR', type(e).__name__, str(e)[:300])
PY

# Interactive fallback when the user is present: Google device-code OAuth.
python3 - <<'PY'
from pytubefix import YouTube
url = 'https://www.youtube.com/watch?v=VIDEO_ID'
yt = YouTube(url, client='WEB', use_oauth=True, allow_oauth_cache=True)
s = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
print('stream', s)
if s:
    print(s.download(output_path='/tmp/pytubefix-oauth'))
PY
```

- `innertube` can be used as a lightweight classifier: if multiple clients return `playabilityStatus.status == LOGIN_REQUIRED` and no `streamingData`, the block is at YouTube playback API/IP/session level, not a single downloader bug.
- `yt-dlp` bot-check + `pytubefix`/`pytube` HTTP 400 means YouTube is requiring a proven/authenticated/non-cloud session for that URL/IP.
- If an official Facebook repost is found, `yt-dlp` can often acquire it without YouTube cookies.

## Verified workaround from session

Chris Williamson YouTube was blocked by bot-check, but an official Facebook repost downloaded successfully with `yt-dlp`, then rendered as a 1080x1920 42s Short. Future automation should make this official-repost search a first-class fallback rather than manual work.

## Implementation pitfall: page URLs are not direct media URLs

Do **not** raw-download Facebook/YouTube page URLs with `urllib` just because they appear in `fallback_source_url`; that saves HTML into `source.mp4` and later ffmpeg fails with `moov atom not found`. Only `urllib` direct media/archive URLs (`.mp4`, `.mov`, `.webm`, archive.org direct downloads). For Facebook creator repost URLs, run them through `yt-dlp`/the source downloader and verify with `ffprobe` before rendering. Also dedupe remote-only manifests by source URL so the cron does not retry the same blocked YouTube source once per clip window.
