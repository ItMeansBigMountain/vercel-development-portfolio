# Vercel Portfolio Audit Pattern

Use when auditing the user's Vercel projects and deciding what is actually up, broken, ready, or retired.

## Required distinctions

For every project, separate:

1. **Vercel API state** — project exists, latest deployment state, framework.
2. **Clean primary alias** — usually `https://<project>.vercel.app`; may be broken even when deployments work.
3. **Latest deployment URL** — can return 200 while the primary alias is 404/500/SSL/hostname-broken.
4. **End-user product state** — real app vs static project-review shell vs placeholder.
5. **Portfolio decision** — fix alias, rebuild, retire, or leave as proof-of-concept.

## User preference

The user wants to see how important apps look for an end user, not just whether HTTP returns 200. Use browser snapshots/screenshots for release candidates.

When retiring a finished project from Vercel, preserve local handoff context first (`PROJECT_HANDOFF_CONTEXT.md`) so future agents can revive the project without keeping its details in active memory.

## Common findings to report explicitly

- `primary alias broken, latest deployment works` — likely alias/clean URL issue, not necessarily app failure.
- `latest deployment also broken` — real app/deployment problem.
- `static review shell` — Vercel page exists but product is not implemented.
- `real app but data/API stuck` — UI exists, but backend/data loading needs debugging.

## Safe decommission workflow

1. Confirm user wants removal.
2. Verify or create local handoff context.
3. Delete only the named Vercel project(s) via API/CLI.
4. Save a deletion log under `/opt/data/HeRmEz/projects/_ops/` with project names, IDs, and HTTP status.
5. Report concise results; do not print tokens.