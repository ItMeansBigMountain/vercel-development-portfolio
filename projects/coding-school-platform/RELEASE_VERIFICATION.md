RELEASE VERIFICATION — 2026-08-31 (operations-engineer)

Verification date: 2026-08-31
Project: coding-school-platform (prj_2RTTGwmqepGM9TMkyX2iXX9jbrNt)
Team: itmeansbigmountains-projects (orgId team_9IP8D1xXFQSrBMY3YlY) — verified from JWT payload in .env.local
App identity (package.json): algorithm-academy — expected identity is "Learn by building"

CREDENTIAL STATE (sanitized):
- .env.local VERCEL_OIDC_TOKEN present — JWT parsed (alg RS256, kid mrk-4302ec1b670f48a98ad61dade4a23be7, sub owner:...project:coding-school-platform, exp 1787668708 ≈ Apr 2025) — EXPIRED.
- Vercel API /v2/user with token: HTTP 403 invalidToken.
- npx vercel whoami (CLI 59.10.0): "Logged out".
- vercel_cli_token / VERCEL_API_TOKEN / VERCEL_TOKEN: not set / 403.
- No fresh interactive login session produced in this run.

BUILDS / LOCALS (verified):
- npm run build:web passed; static export written to app/dist (verified on disk 2026-08-31).
- .vercel/project.json confirms project linkage: projectId prj_2RTTGwmqepGM9TMkyX2iXX9jbrNt, orgId team_9IP8D1xXFQSrBMY3YlY.

LIVE URL PROBES (external, sanitized — NO CLAIMS MADE):
- coding-school-platform.vercel.app: HTTP 200 (existing alias) — NOT verified as serving current "Learn by building" identity; NOT claimed live.
- algorithm-academy.vercel.app: HTTP 200 — serves PISTA legacy identity; NOT owned by this project. Decision: LEFT UNTOUCHED per task instructions (legacy site intent confirmed, not this project).
- No new persistent alias established (deployment blocked by credentials).

SMOKE / GATE (NOT EXECUTED — blocked by credential, not skipped):
- SMOKE_URL=<url> npm run smoke:web — NOT RUN (no live deployment URL to smoke).
- INPUT_GATE_URL=<url> npm run gate:inputs — NOT RUN.
- Per criteria: do not list unverified URLs as live.

ALIAS / LEGACY DECISION:
- algorithm-academy.vercel.app: confirmed unrelated PISTA site (identity mismatch, not this repo/project). Left untouched.
- Second persistent alias (e.g., coding-school-platform-... preview): not created; the only existing alias (coding-school-platform.vercel.app) is stale and unverified; promotion requires a verified current build + authenticated deploy.

ROLLBACK / RESTORE:
- Prior deployment not identified from live inventory (Vercel CLI logged out; no `vercel ls --json` available).
- Alias restoration path: re-authenticate Vercel CLI / set valid VERCEL_API_TOKEN, redeploy `dist/` via `npx vercel deploy --prod --scope itmeansbigmountains-projects`, assign alias to verified URL.

OUT OF SCOPE (per task): native signing, app-store release.

BLOCKER / NEXT STEP:
- Need a CURRENT, valid, project-scoped Vercel token or interactive `vercel login` with a working authentication flow (device flow or token refresh) before any deployment, alias update, or verification gate can proceed.
- Once valid: build → deploy → smoke + gate → verify "Learn by building" identity → establish/persist alias → update verification.
