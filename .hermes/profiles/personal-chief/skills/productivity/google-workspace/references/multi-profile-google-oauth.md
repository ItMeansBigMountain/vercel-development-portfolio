# Multi-profile Google OAuth

Use this when Hermes needs to manage multiple Gmail/Google Workspace identities without overwriting a single `google_token.json`.

## Core pattern

- Keep a non-secret profile registry, e.g. `/opt/data/HeRmEz/projects/_ops/google-email-profiles.json`.
- Store each account's OAuth token in a separate credential directory:
  - `/opt/data/google_profiles/<profile>/google_token.json`
  - `/opt/data/google_profiles/<profile>/pending.json` during PKCE auth only
- Use one auth URL per profile with `login_hint=<expected email>`.
- `login_hint` is a hint, not a lock. Tell the user to confirm the consent-screen email before approving.
- Exchange callbacks as `<profile>: <full redirect URL>` so OAuth state can be matched to the right pending file.
- Token/pending files should be chmod `600`; profile directories chmod `700`.

## Recommended profile policy shape

Each profile entry should include:

- `email`
- `role`
- `allowed_uses`
- `send_email_policy`
- `upload_policy`

For this user's workspace, the current policy is:

- `hermes-agent` / `trapiistan@gmail.com`: primary on-behalf account for Google and YouTube upload work.
- `personal-main` / `affan.fareed@gmail.com`: Gmail read-only; non-email Workspace services full/admin. Do not request Gmail send/modify/settings scopes for this profile.
- `personal-secondary` / `fareed320@gmail.com`: read-first; do not send email without explicit per-message approval.
- `classicalechos` / `classicalechos@gmail.com`: classy/high-ticket content account; review required before upload/use.
- `burner` / `laflametoast@gmail.com`: miscellaneous/free-trial/low-stakes tasks.

## Browser / redirect pitfalls

If Google OAuth hangs on a dimmed loading screen, first suspect an embedded/in-app browser such as Discord mobile. Google native-app OAuth should be opened in the system browser. Ask the user to use Safari/Chrome directly.

A broken final page at `localhost` is expected for headless OAuth. The user must copy the full address-bar URL containing `code=` and `state=`.

For a Desktop OAuth client, a localhost loopback redirect is the correct native-app pattern. If the OAuth client is a Web application instead, the exact redirect URI must be configured in Google Cloud; prefer recreating it as a Desktop app for Hermes/headless flows.

## Setup checklist

- OAuth consent screen configured.
- External/testing app has all target accounts added as test users.
- APIs enabled in the same Google Cloud project as the OAuth client.
- For Workspace scopes: Gmail, Calendar, Drive, Docs, Sheets, People/Contacts.
- For YouTube upload/private channel operations: add YouTube scopes and reauth.

## Smoke-test checklist

After exchanging tokens, perform harmless read-only probes per profile:

- Gmail: `users.getProfile` and `labels.list`
- Calendar: `calendarList.list(maxResults=1)`
- Drive: `files.list(pageSize=1)`
- Docs/Sheets: discovery/build or a harmless read against a known file
- People: `people.connections.list(..., pageSize=1)`

If Gmail returns `Gmail API has not been used... or it is disabled`, enable Gmail API in the OAuth client's Google Cloud project; reauth is not required if the token already has Gmail scopes.
