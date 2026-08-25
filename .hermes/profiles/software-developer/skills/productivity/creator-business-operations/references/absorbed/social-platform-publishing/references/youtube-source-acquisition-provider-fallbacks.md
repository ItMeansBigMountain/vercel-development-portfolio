# YouTube source acquisition without direct VPS downloading

Use this when Viral Radar / creator clipping hits YouTube bot verification such as `Sign in to confirm you’re not a bot` from `yt-dlp` or another headless downloader.

## Durable lesson

Do not keep retrying raw YouTube downloads from the VPS. Treat bot verification as a signal to switch acquisition mode.

Preferred order:

1. **Local/cached source MP4** already present in the project.
2. **Archive/direct MP4 fallback URL** that can be fetched with normal HTTP.
3. **Official clipping/import API** that accepts a public video URL and returns exportable MP4 clips:
   - OpusClip first when configured.
   - Choppity, Vizard, Klap, or MuAPI as alternatives after their endpoint contract is verified.
4. **Google Drive/source-file MP4** supplied by the user, then clip locally.
5. **Direct YouTube download** only with explicit opt-in for that run and appropriate cookies/proxy/authorized access.

## Provider env aliases to check

- OpusClip: `OPUS_CLIP_API_KEY`, `OPUSCLIP_API_KEY`, `OPUS_API_KEY`; org: `OPUS_ORG_ID`, `OPUSCLIP_ORG_ID`.
- Choppity: `CHOPPITY_API_KEY`, `CHOPPITY_KEY`.
- Vizard: `VIZARD_API_KEY`, `VIZARD_KEY`.
- Klap: `KLAP_API_KEY`, `KLAP_KEY`.
- MuAPI: `MUAPI_API_KEY`, `MUAPI_KEY`.

## Reporting pattern

If no provider key/source is configured, report a setup state such as:

```json
{
  "status": "needs_provider_credentials",
  "next_step": "Set OPUS_CLIP_API_KEY or provide a local/Drive MP4 source; direct yt-dlp is intentionally disabled."
}
```

Do not report it as a mysterious render/upload failure. The render/upload path has not been reached.

## Cron/pipeline behavior

- Keep source acquisition failures separate from render/upload failures.
- A missing provider key should not create a Python traceback or crash loop in cron; return a clean actionable status.
- Preserve provider job IDs/state files for later polling when an API returns `submitted`/`pending` instead of an immediate MP4.
