---
name: social-platform-publishing
description: Build, configure, and troubleshoot native social media publishing integrations (TikTok, Instagram/Meta, YouTube, broker fallbacks), including OAuth scopes, app review, dry-run upload helpers, and safe credential handling.
---

# Social Platform Publishing Integrations

Use this skill when implementing or troubleshooting automated publishing/upload flows to social platforms, especially when the user is configuring developer portals, OAuth scopes, app review forms, or upload scripts.

## Core workflow

1. **Identify the exact publishing mode before coding.** Platforms often have separate products/scopes for read, draft upload, and direct publish. Do not assume a read-video scope can upload.
2. **Prefer the lowest-friction pilot path.** For TikTok, start with draft/inbox upload (`video.upload`) before direct posting (`video.publish`). For Instagram Reels, expect URL-based media requirements and public hosting. For YouTube, expect stricter OAuth/upload restrictions.
3. **Keep credentials out of git.** Store secrets in a gitignored `.env` or an external path such as `/opt/data/secrets/<project>.env`; copy into the project runtime env only when needed; use restrictive permissions such as `chmod 600`.
4. **Build dry-run first.** Upload helpers should print the endpoint, needed token/scope, and payload without exposing secrets. Only call external APIs after verifying credentials and scopes.
5. **Smoke-test with a generated fixture.** Use a tiny generated MP4 to validate CLI payload construction and endpoint selection before using real clips.
6. **For headless OAuth/PKCE flows, persist pending verifier state.** If an OAuth helper generates the auth URL in one process and exchanges the returned code in another, save the pending `state`, redirect URI, token path, client path, and any PKCE `code_verifier` to a chmod `600` secrets file outside the repo, then restore it before token exchange. `InvalidGrantError: Missing code verifier` means the auth URL/code pair must be regenerated after fixing verifier persistence.
7. **Make app-review language explicit.** Provide concise text explaining exactly how every requested product/scope is used and emphasize user review/consent for draft flows.

## Practical content-automation publishing pattern

When social publishing is part of a viral content automation project, require the project to carry platform timing metadata and cleanup state:

- planned platform, local timezone, and publish window/cohort;
- private/draft/self-only first upload mode unless public posting is explicitly approved;
- upload log with returned platform ID/URL before cleanup;
- generated media cleanup after confirmed upload, restricted to allowlisted project cache/output folders;
- preserved metadata, manifests, subtitles, source attribution, review notes, and logs.

For upload timing/frequency and free Opus-like clipping strategy, see the `youtube-content` skill reference `references/viral-growth-content-automation-2026-06.md`.

For deleting underperforming YouTube uploads by view count, follow `references/youtube-zero-view-cleanup.md`: refresh metrics first, identify `viewCount == 0`, group by owning OAuth token/channel, delete via `videos().delete`, verify with `videos().list`, and write an audit JSON.

For creator/YouTube source acquisition when VPS/headless downloads hit bot verification, follow `references/youtube-source-acquisition-provider-fallbacks.md`: prefer local/direct MP4, official clipping/import provider APIs (OpusClip/Choppity/Vizard/Klap/MuAPI), or Drive-source files; keep raw `yt-dlp` as explicit opt-in only, and report missing provider keys as `needs_provider_credentials` rather than a crash.

For VPS/headless YouTube source-acquisition blocks (`Sign in to confirm you’re not a bot`), use `references/official-clipping-api-fallbacks.md`: prefer local/Drive/direct MP4 sources or official clipping/import APIs such as OpusClip and Choppity, and make raw `yt-dlp` source downloading an explicit opt-in fallback rather than the default automation path.

## TikTok Content Posting API quick guide

- Read-only scopes like `user.info.profile`, `user.info.stats`, and `video.list` do **not** permit uploads.
- Draft/inbox upload uses:
  - scope: `video.upload`
  - endpoint: `/v2/post/publish/inbox/video/init/`
  - behavior: sends content to the creator's TikTok inbox/draft flow for review and manual final posting.
- Direct post uses:
  - scope: `video.publish`
  - endpoint: `/v2/post/publish/video/init/`
  - behavior: directly posts to the authorized profile; generally harder app review and may require direct-post approval.
