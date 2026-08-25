---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
platforms: [linux, macos, windows]
---

# YouTube Content Tool

## When to use

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, wants to extract and reformat content from any YouTube video, or wants to discover trending/viral YouTube videos for a content/clipping workflow. Transforms transcripts into structured content.

Extract transcripts from YouTube videos and convert them into useful formats.

## Setup

```bash
pip install youtube-transcript-api
```

## Helper Script

`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

## Hermes workflow shortcut

When the user shares a YouTube URL and wants transcripts for Viral Radar or the faceless YouTube channel, do **not** ask them to paste chunks into Discord. Use the durable wrapper:

```bash
python3 /opt/data/scripts/youtube_transcript_ingest.py "YOUTUBE_URL" --creator "Creator Name" --title "Short title"
```

This writes transcript artifacts under `/opt/data/HeRmEz/projects/viral-clip-radar/CLIP_PLANS/` and mirrors source metadata into `/opt/data/HeRmEz/projects/faceless-youtube-channel/STATE/source_transcripts/` so both Viral Radar and the faceless channel can use the source. If transcript fetch fails because YouTube captions are disabled/private or YouTube blocks the VPS as a bot, ask for the video URL plus browser cookies, a transcript, or a local media file instead of making the user manually chunk by default. See `references/youtube-content/hermes-youtube-transcript-ingestion-wrapper-2026-06.md` for the exact wrapper behavior and fallback pattern.

## Workflow

### Supplied video transcript workflow

1. **Fetch** the transcript using the helper script with `--text-only --timestamps`.
2. **Validate**: confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, tell the user the video likely has transcripts disabled.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

### Trend discovery / clipping workflow

When the user wants viral/trending YouTube candidates rather than a single supplied video:

1. Check `references/youtube-content/youtube-data-api-trend-ingestion.md` for credential modes and the minimal verification probe.
2. Prefer `YOUTUBE_API_KEY` for public trend reads, but use `GOOGLE_APPLICATION_CREDENTIALS` or an explicit service-account JSON path when the user says to use Google service-account credentials.
3. Always run a cheap `videos.list(chart=mostPopular, maxResults=1-3)` probe before building the larger pipeline.
4. If Google returns `accessNotConfigured`, report that exact API enablement problem for the credential's project; do not imply the key is bad or fabricate trend data.
5. For clipping channels, filter/rank candidates by duration, recency, view velocity, comment intensity, creator reach, keyword relevance, and clip density; preserve source URLs and attribution.
6. Use a physical candidate workspace pattern (`CLIP_PLANS/<candidate>/`) for metadata, transcripts, edit notes, and approved clip specs; see `references/youtube-content/youtube-data-api-trend-ingestion.md` for the long-form viral clipping project shape.
7. Require transformative framing for clipping channels — commentary, captions, context, analysis, or other added value. Do not design workflows around lazy reuploading.
8. For channel-private actions such as upload, private channel reads, or YouTube Analytics, switch to user OAuth rather than assuming service accounts work.

### Cross-platform clipping sources

When the user wants to clip content from non-YouTube platforms and publish transformed clips to YouTube, use `references/youtube-content/cross-platform-clipping-sources.md`. For Rumble specifically: prefer accessible public listing pages first, preserve source attribution, create a review workspace before download/edit/upload, support yt-dlp browser-cookie retries for gated pages, and use 9:16 cropping as `scale=-2:1920,crop=1080:1920` for landscape sources.

### Clip-and-upload pilot workflow

When the user asks for proof that we can clip and upload from a supplied video, use `references/youtube-content/clipping-upload-pilot.md` before promising success. Preflight source download/transcript access and YouTube user OAuth upload token. For this user's approved automation lanes, upload public unless they explicitly request private/unlisted review; if cloud IP/bot checks block YouTube/Rumble download, continue by saving workspace logs and request cookies or a local source file; do not claim a clip/upload succeeded without a real exported file or uploaded video ID.

### Social platform upload automation

When the user asks to automate posting clips through YouTube, Opus Clip, Instagram, TikTok, or a shared Gmail login, use `references/youtube-content/social-platform-upload-automation.md`. Prefer revocable OAuth/API credentials over stored passwords, treat browser login as a supervised pilot path, and test with private/unlisted/draft uploads before promising autonomous public publishing.

### Faceless timestamp-to-image workflow

When the user wants to reproduce a Claude Code/Higgsfield faceless YouTube workflow using Hermes instead, use `references/youtube-content/faceless-timestamp-image-higgsfield.md`. The core pattern is human voiceover → timestamped transcript → one MS-Paint-style image prompt per timestamp → Higgsfield generation → local images named by timestamp for timeline syncing.

### Faceless YouTube automation on VPS

When the user wants to build a faceless channel rather than summarize a supplied video, use `references/youtube-content/faceless-youtube-automation-vps.md`. Default to a headless VPS pipeline with a Vercel/dashboard surface, Pexels/Hugging Face visuals, ElevenLabs narration, public YouTube uploads for approved lanes, and user OAuth for `youtube.upload`. If a stored YouTube token fails with Google's `deleted_client`, do not keep retrying the old token; create/provide a replacement OAuth client with YouTube Data API v3 enabled and `http://localhost:5000/` redirect.:5000/` as an authorized redirect URI, then run a fresh one-time OAuth flow.

