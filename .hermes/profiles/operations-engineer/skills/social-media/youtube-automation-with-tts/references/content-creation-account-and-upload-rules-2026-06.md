# Content creation account and upload rules — 2026-06

Use this reference for the user's faceless YouTube newsletter pipeline, Viral Clip Radar uploads, and future self-improving content loop.

## Account roles

- **Read newsletter source emails from `fareed320@gmail.com`**.
  - Canonical profile: `personal-secondary`.
  - Legacy alias: `fareed320` may point to `personal-secondary`.
  - Use for Gmail newsletter source reads and post-processing cleanup.

- **Use `trapiistan@gmail.com` for Hermes Workspace/calendar coordination**.
  - Canonical profile: `trapiistan`.
  - Use for Google Calendar events that communicate production schedules and cron/upload timing.

- **Use the correct YouTube channel token for uploads**.
  - `classicalechos` YouTube token owns **Classical Echos**.
  - `trapiistan` YouTube token owns **Sosai Oyama**.
  - Before editing an existing video, verify `channels.list(mine=true)` and `videos.list(..., id=VIDEO_ID)` show the expected channel/video.
- Live YouTube metrics must be fetched using the same OAuth account/token that uploaded the video, not a generic API key from a different account. The YouTube Data API is already enabled; use the lane's upload token/account for `videos.list` and analytics snapshots so private/unlisted/public visibility and channel ownership line up.

## Upload privacy rule

- The user corrected the default: **do not upload YouTube automation outputs as private by default**.
- Approved content automation lanes should upload `public` unless the user explicitly requests private/unlisted review mode.
- The shared uploader should default to `public`.
- If the user asks for a backlog with future releases, prefer cron/calendar scheduling that uploads publicly at the chosen time.
- Only use YouTube `publishAt` when explicitly desired; explain that YouTube's API represents scheduled releases as private until publish time.

## Required YouTube scopes

- `youtube.upload` for uploads.
- `youtube.force-ssl` for existing video status/privacy/metadata edits. `youtube.upload` alone is insufficient to change a previously uploaded video from private to public.
- `youtube.readonly` for verifying channel/video ownership and status.
- `yt-analytics.readonly` for performance loops and self-improving channel analytics.

## Faceless newsletter pipeline

- Canonical account flow: read newsletter/source emails from `fareed320@gmail.com` via Workspace profile `personal-secondary`, then upload the produced Daily Stoic/faceless videos to the **A F** YouTube channel using the explicit fareed320 token path (`/opt/data/secrets/youtube-fareed320/youtube_upload_token.json`) and expected channel ID `UCX_nUA3Yr9VR884DNanyMYA`.
- Do **not** infer the YouTube destination from inbox ownership or inherited environment tokens. A F is the fixed faceless primary; Classical Echos and Sosai Oyama remain separate Viral Radar primary/failover channels.
- One real newsletter email = one video.
- Use actual newsletter body content, not placeholder topics.
- Visuals should use Pexels stock pictures/videos and Hugging Face visuals for now; Sora is not the default because of cost.
- Use ElevenLabs voiceover.
- After upload returns a verified YouTube `video_id`, delete/trash the source newsletter email and delete local rendered media to save VPS space.
- Keep durable metadata/logs/manifests.

## Viral Clip Radar distinction

- Viral Clip Radar does **not** need stock footage for clipping videos.
- For source-acquisition failures, follow `references/viral-radar-source-acquisition-fallbacks-2026-06.md`: fix and smoke-test the current downloader first before jumping to paid clipping APIs, then require cookies/proxy/local media/provider credentials only if YouTube still blocks the VPS.
- It scouts long-form creator videos, clips them, adds captions/transcription, reframes to portrait 9:16 for smartphone/Shorts/Reels distribution, and uploads.
- Current user instruction for influencer/creator Viral Radar clips: upload to **Classical Echos** using `/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json` unless the user explicitly changes the lane.
- Use Google/YouTube APIs for discovery and account verification. For actual media acquisition, **do not default to raw VPS/headless YouTube downloading** when YouTube bot checks appear; prefer compatible automation sources in this order: cached/local source MP4, archive/direct MP4 fallback URL, official clipping/import provider API export (OpusClip first, then Choppity/Vizard/Klap/MuAPI as configured), or Google Drive/source-file MP4. Only use direct `yt-dlp`/YouTube source downloads when explicitly enabled for that run (for example with a clear opt-in flag such as `VIRAL_RADAR_ALLOW_DIRECT_YOUTUBE_DOWNLOAD=1`) and the source is legally/technically downloadable.
- Provider credential aliases worth checking before reporting a blocker: `OPUS_CLIP_API_KEY`, `OPUSCLIP_API_KEY`, `OPUS_API_KEY`, `OPUS_ORG_ID`, `OPUSCLIP_ORG_ID`, `CHOPPITY_API_KEY`, `CHOPPITY_KEY`, `VIZARD_API_KEY`, `VIZARD_KEY`, `KLAP_API_KEY`, `KLAP_KEY`, `MUAPI_API_KEY`, `MUAPI_KEY`.
- Missing provider credentials should be reported as an actionable `needs_provider_credentials`/setup state, not as a crash or a generic source-download failure.
- Do not conflate this with the faceless newsletter stock-footage workflow.

## Reporting style

- For Discord reports about accounts, videos, and scheduled uploads, avoid Markdown tables.
- Use short bold bullets with concrete IDs/URLs and verification status.
