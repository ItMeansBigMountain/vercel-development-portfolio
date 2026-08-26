# tweetBetweenTheLines deterministic archive schema and fixture plan

Last updated: 2026-08-25

## Scope and confidence

This document turns the OAuth/archive research in `PLATFORM_OAUTH_ARCHIVE_MATRIX.md` into deterministic parser requirements. It separates:

- API-access data: OAuth/API records fetched from official developer APIs after least-privilege consent.
- User-uploaded archives: files the user requests directly from the platform and uploads to tweetBetweenTheLines.
- Officially documented facts: cited first-party developer/help/privacy documentation.
- Representative schemas: deterministic adapter targets derived from official export categories where docs name categories, plus synthetic/redacted fixtures for parser tests. Unless a platform publishes exact archive filenames/fields, the exact path map must stay `sample_required` until validated against a consenting user's current export.

The product must not infer schemas with AI at runtime. Unknown files are quarantined, versioned, and require a parser update with fixtures before ingestion.

## App-level archive admission contract

These are tweetBetweenTheLines upload rules, not platform limits:

| Rule | v1 decision | Reason |
|---|---|---|
| Accepted upload container | `.zip` only | Current domain guard `inspectArchive` supports `format: 'zip'`; convert `.tgz`, `.tar`, or raw folders out-of-band only after a new sandbox/test gate. |
| Accepted extracted data files | `.json`, `.csv`, `.txt`, `.html` as parser-specific inputs; media files metadata-only unless a reviewed parser needs them | Most official account exports are JSON/CSV/HTML/text or ZIP bundles; raw media analysis is out of scope for first deterministic launch. |
| Max compressed archive | 250 MB | Matches `packages/domain/src/connectors.ts` guard. |
| Max extracted total | 1 GB | Matches zip-bomb guard. |
| Max single extracted file | 50 MB | Prevents pathological parser memory use. |
| Max entries | 10,000 | Keeps mobile/backend progress bounded. |
| Max nested archive depth | 1 | Prevents recursive archive bombs. |
| Symlinks/devices/absolute paths/`..` | Reject | Path traversal and host-file escape prevention. |
| Malware scan | Must be `clean` | Import fails closed when scan is unavailable. |
| Runtime | Unprivileged, read-only archive mount, no network, no content execution | Keeps uploaded archives untrusted. |

## Provenance and versioning strategy

Every import emits a manifest before parsing:

```json
{
  "schema_version": "archive-manifest@1",
  "platform": "x_twitter",
  "source_kind": "user_uploaded_archive",
  "archive_sha256": "<sha256 of original zip>",
  "parser_version": "x_twitter_archive@1",
  "source_documentation_urls": ["https://help.x.com/en/managing-your-account/how-to-download-your-x-archive"],
  "consent_receipt_id": "consent:<digest>",
  "requested_categories": ["posts", "likes", "follows"],
  "accepted_categories": ["posts", "likes", "follows"],
  "quarantined_files": [],
  "generated_at": "2026-08-25T00:00:00Z"
}
```

Parser schema versions are named `<platform>_archive@<integer>` and are immutable. A new platform export layout, renamed file, or field meaning change gets a new schema version plus a synthetic fixture and, where available, a redacted consenting-user fixture. Normalized event IDs use `event:<tenant>:<subject>:<sourceId>:<sourceRecordId>` and must remain stable across re-imports. Store raw archive object references separately from normalized features; deletion removes raw files, normalized events, derived features, cached exports, queue jobs, and source encryption keys, leaving only a non-personal tombstone.

## Platform map

