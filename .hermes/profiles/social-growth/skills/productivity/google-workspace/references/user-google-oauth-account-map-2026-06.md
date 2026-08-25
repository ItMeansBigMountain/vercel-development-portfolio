# User Google account scope map and OAuth operation notes — 2026-06

Use this for the user's multi-account Google Workspace + YouTube automation.

## Account roles

- `personal-secondary` / `fareed320@gmail.com`: source newsletter Gmail account. Full Workspace automation. Legacy scripts may use `fareed320` as an alias to this profile. For the faceless newsletter workflow, this is the source account only.
- `trapiistan@gmail.com`: Hermes workspace/calendar account; owns the operational calendar lane. Its YouTube token owns **Sosai Oyama** and is the canonical upload destination for videos generated from `fareed320` newsletter emails.
- `classicalechos@gmail.com`: Classical Echos content/channel account. Use its YouTube token for Classical Echos uploads and metadata edits only; do not use it for `fareed320` newsletter videos unless the user explicitly requests that channel.
- `burner` / `laflametoast@gmail.com`: disposable/burner Workspace account with full automation.
- `personal-main` / `affan.fareed@gmail.com`: primary personal Workspace account. As of 2026-06-24, user wants full read/write Workspace automation for this profile too.

## Scope policy

- Full Workspace accounts, including personal-main: Gmail readonly/modify/send/settings.basic, Calendar, Drive, Docs, Sheets, Contacts.
- YouTube channel tokens: youtube.upload, youtube.force-ssl, youtube.readonly, yt-analytics.readonly.

## OAuth hygiene

- Generate separate auth URLs per account/profile with profile-specific pending state; never overwrite one token path with another account.
- Use `login_hint`, but still have the user confirm the consent-screen account/channel.
- Verify tokens after exchange with harmless probes: Gmail profile email, Calendar access, and YouTube `channels().list(mine=true)` for channel identity.
- Store a non-secret account map in the workspace so cron jobs know which token to use.

## User-facing reports

- The user dislikes Markdown tables in Discord. Report Google/OAuth/account status with bold bullets and compact lists.
