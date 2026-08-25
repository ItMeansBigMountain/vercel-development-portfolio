# Personal-main full OAuth reauth pattern

Use when `personal-main` / `affan.fareed@gmail.com` has stale consent, expired/revoked tokens, or a blind main-account context.

## Policy

As of the user's explicit 2026-06-29 instruction, both personal Google accounts have full read/write Workspace permission. `personal-main` / `affan.fareed@gmail.com` is no longer Gmail-read-only.

Full Workspace scope bundle for `personal-main`:

- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.settings.basic`
- `https://www.googleapis.com/auth/calendar`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/contacts`
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/documents`

## Durable helper behavior

For profile-scoped OAuth helpers, derive scopes from the profile registry:

- If `profile == "personal-main"` or the registry access is `read_only_workspace`, use the read-only bundle above.
- Otherwise use the full Workspace bundle from `user-google-account-scope-map-2026-06.md`.
- Support both registry shapes seen in the workspace: top-level `workspace_profiles` and older top-level `profiles`.
- Store pending PKCE state under `/opt/data/google_profiles/<profile>/pending.json` and the token under `/opt/data/google_profiles/<profile>/google_token.json`; never reuse another profile's pending state.

## Interaction pattern

1. Generate an auth URL with `login_hint=affan.fareed@gmail.com`, `prompt=consent`, `access_type=offline`, and the read-only scope bundle.
2. Tell the user to confirm the browser is approving **Affan.fareed@gmail.com**.
3. Tell the user the redirect to `http://localhost:1` will likely fail and that this is expected.
4. Ask them to paste the complete redirected URL from the address bar.
5. Exchange the callback for `personal-main` only.
6. Verify live identity with Gmail `users.getProfile(userId='me')` and confirm the returned email is `affan.fareed@gmail.com`; then smoke-test read-only Calendar/Drive/Docs/Sheets/Contacts probes.

## Pitfall

A generic multi-profile auth helper that always requests the full Workspace scope set can recreate `invalid_scope`/policy mismatch for `personal-main`. Fix the helper to branch on profile/access before generating the auth URL; do not compensate by asking the user to approve broader scopes.