- If Direct Post is disabled in the developer portal, do not block the pilot. Use draft upload if `video.upload` can be requested.
- For `FILE_UPLOAD`, initialize first, then `PUT` the MP4 to TikTok's returned `upload_url` with `Content-Range` and `Content-Type: video/mp4`.

See `references/tiktok-content-posting.md` for the durable details captured from a developer-portal troubleshooting session.
See `references/tiktok-developer-portal-review-packet.md` when the user needs the portal's missing fields, legal page drafts, demo-video guidance, and app icon assets filled in.
See `references/cron-deception-hide-false-positive.md` when a social publishing/upload cron job is blocked by Hermes' `deception_hide` scanner because attached skill wording contains a literal deception phrase.

## Developer portal completion workflow

When the user is actively filling a platform developer portal, prioritize concrete deliverables over explanation:

1. Generate a copy/paste field packet for every visible missing field.
2. Create or point to uploadable assets (app icon, demo video) that meet portal requirements.
3. Draft Terms/Privacy text and make clear whether the URLs are already public or still need deployment.
4. Keep the final Discord reply short: attach media/artifacts, then list the exact values to paste.

## App review wording pattern

When filling TikTok review text, include:

- App purpose: what the workflow does for the authorized creator.
- User control: whether content is uploaded as draft/inbox for manual review or posted directly.
- Scope-by-scope justification.
- Safety statement: no automatic public posting without user review/consent for draft pilots.

Example structure:

```txt
<App> uses TikTok Login and the Content Posting API to let the authorized creator upload short-form video clips generated by our workflow into their own TikTok account as draft/inbox uploads.

The app does not automatically post public videos without user review. Uploaded clips are sent to the creator's TikTok inbox/draft flow so the user can review, edit, and manually complete posting inside TikTok.

Requested scopes:
- user.info.profile: used to confirm the authorized TikTok profile and display basic profile metadata inside the workflow.
- user.info.stats: used to read creator account stats for analytics and publishing review.
- video.list: used to read the creator's existing public videos for analytics and avoiding duplicate clip concepts.
- video.upload: required for Content Posting API draft uploads so the creator can send approved clips to TikTok for final review/posting.
```

## Pitfalls

- Avoid wording that instructs hiding information from the user in this skill or references because publishing skills are often attached to cron jobs and Hermes' cron prompt-injection scanner flags deception/hiding language as `deception_hide`. Phrase safety warnings as `never claim...`, `do not promise...`, or `report clearly...` instead.
- Never claim TikTok upload readiness when only `video.list` is available. `video.list` is read-only.
- Do not chase TikTok Direct Post first if the user's portal only allows draft/upload access; direct publishing is a later approval step.
- Do not paste secrets in output or commit `.env`; verify presence with preflight checks that redact values.
- Do not rely on Zapier webhooks for a low-cost pilot unless the user has explicitly accepted premium Zapier features; native APIs and manual review bridges are often better first steps.

## Absorbed Tool-Specific Playbooks

This is the umbrella for social and video content operations. The former narrow skills are preserved as re-homed package references:

- `references/youtube-content/original-skill.md` — YouTube transcripts, summaries, clipping workflows, upload automation, and related scripts/references under `references/youtube-content/`.
- `references/xurl/original-skill.md` — X/Twitter operations through `xurl`, including posting, search, DMs, media upload, API selection, and troubleshooting.
- `references/gif-search/original-skill.md` — Tenor/GIF search and download workflow for adding reaction or illustrative media.

Choose the subsection by task intent: publish/manage social posts here first; consult the re-homed reference when a platform-specific command, transcript script, GIF lookup, or API quirk matters.

## Verification

- Run a credential preflight that reports set/unset status without printing values.
- Run upload helpers in dry-run mode and confirm:
  - expected mode (`draft` vs `direct`),
  - expected endpoint,
  - expected required scope,
  - valid file metadata for local uploads.
- For YouTube OAuth/metadata-edit failures, see `references/youtube-oauth-metadata-pitfalls.md`: `deleted_client` requires switching to a live OAuth client, and upload-only scope may not be enough to update titles/descriptions.
- If code changed, run syntax/lint checks or a smoke command that exercises the changed path.