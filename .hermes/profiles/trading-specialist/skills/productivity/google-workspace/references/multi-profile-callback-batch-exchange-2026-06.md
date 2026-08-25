# Multi-profile callback batch exchange and verification

Use this when the user returns several Google OAuth localhost callback URLs in one message or uploaded text file.

## Pattern

1. Parse profile blocks by profile name and the following `http://localhost:1/?...code=...` callback URL.
2. Exchange each callback with the profile-scoped helper:

```bash
python3 /opt/data/scripts/google_profile_oauth.py auth-code <profile> '<callback-url>'
```

3. Tokens should land at:

```text
/opt/data/google_profiles/<profile>/google_token.json
```

4. Verify harmlessly after exchange:

- Gmail `users.getProfile(userId='me')` returns expected email.
- Gmail labels list succeeds.
- Calendar `calendarList.list(maxResults=1)` succeeds.
- Drive `files.list(pageSize=1)` succeeds.
- Check `google_profile_oauth.py list` shows `has_token: true` and `has_pending: false` for every profile.

## User-specific scope policy reminder

- Full Workspace accounts: `personal-secondary`, `trapiistan`, `classicalechos`, `burner`.
- `personal-main` / `affan.fareed@gmail.com`: Gmail read-only only, full Calendar/Drive/Docs/Sheets/Contacts.

## Reporting

Report compact bullets, not tables. Include only non-secret facts: profile, expected email, token path, verification status. Never print tokens, refresh tokens, client secrets, or credential JSON.
