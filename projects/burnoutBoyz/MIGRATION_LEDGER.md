# Migration ledger — Honda Tech Upgrade → BurnoutBoyz (t_009c5425 / t_a260e7f9)

Authoritative decision: BurnoutBoyz is canonical; Honda Tech Upgrade is absorbed/legacy.
Verified 2026-09-02.

## Unique assets by source (preserved, not deleted)

|| Source | Role | What is preserved | Destination under BurnoutBoyz | Migration status |
||---|---|---|---|---|
|| `projects/honda-tech-upgrade` (19 files, 63KB; git commits bde1f1151/f2c024bac/577682570) | Original static/Express scaffold + docs + 3/3 Node tests (`app.test.js`) + `index.html` planner UI + `app.js` pure-plan logic | All files + Git history | Prior-art only — `HONDA_PRIOR_ART_MIGRATION.md` (verified 118 lines) defines what may generalize (pure normalization, timeline-order, labeled form, fixture/test style); hard-coded intervals/claims EXCLUDED | Read-only preserved; no import at runtime |
|| `projects/_vercel_mvp/honda-tech-upgrade` (none on disk — previously captured in commit 577682570) | React/Vite Vercel planner | Recovered via Git; not needed live | Not rebuilt — BurnoutBoyz `apps/universal` already replaces it with all-makes Expo Router | Legacy only |
|| `https://honda-tech-upgrade.vercel.app` (Vercel project `honda-tech-upgrade` id `prj_EqqJiUJWGeWJjp4vYGmY6CGBZa9z`; framework vite) | Production legacy URL, HTTP 200, title `Honda Tech Upgrade` | URL preserved; not renamed/redirected/deleted | Labeled legacy/alternate in `canonical-vercel-url-register.md` and `active_app_deployment_inventory.md` | Preserved; no destructive Vercel/repo operation |
|| `https://honda-tech-upgrade-f62krixi3...` (historical READY deployment) | Older review shell | Preservation in inventory rollback record | Same — retained as rollback evidence | Preserved |
|| `projects/burnoutBoyz/HONDA_PRIOR_ART_MIGRATION.md` | Audited audit + checksums + 10 unsupported claims + 5-phase sequence | Already present and verified | Canonical reference; confirms what NOT to migrate | Active |
|| `projects/burnoutBoyz/README.md` / `PRODUCT_DIRECTION.md` | Product identity | Updated to state BurnoutBoyz = canonical; Honda = legacy/alternate | Confirmed | Done |

## Migration of useful functionality (generalized, not copied)
- Planner interaction (form → timeline → badges) → `apps/universal/src/app/index.tsx` (GarageScreen with timestamp, mileage, item state, tabs).
- Deterministic pure-plan logic → `burnoutboyz/timeline.py` + `burnoutboyz/maintenance.py` (provider/version-aware; no hard-coded Civic/Accord/CR-V intervals).
- Labeled accessibility + keyboard focus → universal client semantic roles + visible focus + `accessibilityLabel` fields.
- Local-trial privacy + clear/reset → `clearLocalGarage()` button + `clearSecret()` for VINs + `AsyncStorage` reset; plus `clearSecret` available.
- Fixture/test style → `tests/test_ux.py`, `tests/test_timelines.py`, synthetic fixtures in `fixtures/`; NOT the Honda mileage assertions.
- Source/version/confidence disclosure → `ItemCard` renders `source · confidence`; `Sources` tab; `manualTitle` for VIN/identity.

## What was NOT migrated (explicit exclusions per HONDA_PRIOR_ART_MIGRATION.md §1–10 and user directive)
- Hard-coded `SERVICE_INTERVALS` (Civic/Accord/CR-V mileage-only, no year/trim/engine/schedule-version/severe-use/confidence/source).
- Fixed vehicle/service dropdowns; silent Civic fallback.
- Mileage-only due-state (`milesUntilDue ≤ 1500` fixed threshold).
- UI copy manufacturing maintenance urgency without mechanical context.
- `localStorage-only` durability claim presented as complete ownership plan.
- Any import of `honda-tech-upgrade/app.js` at runtime (no cross-module import; code generalized independently).

## Canonical identity verification (verified this session)
- `burnoutBoyz` repo at workspace root; `burnoutboyz/` backend; `apps/universal/` Expo 57 universal web; `build:web` → `dist/` (routes `/`, `/explore`, `/_sitemap`, `/+not-found`); `tsc --noEmit` clean; `npm run lint` clean.
- `app.json` name = `BurnoutBoyz`; `index.tsx` header = `BURNOUTBOYZ` / `Your garage, explained.`; `explore.tsx` (new) conveys evidence/safety/all-makes identity and links back to garage.
- `README.md`, `PRODUCT_DIRECTION.md`, `HONDA_PRIOR_ART_MIGRATION.md`, `RELEASE_GATE_REVIEW.md` all state BurnoutBoyz = canonical; Honda = absorbed/legacy.
- `canonical-vercel-url-register.md`: Honda entry labeled `retain` (legacy/alternate), not promoted; no BurnoutBoyz canonical URL invented (still a local/build-only product; no fabricated Vercel deployment claimed).
- `projects/_ops/PORTFOLIO_SOURCE_OF_TRUTH.md` and `portfolio-sort-2026-08-31.md`: Honda listed absorbed; BurnoutBoyz = target with preserved legacy evidence.
- `honda-tech-upgrade.vercel.app` preserved (verified by Vercel API: project `honda-tech-upgrade` exists; not renamed/deleted/redirected).
- Git: both repos tracked in monorepo (`honda-tech-upgrade/` unchanged except `.gitignore`/`index.html` local edits; no destructive commit to Honda branch; no history rewrite).

## Blockers / open dependencies (honest; do not invent)
- BurnoutBoyz has no Vercel project registered (no `.vercel/project.json`; `vercel project ls` requires auth and was not completed in this turn; `vercel_cli_token` present but `vercel whoami` returned logged out — so a canonical production alias is NOT yet established; no fabricated URL is written to register).
- `t_a260e7f9` (reviewer validation of this migration, identity, preserved history) remains `todo`; reviewer must independently confirm the build output, identity coherence, and preserved Honda source before final release.
- `t_765b0674` (BurnoutBoyz P0 final verification) is blocked (goal-mode exhaustion / missing authorization/privacy/abuse gates); unrelated to this migration but gates any production claim.
- `VERCEL_API_TOKEN` (uppercase) is not the team token; the lowercase `vercel_cli_token` is the authoritative team token per `portfolio-sort-2026-08-31.md`.

## Rollback / evidence
- Build artifact: `projects/burnoutBoyz/apps/universal/dist/` (exported web, 4 routes, static).
- Source edits: `index.tsx`, `explore.tsx`, `README.md`, `PRODUCT_DIRECTION.md` only.
- No Vercel project renamed/deleted; `honda-tech-upgrade` project unchanged.
- No repo deletion; both directories intact; Git commit SHAs preserved.
- Migration ledger path: this file (`projects/burnoutBoyz/MIGRATION_LEDGER.md`, newly created).
