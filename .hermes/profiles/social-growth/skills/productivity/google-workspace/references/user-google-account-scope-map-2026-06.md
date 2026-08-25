# User Google account scope map and OAuth refresh pattern (2026-06)

Use this reference when managing the user's Google Workspace, Gmail, Calendar, Drive/Docs/Sheets, and YouTube OAuth tokens.

## Reporting style for this user

- In Discord, do **not** present Google/OAuth/account status as Markdown tables.
- Use compact bold bullets grouped by account.
- Keep secrets out of chat: never print refresh tokens, access tokens, client secrets, or raw credential JSON.
- It is fine to report non-secret facts: account email, profile name, token path, scopes by short name, channel title, channel ID, and live verification status.

## Canonical account map

- **personal-secondary**
  - Email: `fareed320@gmail.com`
  - Access policy: full Workspace automation.
  - Uses: newsletter source inbox, email sorting, label/archive/trash after verified video upload, content source extraction.
  - Token path: `/opt/data/google_profiles/personal-secondary/google_token.json`
  - Legacy alias: `/opt/data/google_profiles/fareed320` may symlink here.

- **trapiistan**
  - Email: `trapiistan@gmail.com`
  - Access policy: full Workspace automation.
  - Uses: Hermes main Gmail/workspace account, content calendar, automation docs/reports.
  - Workspace token path: `/opt/data/google_profiles/trapiistan/google_token.json`
  - YouTube channel observed: `Sosai Oyama`, channel ID `UCsxzQlusqwmMUdjMvKAJDfA`.
  - YouTube token path: `/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json`

- **classicalechos**
  - Email: `classicalechos@gmail.com`
  - Access policy: full Workspace automation.
  - Uses: Classical Echos content/channel operations.
  - Workspace token path: `/opt/data/google_profiles/classicalechos/google_token.json`
  - YouTube channel observed: `Classical Echos`, channel ID `UCcIpxiU2CLEsBdHcc7_lcyA`.
  - YouTube token path: `/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json`

- **burner**
  - Email: `laflametoast@gmail.com`
  - Access policy: full Workspace automation.
  - Uses: burner/disposable sending and temporary automation.
  - Token path: `/opt/data/google_profiles/burner/google_token.json`

- **personal-main**
  - Email: `affan.fareed@gmail.com`
  - Access policy: full Workspace automation, including Gmail read/modify/send/settings.
  - Uses: personal email context/review, Robinhood email routing for Agentic trading context, Zoom meeting-assets archive, duplicate-newsletter cleanup, and full Calendar/Drive/Docs/Sheets/Contacts automation.
  - Token path: `/opt/data/google_profiles/personal-main/google_token.json`

## Scope bundles

### Full Workspace automation

Use when the user grants full access to an automation identity other than `affan.fareed@gmail.com`.

- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.settings.basic`
- `https://www.googleapis.com/auth/calendar`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/documents`
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/contacts`

### Personal accounts full Workspace automation

Use for both personal Google accounts per the user's explicit 2026-06-29 permission grant: `personal-main` / `affan.fareed@gmail.com` and `personal-secondary` / `fareed320@gmail.com`.

- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.settings.basic`
- `https://www.googleapis.com/auth/calendar`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/documents`
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/contacts`

### YouTube automation

Use per YouTube channel/account. Normal user-specific YouTube channel actions require user OAuth, not a service account.

- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.force-ssl`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

## Mass refresh workflow

- Generate one OAuth URL per profile with `login_hint` and `prompt=consent`.
- Store pending PKCE state separately for each account/channel; never overwrite one profile's pending state with another.
- For this environment, `/opt/data/scripts/google_profile_oauth.py` is the profile-scoped Workspace helper. It reads `/opt/data/HeRmEz/projects/_ops/google-email-profiles.json`; the registry may use `workspace_profiles` rather than legacy `profiles`. The helper should request the Gmail-read-only/non-email-admin bundle for `personal-main` / `gmail_read_only_workspace_admin`, and the full Workspace bundle for the other automation profiles.
- Exchange redirects into dedicated token paths.
- Verify live identity after exchange:
  - Gmail: `users.getProfile(userId='me')` returns the expected email.
  - Calendar: `calendarList.list` succeeds for Workspace tokens.
  - YouTube: `channels.list(mine=True)` returns the expected channel title/ID.
- Write or update the non-secret map at `/opt/data/HeRmEz/projects/_ops/google-email-profiles.json`.
- For shared/default YouTube upload scripts, point `/opt/data/secrets/youtube-main/youtube_upload_token.json` at the intended channel token deliberately; do not assume the previous default is correct.

## Pitfalls captured

- `fareed320` is not a separate canonical profile; it is the user's `personal-secondary` account.
- `trapiistan` is the Hermes main Gmail/workspace account, but Classical Echos may own the content channel for current uploads.
- Wrong-channel YouTube OAuth can successfully authenticate but still be unable to see or edit videos uploaded by another channel.
- YouTube `youtube.upload` alone may not be enough to modify existing video status/metadata; include `youtube.force-ssl` for privacy/status updates and `youtube.readonly` for ownership verification.
