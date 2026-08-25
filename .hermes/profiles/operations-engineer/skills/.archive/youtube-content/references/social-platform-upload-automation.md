# Social Platform Upload Automation Notes

Use this when a user wants autonomous posting of generated clips to YouTube Shorts, Instagram Reels, TikTok, or via Opus Clip.

## Core principle

Do **not** store platform passwords or treat a shared Gmail login as the automation credential. Prefer revocable OAuth tokens, API keys, or a user-completed browser session. Browser login can be a pilot path, but API/OAuth is the durable path.

## YouTube

- Official upload path: YouTube Data API `videos.insert`.
- Required user OAuth scope: `https://www.googleapis.com/auth/youtube.upload`.
- Service accounts are not sufficient for normal channel uploads.
- Uploads from API projects created after 2020-07-28 are forced to private until the API project passes YouTube compliance/audit.
- Good pilot shape: render clip -> upload `private` -> report real video ID/URL -> user manually reviews/publishes or app later completes audit.

Suggested secret paths/env:

```bash
YOUTUBE_UPLOAD_CLIENT_SECRET=/opt/data/secrets/youtube-oauth-client.json
YOUTUBE_UPLOAD_TOKEN=/opt/data/.hermes/youtube_upload_token.json
YOUTUBE_COOKIES=/opt/data/secrets/youtube-cookies.txt
```

## Instagram

- Official publishing path: Instagram/Meta Graph API content publishing.
- Supports Reels/videos for Instagram professional accounts.
- Requirements commonly include a Meta app, professional IG account, connected Facebook/Page flow depending on login mode, and permissions such as `instagram_business_content_publish` or `instagram_content_publish`.
- Media must be publicly reachable by Meta via `video_url`, or uploaded through Meta's resumable upload flow where supported.
- Rate limit: Instagram docs commonly cite 100 API-published posts per 24-hour moving window per account.

## TikTok

- Official publishing path: TikTok Content Posting API.
- Required scope for direct posting: `video.publish`.
- Supports `FILE_UPLOAD` and `PULL_FROM_URL` sources.
- Must query creator info first to get allowed privacy levels/settings.
- Unreviewed/unaudited API clients are restricted to private visibility until TikTok audit; this is still useful for pilots.
- Direct post init endpoint pattern: `/v2/post/publish/video/init/`; upload URL is time-limited.

## Opus Clip

- Opus Clip API exists but is closed beta / limited to high-volume paid annual users.
- If the user has API access, prefer `OPUSCLIP_API_KEY` and API workflows.
- If no API access, use Opus as a browser-session experiment only: user logs in and connects social accounts manually, then agent tests whether it can submit URLs, monitor jobs, download clips, or use Opus's own publisher.
- Do not promise stable Opus browser automation until login, 2FA/captcha, file upload, credits, and export controls are verified in the live account.

## Practical strategy

1. Build local clipping/rendering first so final MP4 artifacts exist independent of any platform.
2. If YouTube is the current blocker, do **not** keep centering YouTube or Zapier. Pivot to TikTok/Instagram upload pilots while keeping YouTube private upload as an optional fallback.
3. TikTok is often the cleaner first non-YouTube pilot because the Content Posting API supports `FILE_UPLOAD` from a rendered MP4; use `SELF_ONLY` until app audit/approval is complete and query creator info before execution.
4. Instagram Reels is a strong second pilot, but requires an Instagram professional account plus a public `video_url` reachable by Meta unless a resumable-upload path is implemented.
5. Treat Opus browser automation as a pilot, not the primary production mechanism, unless API access is available.
6. Add a third-party social-posting broker only if direct TikTok/Instagram OAuth/API setup is too slow or unreliable. If the user explicitly drops a broker/Zapier idea, remove it from the plan instead of continuing to recommend it.
7. For browser-based login attempts, ask the user to complete login/2FA/captcha in-session; never ask for or store account passwords.
8. Keep all social publishing tests private/unlisted/draft/self-only until the user verifies output quality and platform compliance.

See also `references/tiktok-instagram-native-upload-pivot.md` for the session-specific native TikTok/Instagram pivot pattern, credential handling, and dry-run script shape.

## Third-party broker option

A unified posting API/provider (for example Buffer/Ayrshare/Make/Zapier-style brokers) can be the fastest production route for multi-platform posting. The tradeoff is another paid vendor and account-connection step, but it keeps Hermes from brittle browser clicking and platform-specific OAuth maintenance.

### Native-first plus broker-fallback launch pattern

When the user wants a "bulletproof" clipping-to-social publishing stack, recommend a hybrid rather than choosing only native APIs or only a SaaS broker:

1. Keep **native YouTube upload** as the direct baseline: YouTube Data API `videos.insert`, user OAuth token, `youtube.upload` scope, private-first pilot.
2. Add **one** low-friction broker as the first paid fallback, not several at once. In 2026 research, good first candidates were Upload-Post or Postproxy for low-cost API-first proof-of-life; keep Ayrshare as the more mature/higher-cost fallback if the cheaper provider fails on account connection, video upload, or per-platform status reporting.
3. Use native TikTok/Instagram only when broker coverage is insufficient or direct control is required; both need app/OAuth setup and may require review/audit before public automated posting.
4. Treat Opus Clip as optional clipping/autopost experimentation unless the account has API beta access. Without API access, use a supervised browser session only after the user completes login/2FA/captcha.
5. Create a project-local credential preflight script before attempting uploads. It should load `.env`, check for required files/env vars, and print only `set/present/missing` status — never secret values.
6. Pilot order: render local MP4 -> native YouTube private upload -> broker upload/draft/private to YouTube/TikTok/Instagram -> compare returned IDs, status polling, and failure detail -> only then consider public posting.

Suggested project env template keys for this class of workflow:

```bash
YOUTUBE_UPLOAD_CLIENT_SECRET=/opt/data/secrets/youtube-oauth-client.json
YOUTUBE_UPLOAD_TOKEN=/opt/data/.hermes/youtube_upload_token.json
YOUTUBE_COOKIES=/opt/data/secrets/youtube-cookies.txt
UPLOAD_POST_API_KEY=
POSTPROXY_API_KEY=
AYRSHARE_API_KEY=
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TIKTOK_ACCESS_TOKEN=
META_APP_ID=
META_APP_SECRET=
META_ACCESS_TOKEN=
INSTAGRAM_USER_ID=
OPUSCLIP_API_KEY=
RESIDENTIAL_PROXY=
```

When advising purchases/subscriptions, verify current pricing/features from vendor pages first, then recommend buying/testing **one** broker at the start of the billing month and keeping direct YouTube OAuth as an independent fallback. Do not imply shared Gmail credentials solve cross-platform automation; Gmail login, YouTube OAuth, Opus sessions, Meta tokens, and TikTok tokens are separate credentials.