| Platform | First-party sign-in / linked-account OAuth | Review/scopes gate | User archive request steps | Deterministic archive target | Field map for initial parser | Status |
|---|---|---|---|---|---|---|
| Google / YouTube | Google OAuth 2.0 web/native; native apps use PKCE.[1][2] | Sensitive/restricted scopes may require Google verification; YouTube calls consume quota.[3][4] | Google Account → Data & privacy → Download your data / Takeout → select products → export.[5] | Takeout `.zip` imported as product folders; YouTube watch/search/history files are sample-validated before enabling. | `posts`: uploaded/commented public YouTube items where present; `likes`: liked videos if present; `searches`: YouTube search history; `watch_history`: YouTube watch history; `ads/interests`: Google ad topics only if present and explicitly consented. | `supported_api` for deltas/metadata; `supported_archive_import` after sample validation. |
| Facebook | Facebook Login.[7] | Advanced permissions require App Review; request only needed permissions.[8][9][10] | Accounts Center / Facebook help flow to export a copy of Facebook information.[11] | Meta archive `.zip`, JSON preferred; exact filenames are not officially stable. | `posts`: own posts; `likes`: reactions/likes; `follows`: friends/pages/groups following where present; `searches`: search history if included; `ads/interests`: ads topics/interests if included. | `manual_import_first`; `sample_required` for exact schema. |
| Instagram | Instagram API with Instagram Login / Basic Display where approved.[13][14] | Meta App Review for advanced access.[8][9] | Instagram Help flow to review/export information.[12] | Meta/Instagram archive `.zip`, JSON preferred; exact filenames are not officially stable. | `posts`: media captions/comments by user where present; `likes`: liked posts/comments; `follows`: following/followers; `searches`: recent searches; `ads/interests`: ads topics if present. | `manual_import_first`; `sample_required` for exact schema. |
| Threads | Threads developer docs exist.[15] | Product/app review; no broad personal-history OAuth promise. | If Meta export includes Threads data, treat it as a Meta archive sub-product only after schema confirmation.[11][15] | No enabled parser until official export sample confirms paths. | `posts` only after sample; no likes/follows/search/watch/ads claims yet. | `blocked_or_restricted` for history. |
| X / Twitter | OAuth 2.0 authorization-code with PKCE; `offline.access` controls refresh-token issuance.[16] | Paid/reviewed tier may be required; rate limits are tier-sensitive.[17][19] | X help flow: account settings → request archive → download `.zip` after email/notification.[18] | X archive `.zip`; representative paths include `data/tweets.js`, `data/like.js`, `data/following.js`, `data/follower.js`, `data/ad-engagements.js`, and manifest/account files, but exact fields must be sample-validated. | `posts`: tweet id/text/created_at/entities; `likes`: liked tweet id/time; `follows`: account id/screen name; `searches`: only if export includes searches; `ads/interests`: ad engagements/interests where present. | `supported_archive_import`; API optional only after paid/reviewed gate. |
| TikTok | Login Kit and scopes are official; scopes are user-authorized and app-approved.[20][21] | Additional scopes are requested in the developer app and users can grant/deny/revoke.[21] | TikTok support says users can request data, then download when ready; data may include username, watch video history, comment history, and privacy settings; some recent/third-party data may be unavailable.[22] | TikTok archive `.zip` containing JSON/TXT exports; exact filenames are sample-validated. | `posts`: user-created videos metadata; `likes`: liked videos if included; `follows`: following/followers; `searches`: search history if included; `watch_history`: watch video history; `ads/interests`: ad settings/interests where present. | `manual_import_first`; limited API later. |
| Reddit | Reddit OAuth2/scopes are official.[24][25] | Developer app plus API rules/rate limits.[26] | Reddit help: visit `reddit.com/settings/data-request`, log in, submit, then retrieve the prepared data package.[27] | Reddit data request package; representative CSV/JSON paths are sample-validated. | `posts`: submitted posts; `likes`: upvotes/downvotes/saved if included; `follows`: subscribed subreddits; `searches`: if included; `ads/interests`: account/ad personalization fields if included. | `supported_api` plus `supported_archive_import`. |
| LinkedIn | Authorization-code OAuth.[28] | Product-gated APIs and documented rate limits.[29][30] | LinkedIn Help flow to download account data.[31] | LinkedIn archive `.zip` of CSV/JSON/HTML files; exact filenames are sample-validated. | `posts`: shares/comments/articles; `likes`: reactions; `follows`: connections/following/companies; `searches`: search history if included; `ads/interests`: ad categories if included. | `manual_import_first`; restricted API. |
| Snapchat | Snap Login Kit identity/profile path.[32] | Snap developer terms constrain use.[34] | Snapchat support: download My Data from account/privacy controls; Snapchat says it collects account info and usage such as submitted Spotlight/Snap Map Snaps.[33] | Snapchat My Data `.zip`; exact JSON/HTML files sample-validated. | `posts`: public Spotlight/Snap Map/story metadata if included; `likes`: unavailable unless present; `follows`: friends/subscriptions where present; `searches`: search history if included; `ads/interests`: ad/interests/settings where present. | `manual_import_first`; Login Kit identity only. |
| Discord | Discord OAuth2 scopes/flows.[35] | OAuth identity/guilds/connections scopes; do not use OAuth as message-history access. Rate limits apply.[36] | Discord support flow to request a copy of account data from desktop/browser/mobile.[37] | Discord data package `.zip`; representative paths include `account/`, `messages/`, `servers/`, `activity/` and are sample-validated. | `posts`: own message rows only from data package; `likes`: reactions where present; `follows`: servers/guilds/connections; `searches`: unavailable unless package includes; `watch_history`: not applicable; `ads/interests`: activity/analytics/ad fields if present. | `supported_api` for identity/guild metadata; archive for user history. |
| Bluesky / AT Protocol | AT Protocol OAuth is specified; clients/PDS host discovery matters.[38][39] | No central Meta-style app review; compatibility per PDS/client. | Repository export/account migration exports repo data; docs describe account migration and repository mechanisms.[40] | CAR/repository export, not generic social ZIP; v1 stores raw CAR and deterministic decoded records. | `posts`: `app.bsky.feed.post`; `likes`: `app.bsky.feed.like`; `follows`: `app.bsky.graph.follow`; `searches/watch/ads`: not covered by repo export. | Strong `supported_api` + repository import candidate. |
| Pinterest | Pinterest authorization/API v5.[41][42] | App/API approval and scopes. | Privacy-policy access rights path; exact downloadable archive layout not verified.[43] | No archive parser until a privacy export sample is obtained. API parser can handle pins/boards. | `posts`: pins/boards via API; `likes/follows/searches/ads`: archive-only if present in export. | API for pins/boards; `sample_required` for archive. |
| Tumblr | Tumblr OAuth/API v2; API terms apply.[44][46] | Developer app/API terms. | Tumblr Help: export each blog separately; Tumblr packages blog content into a ZIP.[45] | Blog export `.zip`, per-blog. | `posts`: blog posts and media metadata; `likes/follows/searches/watch/ads`: not covered by blog export unless API/other official export provides them. | `supported_api` + blog export import. |
| Twitch | Twitch authentication/scopes/rate limits are official.[47][48][49] | Granular channel/account scopes; rate limits. | Twitch privacy notice/access choices are the data-rights path.[50] | No enabled archive parser until user privacy-export sample confirms files. | `posts`: clips/channel/video metadata via API where scoped; `watch_history/chat/ads`: only if privacy export includes and consented. | API for approved account/channel data; manual privacy import later. |
| Spotify | Authorization Code with PKCE.[51] | Scopes cover profile/library/listening/playlist/playback categories; rate limits apply.[52][53] | Spotify support: automated Download your data tool returns several JSON files; extended streaming history is a support/data request path.[54] | Spotify JSON files; extended streaming history JSON is high-confidence parser target. | `posts`: playlists/user-created library artifacts; `likes`: saved tracks/albums/shows; `follows`: followed artists/playlists if included/API; `searches`: not covered unless export includes; `watch_history`: map to listening history; `ads/interests`: inferred ad segments only if officially exported. | `supported_api` + extended-history import. |
| Mastodon / Fediverse | Mastodon OAuth and scopes per instance.[55][56] | Per-instance app registration/terms. | Mastodon import/export docs cover moving/leaving accounts and exporting account data.[57] | Instance export; representative files include outbox/CSV relationship lists, but exact instance output can vary. | `posts`: statuses/outbox; `likes`: favourites; `follows`: follows/followers/lists; `searches/watch/ads`: generally not covered. | `supported_api` + instance export import. |

