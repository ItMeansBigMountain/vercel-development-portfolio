# Social Platform Onboarding and Credential Operations

Updated: 2026-08-25

## Objective

Operate one unified `#content-creation` lane for original and curated content, Parrot AI assets, editing, scheduling, publishing, analytics, community management, and multi-platform growth.

## Security architecture

- Prefer each platform's official OAuth/API flow over storing account passwords.
- Keep app client secrets and user refresh tokens out of Git, Discord, prompts, logs, and ordinary project files.
- Store platform credentials under `/opt/data/secrets/social/<platform>/<account>/` with directories mode `700` and files mode `600`.
- Keep a non-secret registry under the project with platform, account label, platform user ID, granted scopes, token expiry, refresh expiry, health status, and last identity probe.
- Store access/refresh tokens atomically. When refresh endpoints rotate refresh tokens, replace the old token in the same transaction.
- Create one stateful token-health cron that checks expiry without printing tokens, refreshes proactively, verifies account identity, and reports only material failures to `#content-creation`.
- Every publisher must verify destination identity before upload and record returned post ID/URL before deleting local media.
- Browser-only credentials, where unavoidable, belong in a protected secret file and browser profile; never put passwords in Git or Discord. MFA remains interactive.
- Revoke and reauthorize on scope changes rather than silently assuming old grants cover new publishing capabilities.

## Platform routes

### YouTube

- Current status: existing channel-specific OAuth upload tokens and upload/metrics automation.
- Auth: Google OAuth 2.0 user authorization; YouTube does not support service accounts for channel actions.
- Preserve separate token files per channel/account and verify channel ID before every upload/delete/metrics action.
- Official reference: https://developers.google.com/youtube/v3/guides/authentication

### TikTok

- Recommended path: TikTok for Developers + Content Posting API, using OAuth authorization code flow.
- Access token: 24 hours. Refresh token: 365 days. TikTok may return a new refresh token during refresh; save the newest value.
- Publishing scopes/app review must be completed before unattended direct posting.
- Official reference: https://developers.tiktok.com/doc/oauth-user-access-token-management

### Instagram and Facebook

- Recommended path: Meta app + Instagram professional account and linked Facebook Page; use official content publishing endpoints.
- Exchange the one-hour Instagram token for a long-lived token valid for 60 days. Keep app secret server-side only and refresh before expiry.
- Request only the publishing, identity, page, and insights scopes required by the approved workflow; app review/business verification may be required.
- Official reference: https://developers.facebook.com/documentation/instagram-platform/reference/access_token

### Threads

- Recommended path: Meta Threads API with its own explicit OAuth scopes and token lifecycle, stored separately from Instagram even if the same Meta app/account is used.
- Verify current publishing and insights permissions during onboarding; do not assume Instagram grants cover Threads.

### LinkedIn

- Recommended path: LinkedIn developer app + 3-legged OAuth. Personal posting uses member-social permissions; organization posting requires organization permissions and app/product approval.
- Access tokens currently have a 60-day lifespan. Refresh-token availability depends on approved products/partner access; plan a user reauthorization fallback.
- Official reference: https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow

### X

- Use the official X developer API and OAuth 2.0 user-context flow where the account tier permits posting and media upload.
- Verify current pricing and write limits before onboarding; do not assume publishing is free.
- Store OAuth client credentials and user refresh token separately from browser login credentials.

### Reddit

- Use a registered Reddit application and OAuth user authorization for submissions and moderation. Keep subreddit rules and self-promotion limits in the publishing policy.
- Verify scopes and account identity before enabling autonomous posting.

### Pinterest

- Use Pinterest's official developer app/OAuth and Pins publishing API. Record board IDs in the non-secret registry.

### Bluesky

- Prefer app passwords or OAuth according to current official AT Protocol support. Store an app-specific credential, never the primary account password.

### Parrot AI

- Browser-first creative provider, not a social publishing identity.
- Store login only in the protected Parrot secret/browser profile when needed; MFA remains interactive.
- Always download generated outputs into the durable project before publishing. Do not rely on Parrot-hosted URLs as the only copy.
- Do not depend on unattended Parrot production until generation and export are proven end-to-end.

## Shared publishing contract

Every platform adapter should implement:

1. `health` — expiry, scopes, identity, and harmless API probe.
2. `refresh` — atomic token refresh with rotated-refresh-token handling.
3. `upload_media` — resumable upload where supported.
4. `publish` — caption/title/alt-text/audience/disclosure controls.
5. `verify` — retrieve the post and confirm public/account identity.
6. `metrics` — platform-native reach, watch time, retention, engagement, and follower conversion where available.
7. `delete` — disabled by default and separately gated.

Write a cross-platform publication ledger with one row per platform containing source asset hash, account ID, post ID, URL, published timestamp, status, and analytics checkpoint. Never reuse one platform's token for another account or brand.

## Recommended onboarding order

1. TikTok — strongest immediate vertical-video expansion target.
2. Instagram Reels + Facebook Reels — shared Meta app and broad reach.
3. Threads — text/context distribution around published videos.
4. LinkedIn — business, cloud-career, tutoring, and agentic-AI content.
5. X — only after current API pricing/write access is confirmed.
6. Pinterest — evergreen visual discovery.
7. Reddit — community-specific, rules-first distribution.
8. Bluesky — lightweight text/social syndication.

## Operational crons

- Token health: daily; silent when healthy; proactive refresh based on each platform's expiry.
- Content calendar: daily planning brief in `#content-creation`, only when decisions are needed.
- Publisher: platform-specific windows and rate limits; record post IDs before cleanup.
- Metrics learning: daily or weekly depending on API limits; report only meaningful winners/declines/actions.
- Credential review: monthly; verify app review status, scopes, expiry horizon, and broken adapters.

## Native APIs versus unified scheduler

Start with native APIs for YouTube, TikTok, and Meta so identity, analytics, and token behavior are explicit. Evaluate a self-hosted unified scheduler such as Postiz only if native app-review burden becomes the bottleneck. A unified service reduces adapter work but adds another privileged credential store and operational dependency; it should not become the sole copy of tokens or media.
