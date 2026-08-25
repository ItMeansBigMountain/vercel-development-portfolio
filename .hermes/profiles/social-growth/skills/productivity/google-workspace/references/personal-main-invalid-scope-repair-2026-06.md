# Personal-main invalid-scope repair pattern (2026-06)

Use this when `personal-main` / `affan.fareed@gmail.com` fails with `invalid_scope` or when the main account context is blind until OAuth scopes are repaired.

## Policy

- `personal-main` is read-only unless the user explicitly changes policy.
- Do not request Gmail modify/send, Calendar write, Drive write, Docs write, or Sheets write for this profile.
- Expected read-only scopes:
  - `https://www.googleapis.com/auth/gmail.readonly`
  - `https://www.googleapis.com/auth/calendar.readonly`
  - `https://www.googleapis.com/auth/drive.readonly`
  - `https://www.googleapis.com/auth/documents.readonly`
  - `https://www.googleapis.com/auth/spreadsheets.readonly`
  - `https://www.googleapis.com/auth/contacts.readonly`

## Repair sequence

1. Generate a fresh profile-scoped OAuth URL for `personal-main` with `prompt=consent`, `login_hint=affan.fareed@gmail.com`, and only the read-only scope bundle.
2. Store pending PKCE state under the profile-specific directory, not a shared pending file.
3. Ask the user to approve with `Affan.fareed@gmail.com`, then paste the entire `http://localhost:1/?code=...&scope=...` redirect URL.
4. Exchange the callback into `/opt/data/google_profiles/personal-main/google_token.json`.
5. Verify live identity and service access:
   - Gmail `users.getProfile(userId='me')` returns `affan.fareed@gmail.com`.
   - Calendar list succeeds.
   - Drive list succeeds.
   - Docs and Sheets discovery/client construction succeeds.
   - People/Contacts read succeeds.

## Helper-script pitfalls

- Some older profile OAuth helpers assumed the profile registry key was `profiles`; the current registry may use `workspace_profiles`. Robust helpers should accept either.
- Scope selection must be profile-aware: full Workspace scopes for automation accounts, read-only Workspace scopes for `personal-main`.
- If the OAuth callback includes a `scope=` parameter, preserve those granted scopes when constructing the token flow and relax token-scope comparison if the provider returns an equivalent subset/order.

## Reporting style

For this user, report OAuth status in compact Discord bullets, never tokens/secrets. It is fine to report email identity, token path, and which services smoke-tested successfully.