## Deterministic parser fixture rules

1. Every parser gets at least one synthetic fixture whose data is obviously fake and one optional redacted real fixture after explicit user consent.
2. Fixtures live under `fixtures/archive-synthetic/` and include: `archive_tree`, `raw_records`, `normalized_records`, `expected_manifest`, and `source_urls`.
3. Parsers map exact JSON paths or CSV columns to normalized categories. No free-form LLM extraction is allowed.
4. Missing optional categories are recorded as `not_present_in_archive`, not as zeros.
5. A platform support page naming a category is not enough to enable a field parser; enabling requires a concrete path/field sample.
6. Field-level maps must classify each normalized field as `official_field`, `derived_deterministic`, or `product_metadata`.

## Immediate implementation implications

- Enable first parsers for lower-risk, structured lanes: Spotify extended streaming JSON, Bluesky/ATProto repo records, Tumblr blog ZIP metadata, Mastodon export/statuses, and X archive posts/likes/follows after sample validation.
- Keep Meta, TikTok, LinkedIn, Snapchat, Discord, Pinterest, and Twitch archive parsers behind `sample_required` flags until current consenting-user/redacted fixtures confirm paths.
- OAuth connectors should be limited to sign-in/linked-account identity until product review confirms scopes and platform terms for each data category.
- Product copy must say “official APIs and official exports where available,” not “complete history from every platform.”

## Sources

