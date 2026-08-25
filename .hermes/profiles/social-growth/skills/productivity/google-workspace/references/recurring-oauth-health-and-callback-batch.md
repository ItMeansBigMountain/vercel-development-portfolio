# Recurring Google/YouTube OAuth health and callback batch pattern

Use when recent sessions show repeated `invalid_grant`, revoked/expired tokens, insufficient scopes, or crons that technically exit OK while Google/YouTube work is blocked.

## Durable lesson

Most downstream failures in the user's Google/YouTube automation are not independent app bugs. They often collapse to one of these auth classes:

- Workspace token revoked/expired (`invalid_grant`).
- Workspace token valid for Gmail but missing Calendar/Drive/Docs/Sheets scopes.
- YouTube upload/metrics token revoked/expired.
- Correct token exists but belongs to the wrong YouTube channel/brand account.
- User pasted a localhost callback from an older auth URL/state, causing `invalid_grant` during exchange.

## Review workflow

1. Inventory tokens first:

```bash
python3 /opt/data/scripts/google_reauth_workflow.py inventory
```

2. Verify each relevant lane separately; do not infer Workspace readiness from YouTube readiness or vice versa:

```bash
python3 /opt/data/scripts/google_reauth_workflow.py verify workspace personal-secondary
python3 /opt/data/scripts/google_reauth_workflow.py verify workspace personal-main
python3 /opt/data/scripts/google_reauth_workflow.py verify workspace classicalechos
python3 /opt/data/scripts/google_reauth_workflow.py verify workspace burner
python3 /opt/data/scripts/google_reauth_workflow.py verify youtube trapiistan
python3 /opt/data/scripts/google_reauth_workflow.py verify youtube classicalechos
```

3. If a verify call fails, generate a fresh auth URL immediately and tell the user to use only the newest URL. Old localhost callbacks should not be retried. Recurring watchdog output must be actionable: include one fresh URL per failed profile, the expected account/channel identity, and the exact labeled callback format. Never emit only `invalid_grant` or a profile name without a recovery link.

4. Ask the user to return callbacks in labeled batch format:

```text
workspace:personal-secondary: <full localhost URL>
workspace:classicalechos: <full localhost URL>
workspace:burner: <full localhost URL>
youtube:trapiistan: <full localhost URL>
youtube:classicalechos: <full localhost URL>
```

5. Exchange, then verify again. For YouTube, confirm both scopes and actual channel title/id via `channels().list(mine=True)`.

## Cron preflight pattern

For Google/YouTube dependent crons, prefer a fast auth preflight before expensive work:

- If token/scopes/channel identity are good, continue.
- If a token is broken, return a structured blocked status and the exact reauth command/profile.
- Do not spend time rendering/uploading/deleting when the target channel token cannot refresh.

Recommended business statuses:

- `ok_uploaded`
- `ok_noop`
- `blocked_auth`
- `blocked_scope`
- `blocked_channel_mismatch`
- `blocked_source`
- `blocked_provider`
- `error`

This prevents misleading cron outcomes where the scheduler says `ok` but the actual business result was blocked.

## Long-lived token hygiene

Current Google Identity guidance: access tokens are short-lived; durable automation depends on receiving and securely storing a refresh token from an OAuth authorization-code flow with `access_type=offline`. Google can still expire or revoke refresh tokens, so crons must handle refresh failure gracefully. Practical causes include user revocation/password-security events, testing-mode OAuth apps, unused tokens, scope changes, and per-client/user token limits.

For this user's automation, generate URLs with `access_type=offline` and `prompt=consent`, then verify the stored token refreshes. To avoid the common 7-day refresh-token failure, ensure the Google Cloud OAuth consent app is not left in Testing mode for external Gmail users; move it to Production when appropriate, or use an Internal Workspace app where available. Sensitive/restricted scopes may still show unverified-app warnings or need Google verification for broad public use, but personal/small-user production apps can often continue with click-through consent.

## Pitfalls

- `login_hint` is not an account lock; the user must confirm the consent-screen account/channel.
- A Google account can own multiple YouTube channels/brand channels; always verify channel ID after exchange.
- Gmail-only success is not full Workspace success; Calendar/Drive can still fail with insufficient scopes.
- A localhost callback code is single-use and short-lived; on `invalid_grant`, generate a fresh URL instead of reusing the pasted callback.
- There is no promise that a Google refresh token "never expires"; the best achievable setup is offline refresh tokens from a Production/Internal OAuth app plus health checks and fast reauth when Google revokes one.
