# stockNews retirement evidence — 2026-08-25

Status: BLOCKED pending Vercel authentication.

## Preconditions

- Software migration task `t_d1c1935a`: done.
- Trading validation task `t_899e5551`: done; retirement readiness passed for discovery-only, low-trust catalyst use.

## Production frontend

- Production URL scheduled for retirement: https://stock-news-frontend-chi.vercel.app/
- Current status: **still live**; external pre-retirement probe returned HTTP 200.
- Exact Vercel project: `stock-news-frontend` (`prj_2PYd7tq2vZev24wYaGX6XsxjBHDB`) in org `team_9IP8D1xXFQSrBMZrMjRnl9sD`.
- Removal was not attempted because Vercel CLI reported no credentials, and the browser automation environment could not launch Chrome. No unrelated Vercel project was touched.
- Required operator action: authenticate Vercel, delete only `stock-news-frontend`, verify project readback is not found, and externally verify this URL no longer serves the app.

Previous standalone backend retirement evidence remains at `/opt/data/HeRmEz/projects/_ops/vercel-stocknews-backend-retirement-2026-06-29.json`.

## GitHub archive

- Archived repository: https://github.com/ItMeansBigMountain/stockNews
- API PATCH returned HTTP 200 with `archived=true`.
- Independent API GET readback returned HTTP 200 with `archived=true` and default branch `main`.
- Remote main/HEAD preserved in the bundle: `331f669589ecb73dc7924baadf5d16e7563ff6d2`.

## Recoverable backup

Backup directory: `/opt/data/HeRmEz/projects/_backups/stockNews-retirement-20260825T201537Z`

- Local tracked source archive: `stockNews-local-tracked.tar.gz`
  - SHA-256: `a90969bab3b32fb41d2dcd32657765493e6b5a07408e1b4e427d71bda04dbc1b`
  - Restore smoke test: 69 files extracted.
- Full standalone repository history: `stockNews-remote-all.bundle`
  - SHA-256: `660bacd9a4f1679760d28e9b6937f8a1338426e0303038bc1e15b45be8ce8b2a`
  - `git bundle verify`: complete history.
  - Clone smoke test: passed at the expected remote HEAD.
- Checksums file: `SHA256SUMS`.

## Source location

`/opt/data/HeRmEz/projects/stockNews` remains preserved in place. It has 69 tracked files and no local changes. No local removal was performed while the production retirement remains incomplete.
