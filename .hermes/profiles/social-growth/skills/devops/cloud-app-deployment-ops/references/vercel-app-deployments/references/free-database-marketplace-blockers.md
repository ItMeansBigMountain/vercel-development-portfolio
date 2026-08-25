# Free database setup blockers for Vercel apps

## Context

A Vercel Flask app needed durable OAuth token storage. The app was already Postgres-ready and had `/healthz` reporting storage status. The user asked to add a database and make sure it was free.

## Practical sequence

1. Prefer a free Postgres tier compatible with Vercel serverless, such as the Vercel Neon integration.
2. Confirm the app already supports Postgres env names (`DATABASE_URL` plus any app-specific aliases such as `MUSICAI_DATABASE_URL` or `MUSICAI_TOKEN_DB`).
3. Try `npx vercel integration add neon --token "$TOKEN"` from the linked project directory.
4. If Vercel returns marketplace terms acceptance, stop and provide the exact acceptance URL. Do not accept terms unless the user explicitly authorizes it.
5. After terms are accepted, provision the integration, set all aliases the app checks, redeploy, and verify `/healthz` reports `backend: postgres` and `durable: true`.

## Reporting language

Use concise status:

- `Free database provisioning blocked on Neon marketplace terms acceptance.`
- `App is already Postgres-ready; only external account action remains.`
- `Do not store OAuth tokens for real users until /healthz says durable true.`

## Pitfalls

- Do not imply `/tmp` SQLite is a free database solution for real users; it is only a temporary demo fallback on Vercel.
- Do not accept legal/marketplace terms on the user's behalf without explicit authorization.
- Do not print connection strings or Vercel/Neon tokens; report only `set`/`missing` and health endpoint booleans.