[1] https://developers.google.com/identity/protocols/oauth2/web-server — Google OAuth 2.0 for Web Server Applications
[2] https://developers.google.com/identity/protocols/oauth2/native-app — Google OAuth 2.0 for Mobile & Desktop Apps
[3] https://developers.google.com/identity/protocols/oauth2/scopes — Google OAuth 2.0 Scopes for Google APIs
[4] https://developers.google.com/youtube/v3/determine_quota_cost — YouTube Data API Quota Calculator
[5] https://support.google.com/accounts/answer/3024190 — Google Account Help: Download your data
[7] https://developers.facebook.com/docs/facebook-login — Facebook Login
[8] https://developers.facebook.com/docs/permissions/reference — Meta Permissions Reference
[9] https://developers.facebook.com/docs/app-review — Meta App Review
[10] https://developers.facebook.com/docs/facebook-login/guides/access-tokens — Meta Access Tokens
[11] https://www.facebook.com/help/212802592074644 — Facebook information export
[12] https://help.instagram.com/181231772500920 — Instagram information export
[13] https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login — Instagram API with Instagram Login
[14] https://developers.facebook.com/docs/instagram-basic-display-api — Instagram Basic Display API
[15] https://developers.facebook.com/docs/threads — Threads API docs
[16] https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code — X OAuth 2.0 Authorization Code with PKCE
[17] https://docs.x.com/x-api/posts/manage-tweets/introduction — X Manage Posts docs
[18] https://help.x.com/en/managing-your-account/how-to-download-your-x-archive — X archive help
[19] https://docs.x.com/x-api/fundamentals/rate-limits — X API rate limits
[20] https://developers.tiktok.com/doc/login-kit-web — TikTok Login Kit Web
[21] https://developers.tiktok.com/doc/scopes-overview — TikTok Scopes Overview
[22] https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/requesting-your-data — TikTok Requesting your data
[23] https://developers.tiktok.com/doc/overview — TikTok developer docs
[24] https://github.com/reddit-archive/reddit/wiki/OAuth2 — Reddit OAuth2
[25] https://www.reddit.com/dev/api/oauth — Reddit OAuth2 scopes
[26] https://github.com/reddit-archive/reddit/wiki/API — Reddit API rules/rate guidance
[27] https://support.reddithelp.com/hc/en-us/articles/360043048352-How-do-I-request-a-copy-of-my-Reddit-data-and-information — Reddit data request
[28] https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow — LinkedIn authorization-code flow
[29] https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts/rate-limits — LinkedIn rate limits
[30] https://learn.microsoft.com/en-us/linkedin/shared/integrations/people/profile-api — LinkedIn Profile API
[31] https://www.linkedin.com/help/linkedin/answer/a1339364/downloading-your-account-data — LinkedIn data download
[32] https://developers.snap.com/snap-kit/login-kit/overview — Snap Login Kit
[33] https://help.snapchat.com/hc/articles/7012305371156 — Snapchat My Data
[34] https://www.snap.com/terms/developer — Snap Developer Terms
[35] https://discord.com/developers/docs/topics/oauth2 — Discord OAuth2
[36] https://discord.com/developers/docs/topics/rate-limits — Discord rate limits
[37] https://support.discord.com/hc/en-us/articles/360004027692-Requesting-a-Copy-of-your-Data — Discord data package
[38] https://atproto.com/specs/oauth — AT Protocol OAuth
[39] https://docs.bsky.app/docs/advanced-guides/api-directory — Bluesky API hosts/auth
[40] https://atproto.com/guides/account-migration — AT Protocol account migration/repository export
[41] https://developers.pinterest.com/docs/getting-started/authentication-and-authorization — Pinterest authorization
[42] https://developers.pinterest.com/docs/api/v5 — Pinterest API v5
[43] https://policy.pinterest.com/en/privacy-policy — Pinterest Privacy Policy
[44] https://www.tumblr.com/docs/en/api/v2 — Tumblr API v2
[45] https://help.tumblr.com/export-your-blog — Tumblr blog export
[46] https://www.tumblr.com/docs/en/api_agreement — Tumblr API License Agreement
[47] https://dev.twitch.tv/docs/authentication — Twitch authentication
[48] https://dev.twitch.tv/docs/authentication/scopes — Twitch scopes
[49] https://dev.twitch.tv/docs/api/guide — Twitch API guide/rate limits
[50] https://www.twitch.tv/p/en/legal/privacy-notice — Twitch Privacy Notice
[51] https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow — Spotify Authorization Code with PKCE
[52] https://developer.spotify.com/documentation/web-api/concepts/scopes — Spotify scopes
[53] https://developer.spotify.com/documentation/web-api/concepts/rate-limits — Spotify rate limits
[54] https://support.spotify.com/us/article/understanding-my-data — Spotify Understanding my data
[55] https://docs.joinmastodon.org/methods/oauth — Mastodon OAuth
[56] https://docs.joinmastodon.org/api/oauth-scopes — Mastodon OAuth scopes
[57] https://docs.joinmastodon.org/user/moving — Mastodon import/export
