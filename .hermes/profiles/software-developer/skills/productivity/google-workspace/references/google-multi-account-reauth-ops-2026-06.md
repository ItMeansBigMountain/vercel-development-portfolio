# Multi-account Google OAuth reauth operations — 2026-06

Use this when repairing the user's Google Workspace auth across all named profiles.

## Profile-scoped workflow

- Use `/opt/data/scripts/google_profile_oauth.py` for Workspace tokens.
- Registry: `/opt/data/HeRmEz/projects/_ops/google-email-profiles.json`.
- Token path shape: `/opt/data/google_profiles/<profile>/google_token.json`.
- Pending state shape: `/opt/data/google_profiles/<profile>/pending.json`.
- Generate one auth URL per profile with `auth-url <profile>`; this overwrites that profile's pending state only, not other profiles.
- Ask the user to return redirects as `<profile>: <full localhost URL>` so exchange can route to the correct pending file.

## Scope policy reminders

- `personal-secondary` / `fareed320@gmail.com`: full Workspace automation. Legacy `fareed320.old-*` tokens may prove Gmail access, but may only contain `gmail.modify`; do not treat them as full Workspace readiness.
- `trapiistan`, `classicalechos`, and `burner`: full Workspace automation.
- `personal-main` / `affan.fareed@gmail.com`: full Workspace automation, including Gmail readonly/modify/send/settings plus Calendar/Drive/Docs/Sheets/Contacts. The user explicitly removed the former read-only Gmail restriction on 2026-06-24.

## Verification pattern

- Verify existing narrow tokens with their actual token scopes. If a token only has `gmail.modify`, loading it with a larger requested scope list can raise `invalid_scope` even though Gmail access works.
- For full Workspace tokens after exchange, run harmless probes:
  - Gmail `users.getProfile` and `labels.list`.
  - Calendar `calendarList.list(maxResults=1)`.
  - Drive `files.list(pageSize=1)`.
  - Build/probe Docs, Sheets, and People/Contacts where needed.
- Verify YouTube separately from Workspace. The user's YouTube upload tokens live under `/opt/data/secrets/youtube-*/youtube_upload_token.json`; use `channels.list(mine=True)` and compare channel ID/title.

## User-facing handoff

- Do not paste secrets or token JSON.
- It is safe to report email, profile name, token path, pending path, channel title, and channel ID.
- Bundle all generated URLs into a workspace note when there are many links, but include concise instructions in chat:
  - open in a normal browser;
  - confirm the account shown by Google;
  - localhost failure is expected;
  - copy the full address-bar URL containing `code=` and send it back with the profile prefix.
