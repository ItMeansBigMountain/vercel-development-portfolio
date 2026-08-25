# Viral Radar no-vendor influencer source acquisition — 2026-06

Use this when Viral Radar needs to clip influencers but YouTube source downloads hit cloud-IP bot checks and the user does not want external clipping vendors.

## User correction

The user clarified that Viral Radar cron jobs must clip and upload videos, not only identify sources. They also told us to leverage Hermes' browser/web ability and keep doing the no-vendor method that worked.

## Working pattern from this session

1. Keep the YouTube Data API seeding step for metadata and candidate queue discovery.
2. When `yt-dlp` against YouTube returns "Sign in to confirm you're not a bot," do **not** stop at discovery-only.
3. Search the web for official or creator-controlled reposts:
   - `site:facebook.com <creator> <title keywords> video`
   - `site:facebook.com/<official-page>/videos <topic>`
   - LinkedIn and owned sites can provide transcripts/metadata, but Facebook video URLs were the practical downloadable source in this run.
4. Prefer official creator/page reposts over fan pages. Accept near-official brand/community pages only when they are part of the creator ecosystem and the manifest clearly attributes the source.
5. Download the official Facebook video with yt-dlp:

```bash
mkdir -p SOURCES/<creator-source-slug>
yt-dlp -f 'bv*+ba/b' --merge-output-format mp4 \
  -o 'SOURCES/<creator-source-slug>/source.%(ext)s' \
  --no-playlist --restrict-filenames --force-ipv4 '<facebook-video-url>'
```

6. Seed a normal `clip_manifest.json` with:
   - `creator`
   - `source_title`
   - `source_url` = official repost URL
   - `source_file` = `SOURCES/<creator-source-slug>/source.mp4`
   - `source_attribution`
   - one or more clips with hook/context overlays
7. Run the existing daily uploader with the manifest forced:

```bash
FORCE_UPLOAD=1 \
VIRAL_RADAR_MANIFEST=/opt/data/HeRmEz/projects/viral-clip-radar/CLIP_PLANS/<plan>/clip_manifest.json \
VIRAL_RADAR_MAX_SOURCE_ATTEMPTS=1 \
python3 /opt/data/scripts/viral_radar_daily_upload.py
```

8. Verify a real YouTube `video_id`/URL before claiming success.

## Confirmed creator examples

- Alex Hormozi official Facebook source -> public upload succeeded.
- Kinobody official Facebook source -> public upload succeeded.
- Chris Williamson official Facebook source -> public upload succeeded.
- GG33 Wisdom Facebook source -> public upload succeeded.
- Capital Club Community / Nate Belmar Facebook source -> public upload succeeded.

## Queue/rotation rules

- Do not silently fall back to Huberman/NASA/unknown evergreen clips when the user asked for all influencers.
- Exclude Zerkaa/ZerkaaPlays unless the user explicitly re-adds them.
- Track enriched upload logs with creator/source metadata so the queue can avoid repeating the same influencer.
- If all non-evergreen influencer sources fail, report `blocked_source_all_candidates` nonzero with attempted creator URLs, rather than uploading filler.

## Pitfalls

- Browser login to Google may be blocked as "browser or app may not be secure" in remote browser contexts; do not persist that as a permanent impossibility. Try official repost sources first.
- Pytubefix OAuth may require an interactive device-code flow. If used, keep stdin open and complete auth before pressing Enter.
- Do not save user-provided passwords or account credentials in skills, memory, files, or logs.
