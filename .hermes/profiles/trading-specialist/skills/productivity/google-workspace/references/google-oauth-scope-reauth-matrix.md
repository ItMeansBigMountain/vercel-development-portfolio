# Google OAuth scope / reauth matrix

Use this after a user enables more Google APIs and asks whether OAuth reauthorization is needed.

## Principle

Enabling an API in Google Cloud only permits the project to call that API. OAuth tokens still only contain the scopes the user consented to. If the new API action needs scopes that were not in the original token, reauth is required.

## No reauth needed when

- The token already contains the needed scope.
- The user only enabled a previously-disabled API for an already-granted scope.
- Example: token already has Gmail scopes, Gmail API was disabled, user enables Gmail API. Smoke-test Gmail again; do not reauth first.

## Reauth needed when adding

- YouTube uploads: `https://www.googleapis.com/auth/youtube.upload`
- YouTube account/channel management or private channel reads: relevant YouTube Data scopes such as `youtube`, `youtube.readonly`, `youtube.force-ssl` depending on action.
- YouTube Analytics / Reporting: analytics/reporting scopes.
- Google Tasks: Tasks scopes.
- Google Meet operations: Meet scopes.
- Classroom operations: Classroom scopes.
- Cloud Search: Cloud Search scopes.
- BigQuery / Cloud Storage user-level operations: relevant Cloud scopes.

## API key vs OAuth

Google Maps and other public API-key workflows do not require OAuth reauth. Store keys as secrets, restrict them in Google Cloud, and prefer server/IP/API restrictions. Do not paste API keys back into chat.

## Workspace baseline used in this session

The current multi-profile Workspace tokens were granted:

- Gmail readonly/send/modify
- Calendar
- Drive
- Contacts readonly
- Docs
- Sheets

This baseline supports morning review, Gmail search/read/labels, Calendar, Drive, Docs, Sheets, and Contacts reads across the user's profiles. It does not support YouTube upload/private analytics until YouTube scopes are added and profiles are reauthorized.

## Verification before reporting readiness

Run harmless probes against each profile token and report actual results:

- Gmail profile and labels
- Calendar list
- Drive list
- Docs and Sheets discovery or read-only file probe
- People/Contacts connection probe
- YouTube public probe if using API key or OAuth for public discovery
- YouTube private/upload probe only after adding YouTube scopes
