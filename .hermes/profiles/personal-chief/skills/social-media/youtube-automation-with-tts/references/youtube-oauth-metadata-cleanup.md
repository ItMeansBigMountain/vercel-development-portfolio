# YouTube OAuth and metadata cleanup playbook

Use when cleaning up YouTube descriptions/tags/titles, switching channels, or fixing uploads that exposed behind-the-scenes production wording.

## Durable lessons

- `youtube.upload` scope is enough to upload videos, but it is not enough for later metadata/privacy edits. For title/description/tag/privacy cleanup, request both:
  - `https://www.googleapis.com/auth/youtube.upload`
  - `https://www.googleapis.com/auth/youtube.force-ssl`
- A YouTube metadata/privacy update can return `403 forbidden` or `not_found_or_no_access` even with valid scopes if the OAuth token belongs to the wrong channel/account. Verify `channels().list(mine=True)` before editing.
- Multi-channel users may have separate target channels for uploads. Keep tokens separated by channel/project (for example `youtube-main` vs `faceless-youtube-channel`) and do not assume the most recent authorization owns older videos.
- `Error 401: deleted_client` on the Google consent page means the saved OAuth client was removed/stale. Find or configure a current client secret, regenerate the auth URL, and retry; do not keep reusing the dead client.
- For headless localhost redirects, set `OAUTHLIB_INSECURE_TRANSPORT=1` only for the token exchange command; this is normal for the local redirect flow.
- Preserve the pending OAuth state/code verifier between `auth-url` and `exchange`, especially for web clients using PKCE.

## Cleanup verification checklist

1. Exchange the redirect URL and run an auth check.
2. Confirm the authorized channel with `channels().list(part='snippet,contentDetails', mine=True)`.
3. Fetch the target video with `videos().list(part='snippet,status', id=...)`.
4. Update `snippet` with sanitized public title, description, tags, and existing/appropriate `categoryId`.
5. Read back the snippet and search for banned production terms:
   - `faceless`
   - `operator-signal`
   - `generated from newsletter`
   - `source profile`
   - `source sender`
   - `source subject`
   - `source date`
6. Verify configured support URLs are present when required:
   - Linktree
   - Buy Me a Coffee
   - Cash App
   - Venmo

## Metadata style

Public metadata should sound like the creator, not a system log. Do not expose source profile, automation, AI/B-roll/voice provider, or email-processing details. Keep any source metadata in local artifacts only.