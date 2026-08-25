# Vercel live portfolio audit pattern (2026-06-29)

Use when the user asks what Vercel projects are up/running.

## Audit pattern

1. Use the Vercel API/CLI with secret-safe token handling; never print the token.
2. List all visible projects and latest deployments.
3. Check at least:
   - canonical primary URL: `<project>.vercel.app`
   - configured aliases/domains if available
   - latest deployment URL(s)
4. Classify separately:
   - **healthy primary**: primary URL returns 200
   - **alias drift**: primary alias is 404/500/DNS/SSL failure but latest deployment URL returns 200
   - **actual breakage**: primary and latest checked deployments fail
   - **blocked/protected**: deployment state/HTTP response indicates protection/auth
5. Save both machine JSON and readable Markdown under `/opt/data/HeRmEz/projects/_ops/`.

## Important pitfall

Do not report a Vercel project as simply "down" from the primary alias alone. In this workspace, many projects had broken or nonstandard primary aliases while the latest deployment URL returned 200. Report alias drift separately so the next action is alias repair/decommission, not app debugging.

## Example summary shape

- Projects visible via API: N
- Primary URL healthy 200: N
- Primary URL errors/non-resolving: N
- Needs attention:
  - actual broken/no good latest URL
  - primary alias broken, latest deployment healthy
- Healthy examples / full report path
