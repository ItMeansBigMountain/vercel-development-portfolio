# Manual YouTube clip source-blocker workflow

Use when a user gives a YouTube URL and asks to clip/upload it, but the normal downloader cannot acquire the source.

## Durable workflow

1. Check whether a `CLIP_PLANS/*/clip_manifest.json` already exists for the YouTube video ID. A manifest can already contain reviewed clip windows even when the actual source MP4 is missing.
2. Check upload logs before rendering/uploading so the same source/title is not duplicated.
3. Try the source acquisition ladder in order:
   - `yt-dlp` with the configured Viral Radar cookies file when present.
   - `pytubefix` / `pytube` fallback clients.
   - OAuth-capable `pytubefix` only if appropriate for the account/session.
   - External provider preflight for configured non-Opus providers.
4. If all source acquisition paths are blocked, report the exact actionable unblockers instead of pretending the clip can be rendered:
   - local/Drive MP4 source file,
   - fresh working YouTube cookies from a logged-in browser/session,
   - residential proxy for downloader traffic,
   - configured non-Opus clipping provider key.
5. Once a source is available, render the existing manifest’s planned windows to vertical Shorts, verify with `ffprobe`, then upload through the Viral Radar uploader using the explicit lane token/failover rules.

## Pitfalls

- Do not treat an existing manifest as proof that the source file or exports exist. Search for the MP4s and verify files before upload.
- Do not loop on the same downloader failure. After cookies + Python fallbacks + provider preflight have failed, stop and ask for one of the unblockers.
- Do not add stock footage to Viral Radar creator clips; this lane clips the actual source video.