When the user asks to become better at virality, tune upload timing/frequency, improve faceless graphics, or replace Opus Clip with free/API-driven options, use `references/youtube-content/viral-growth-content-automation-2026-06.md`. Apply the learning into project files, not just chat: shared playbook, per-project README/workflow pointers, dry-run upload tests, and explicit cleanup-after-success rules.

When the user asks to activate content pipelines with cron or scheduled uploads, use `references/youtube-content/cron-activated-content-pipelines-2026-06.md`: wrap project pipelines in `/opt/data/scripts/` entrypoints, schedule them for Central-time peak windows, use public uploads for approved lanes unless private/unlisted is explicitly requested, add daily `.done` duplicate protection, delete media only after confirmed upload IDs, and verify with real direct execution plus cleanup checks.

For the user's HeRmEz workspace, also use `references/youtube-content/hermez-shared-youtube-upload-method-2026-06.md`: it captures the canonical shared OAuth/upload scripts, secrets path, headless PKCE verifier persistence, public-upload default for approved automation lanes, production-over-setup proof requirements, upload log locations, and the current YouTube automation project lanes. For account selection, consult `/opt/data/HeRmEz/projects/_ops/google-email-profiles.json`: default faceless YouTube/Viral Radar uploads to the Hermes agent account (`hermes-agent` / `trapiistan@gmail.com`); use `classicalechos` only after niche/account review; do not default to the user's personal accounts for uploads.

If YouTube is blocking the clipping project and the user wants TikTok/Instagram instead — especially if they explicitly drop Zapier/broker tooling — use `references/youtube-content/tiktok-instagram-upload-pivot-2026-06.md`: render MP4s first, pilot TikTok native `FILE_UPLOAD` with `SELF_ONLY`, then Instagram Reels via public `video_url`, and keep YouTube/brokers as fallback only.

### Zapier-free clip review bridge

When Zapier webhooks are unavailable, credentials are not ready, or the user is just exploring automation, do not block the clipping project on Zapier. Use `references/youtube-content/zapier-free-clip-review-bridge.md`: generate local JSON/CSV/Markdown review packets from rendered MP4s so the user can import to Notion/Sheets, paste to Discord/email, or manually upload while the clip pipeline matures.

### VPS download + manual-upload clipping delivery

When the user asks for finished clip files but will upload manually, use `references/youtube-content/vps-youtube-clipping-delivery.md`. It captures the proven workflow: use a legitimate Internet Archive mirror when direct YouTube downloads are bot-blocked, extract transcript-driven segments, render captioned 9:16 MP4s from a manifest when available, verify with `ffprobe` and preview frames, clean disposable local media after backing up metadata, then deliver `MEDIA:/absolute/path.mp4` files.

For VPS clipper projects, make deletion of downloaded source videos the default after successful clip render/verification. Keep finished MP4 clips for manual upload, but delete sources from known disposable cache directories (for example `SOURCES/`, `TMP/`, `DOWNLOADS/`, `RAW_VIDEO/`) unless an explicit debug flag such as `--keep-source` is passed. Do not auto-delete arbitrary user-supplied files outside those cache folders. For a reusable implementation pattern, use `references/youtube-content/vps-clipper-self-cleaning.md`.


## Error Handling

- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **Dependency missing**: run `pip install youtube-transcript-api` and retry.
