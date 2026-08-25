# Vercel Postgres / Neon marketplace provisioning pattern

Use this reference when a Vercel app needs durable Postgres on Vercel/Neon instead of serverless-local SQLite or `/tmp` fallback storage.

## Pattern

1. First confirm the app can expose a storage/readiness endpoint without secrets, e.g. `/healthz` reporting backend, durable boolean, encryption state, and missing env keys by name only.
2. Try the Vercel integration path rather than assuming an old `vercel storage` command exists. Current CLI discovery showed `vercel storage` was not available, while `vercel integration add neon` was the relevant path.
3. If `vercel integration add neon` returns an `action_required` / marketplace terms acceptance message, stop and ask the user to accept terms in their Vercel account or explicitly authorize the CLI terms action. Do not accept marketplace/legal terms on the user's behalf without explicit authorization.
4. Prefer the free Neon/Vercel Postgres plan unless the user explicitly approves paid database spend; tell the user when a marketplace/subscription step is required before proceeding.
5. After provisioning, inspect only variable names / set-missing status. If the integration writes a local `.env.local`, extract the generated `DATABASE_URL` without printing it, then set database env vars with names the app actually checks, commonly:
   - `DATABASE_URL` for framework/database defaults
   - app-specific aliases such as `MUSICAI_DATABASE_URL` or `MUSICAI_TOKEN_DB`
6. Redeploy production and verify the live health endpoint reports durable Postgres, not just that env vars were set.
6. Keep logs, docs, and chat redacted: never print the Postgres connection string or Vercel/Neon tokens. Report only `set`/`missing`, backend type, and durable status.

## Verification checklist

- Local fallback still works for development.
- Production `/healthz` shows `backend: postgres` or equivalent.
- Production `/healthz` shows `durable: true`.
- Token/secret encryption remains enabled if the app stores OAuth tokens.
- OAuth callback and dashboard routes still work after redeploy.

## Pitfalls

- A Vercel serverless app writing SQLite under the project bundle will fail or be read-only; `/tmp` SQLite is acceptable only as a temporary demo fallback and is not durable.
- Do not conclude that durable storage is configured until the live deployed app reports the durable backend.
- Marketplace terms acceptance is an account/legal action, not a technical retry loop. Capture the blocker cleanly and resume once the user accepts/authorizes it.
