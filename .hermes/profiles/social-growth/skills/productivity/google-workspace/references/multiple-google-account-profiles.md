# Multiple Google Workspace / Gmail account profiles

Use this when the user wants Hermes to manage more than one Gmail/Google account as distinct internet identities or project lanes.

## Goal

Keep each Google account isolated and addressable by a short profile name such as `main`, `work`, `clients`, `content`, or `research`.

## Safe credential handling

- Do **not** ask for or store Google passwords.
- Prefer OAuth Desktop app credentials and user approval.
- If the user pastes a client ID / client secret in chat, write a valid Desktop OAuth JSON locally with mode `600`, continue setup, and recommend rotating the secret in Google Cloud afterward because it was exposed in chat.
- Tokens are revocable from the user's Google Account security settings.

## Storage pattern

For each account, use a separate Hermes-home-style credential directory:

```bash
BASE=/opt/data/google-workspace-profiles
PROFILE=main
mkdir -p "$BASE/$PROFILE"
chmod 700 "$BASE/$PROFILE"
```

Run setup/API commands with that profile's `HERMES_HOME` override so `google_client_secret.json`, `google_token.json`, and pending OAuth state stay isolated:

```bash
HERMES_HOME="$BASE/$PROFILE" \
  python /opt/data/skills/productivity/google-workspace/scripts/setup.py --client-secret /path/to/client_secret.json

HERMES_HOME="$BASE/$PROFILE" \
  python /opt/data/skills/productivity/google-workspace/scripts/setup.py --auth-url

HERMES_HOME="$BASE/$PROFILE" \
  python /opt/data/skills/productivity/google-workspace/scripts/setup.py --auth-code "PASTED_REDIRECT_URL"

HERMES_HOME="$BASE/$PROFILE" \
  python /opt/data/skills/productivity/google-workspace/scripts/setup.py --check
```

Use the same override for reads/actions:

```bash
HERMES_HOME="$BASE/$PROFILE" \
  python /opt/data/skills/productivity/google-workspace/scripts/google_api.py gmail search "is:unread newer_than:1d" --max 10
```

## Profile inventory

Maintain a non-secret inventory, for example:

`/opt/data/HeRmEz/projects/_ops/google-workspace-profiles.md`

Record only safe metadata:

- profile name
- human purpose / identity lane
- account email address
- scopes granted
- credential directory path
- date verified
- intended morning-report usage

Never record refresh tokens, access tokens, private keys, full client secrets, or raw authorization codes.

## Morning report usage

For morning reviews, query only the profiles the user explicitly connected for that purpose. Keep output grouped by profile, and default to concise summaries:

- urgent/unread Gmail
- today's calendar events
- important Drive/Docs changes only when requested

Before sending email, creating/deleting calendar events, sharing files, deleting Drive files, or editing Docs/Sheets, confirm the exact action with the user.
