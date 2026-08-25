---
name: software-project-delivery
description: "Use when delivering software projects end-to-end: portfolio inventory, app scaffolding, domain-specific product builds, debugging, QA, docs, repo hygiene, deployment handoff, and verification."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [software-development, project-delivery, portfolio, django, scanners, runelite, debugging, qa, deployment]
    related_skills: [test-driven-development, software-quality-workflows, github-repo-management, github-pr-workflow, codebase-inspection]
---

# Software Project Delivery

## Overview

This umbrella covers building, debugging, organizing, and shipping software projects as working artifacts. Use it when the user's request spans product direction, repo/workspace hygiene, implementation, testing, deployment, or handoff. It also preserves detailed playbooks for several recurring product classes: client-editable Django sites, collectible card scanner apps, OSRS/RuneLite plugins, browser-based QA, and Node inspector debugging.

The default standard is: inspect first, implement the smallest useful slice, verify with real commands or browser checks, document operational handoff, then commit/push when requested.

## When to Use

- Inventorying, consolidating, retiring, or creating repos in a project portfolio.
- Turning a product brief or static mockup into a runnable app.
- Building domain-specific apps where prior experiential notes exist: Django admin-backed client sites, card scanner/price-intelligence apps, or OSRS RuneLite plugins.
- Debugging Node/TypeScript/React/Ink behavior with real breakpoints instead of guesswork.
- Running exploratory browser QA and producing evidence-backed bug reports.
- Updating trackers, README files, product direction docs, deployment guides, or client handoff docs.

## Universal Delivery Workflow

When explaining customer/user experience flows for this user, keep it in very small, short bullets if requested. Avoid long narrative product prose; use concise start-to-finish bullets for each actor/persona.

1. **Inspect before changing.** Read project files, trackers, README/direction docs, git status, and relevant branches or child repos.
2. **Classify the job.** Is this a portfolio decision, new scaffold, feature slice, bugfix, QA pass, deployment, or handoff?
3. **Write or update source-of-truth docs.** Use `PRODUCT_DIRECTION.md`, `MERGE_INTO_*.md`, `DEVELOPMENT_PLAN.md`, `DEVELOPER_CHEATSHEET.md`, trackers, or client guides where appropriate.
4. **Implement vertical slices without premature handoff.** Prefer a small working feature with tests over broad unverified scaffolding, but when the user gives a standing end-to-end implementation mandate, keep advancing through the full task list across continuation turns. A passing intermediate slice is progress—not a reason to stop with a summary while executable work remains.
5. **Verify with real execution.** Run tests/builds, start servers, fetch endpoints, inspect browser console, or attach a debugger as needed.
6. **Protect credentials and nested repos.** Never print `.env` values; keep standalone child repos ignored/submodule-managed if nested under a parent workspace.
7. **Commit/push when requested.** Do not claim code is pullable until `git push` has succeeded.

## Portfolio and Roadmapping

For this user's project portfolio, first load `references/user-project-portfolio-operating-model.md`; it captures the retire/set-aside handoff pattern, app-domain classifications, and Vercel end-user review preference.

For workspaces with many related projects:

- Update the same artifacts consistently: project-local docs, `PROJECT_REVIEW_SHEET.md`, CSV trackers, workspace README/indexes, aggregate update logs, and `.gitignore` for nested repos.
- When projects overlap, choose a primary target app and add merge notes to sources.
- When a project is only a plan/static review shell, do not run installs or redeploys; recommend restoring source or scaffolding the documented MVP first.
- For product-parity research, record public sources and translate competitor concepts into original names.
- For this user's project portfolio statuses and durable buckets (finished/set aside, ship/operate, incubate, upcoming OSRS lane, archive/freeze), see `references/user-project-portfolio-status-2026-06-29.md`.

## Domain Playbooks

### Client-editable Django sites

Use Django admin as the first CMS for community, nonprofit, PTA, small-business, or client-owned content sites.

- Model recurring content: newsletters, events, announcements/flyers, volunteer opportunities, resources, membership, sponsors, fundraising, and site settings.
- Prefer Stripe Payment Links before custom checkout.
- Deploy to a Python host such as Render/Railway/Fly/PythonAnywhere; GitHub Pages is static-only.
- Write client admin and deployment docs, including admin URL, content publishing workflow, env vars, database/static files, and custom domain steps.
- Verify tests, migrations, public pages, `/admin/`, and uploaded-media behavior in local or staging.

### Collectible card scanner and price-intelligence apps

Treat lookup as the baseline and video/AR overlay as the product direction.

- Start with OCR or manual search fallback, then normalize multi-source price rows.
- Preserve condition/grade assumptions (`raw-nm`, `raw-lp-mp`, `graded-8/9/10`, etc.) and save them with watchlist entries.
- For video, sample frames and stabilize predictions before rendering overlays; do not OCR every frame blindly.
- Show source, recency, confidence, and marketplace spread instead of one opaque price.

### OSRS / RuneLite plugins

For OSRS clan competition products that go beyond a local plugin into a public website/backend/service, load `references/osrs-clan-competition-service-pattern.md`; model clan type/bracket, member overview, Wise Old Man linkage, upcoming fight posts, agreed match terms, and completed battle analytics while keeping sensitive worlds/rally notes private until agreement.

For OSRS plugins, each child plugin should be its own Gradle/RuneLite repo under the user's portfolio container, except when the user explicitly decides related ideas should become one plugin/product. For merge workflow details, see `references/absorbed/osrs-plugins/merge-related-runelite-submodules.md`. For current portfolio/UI lessons from recent work, see `references/osrs-runelite-plugin-portfolio-lessons.md`. For the latest portfolio-refinement notes, standalone-plugin policy, social API examples, Swing control pitfalls, and submodule cleanup patterns, see `references/osrs-plugin-portfolio-refinement.md`.

- Use Java 11 and verified boilerplate; run `./gradlew clean test assemble --no-daemon` before committing/pushing.
- Keep Old School RuneScape sources separate from RuneScape 3; use OSRS Wiki and RuneLite item IDs.
- RuneLite side panels must fit the default RuneLite sidebar width without requiring player resizing. Prefer compact dropdowns + icon buttons over wide tabs/buttons; explicitly constrain Swing control sizes under `BoxLayout`.
- For live social/client features, inspect the local `runelite-api` jar with `javap` when docs/examples are unclear, then wire graceful empty/unsupported states.
- When merging two plugin repos, choose one canonical child repo, move the other plugin's useful code into that package as helpers/views/models, update `@PluginDescriptor` + `plugin.json` + `runelite-plugin.properties`, commit/push the child first, then remove the obsolete parent submodule gitlink.
- For plugin-hub submission: child repo build/test/push first, update plugin-hub manifest with the child commit SHA, then push parent pointers.
- For social tracking plugins, start empty unless live RuneLite APIs provide members; avoid fake/default people in production UI.
- For social tracking refresh, rescan on login and expose a configurable integer refresh interval in minutes, defaulting to 60, plus manual refresh.
- When merging two plugin repos, choose one canonical child repo, move the other plugin's useful code into that package as helpers/views/models, update `@PluginDescriptor` + `plugin.json` + `runelite-plugin.properties`, commit/push the child first, then remove the obsolete parent submodule gitlink.
- For social tracker plugins, prefer top tabs for primary social views (Friends Chat, Clan Chat, Friends List), rescan on login, expose manual Rescan, and add an integer refresh interval config in minutes defaulting to 60.
- When merging two plugin repos, choose one canonical child repo, move the other plugin's useful code into that package as helpers/views/models, update `@PluginDescriptor` + `plugin.json` + `runelite-plugin.properties`, commit/push the child first, then remove the obsolete parent submodule gitlink.
- When the user needs to run a local Windows copy, commit and push child-repo changes first, then tell them to `git switch main`, `git pull origin main`, and run `.\gradlew.bat run --no-daemon` from the plugin directory.
- When merging two plugin repos, choose one canonical child repo, move the other plugin's useful code into that package as helpers/views/models, update `@PluginDescriptor` + `plugin.json` + `runelite-plugin.properties`, commit/push the child first, then remove the obsolete parent submodule gitlink.
- When the user wants multiple social views, choose the narrowest control that actually fits the default RuneLite side panel. Top tabs are acceptable only if screenshots/manual testing show they do not trail off; otherwise use a constrained selector row (`JComboBox` + icon button) with explicit preferred/maximum sizes.
- When merging two plugin repos, choose one canonical child repo, move the other plugin's useful code into that package as helpers/views/models, update `@PluginDescriptor` + `plugin.json` + `runelite-plugin.properties`, commit/push the child first, then remove the obsolete parent submodule gitlink.
- Test long names and result states for overflow.
- When merging two plugin repos, choose one canonical child repo, move the other plugin's useful code into that package as helpers/views/models, update `@PluginDescriptor` + `plugin.json` + `runelite-plugin.properties`, commit/push the child first, then remove the obsolete parent submodule gitlink.
- For social tracker concepts, build local discovery/tracking/removal/cap behavior first: configurable source toggles, normalized member records, source tags, ignored-name persistence, panel filters, rescan, and one-by-one removal.
- Keep Old School RuneScape sources separate from RuneScape 3; use OSRS Wiki and RuneLite item IDs.
- RuneLite side panels must fit narrow UI constraints; test long names and result states for overflow.
- For social-tracker plugins that watch friends list, clan chat, and friends chat, use a state-driven side panel with explicit top tabs (`Friends Chat`, `Clan Chat`, `Friends List`), per-member remove/untrack actions, compact ignored-member persistence, and a scanner/service boundary before adding external XP/KC APIs. See `references/runelite-social-tracker-panel-pattern.md`.
- When merging two plugin repos, choose one canonical child repo, move the other plugin's useful code into that package as helpers/views/models, update `@PluginDescriptor` + `plugin.json` + `runelite-plugin.properties`, commit/push the child first, then remove the obsolete parent submodule gitlink.
- For plugin-hub submission: child repo build/test/push first, update plugin-hub manifest with the child commit SHA, then push parent pointers.
- For plugin-hub submission: child repo build/test/push first, update plugin-hub manifest with the child commit SHA, then push parent pointers.
- For parent HeRmEz updates involving submodules, push the child repo commit first, then update/remove submodule pointers in the parent repo; tell Windows users to run `git submodule sync --recursive` and `git submodule update --init --recursive <path>` after `git pull`.
- Keep repo-local research notes during OSRS plugin work. Add/update `PROJECT_NOTES.md`, `PRODUCT_DIRECTION.md`, or cleanup-plan docs with verified API methods, working examples, and product decisions so future sessions do not re-research old context externally.
- Preserve standalone-plugin behavior unless the user explicitly approves a shared library: copy/adapt shared account/detail/rival patterns into each plugin rather than requiring users to install multiple plugins.
- Treat `projects/osrs-plugins/` as the active plugin portfolio, not a dumping ground. Remove consolidated thin-plugin submodules from the parent after recording their direction in canonical repos. Keep boilerplate as a remote/template or under `_templates/`, not as a top-level active plugin folder.
- When pruning parent submodules, verify both `.gitmodules` and the directory listing; on Windows, stale removed submodule folders may require manual `rmdir /s /q` after `git pull`, `git submodule sync --recursive`, and `git submodule update --init --recursive`. See `references/osrs-plugin-portfolio-refinement.md` for the current cleanup pattern and active set.
- For plugin-hub submission: child repo build/test/push first, update plugin-hub manifest with the child commit SHA, then push parent pointers.
- For plugin-hub submission: child repo build/test/push first, update plugin-hub manifest with the child commit SHA, then push parent pointers.

### Social-proof commerce and creator-linked marketplaces

For marketplaces that connect products to creator posts, cumulative engagement, or a derived “heat” score, load `references/social-proof-commerce-mvp.md`. Keep commercial product truth separate from attributed social evidence, use approved platform APIs or rights-confirmed submissions instead of scraping, and trust only server-side catalog prices when creating Stripe Checkout Sessions. Verify production UI with real image loading, checkout error paths, and horizontal-overflow checks.

When turning a storefront prototype into a durable Vercel/Next.js commerce operation, also load `references/serverless-commerce-backend-delivery.md`. It covers managed Postgres provisioning, delimiter-aware migrations, signed persistent carts, database-atomic Stripe webhook finalization, passwordless administrator invitations, social-evidence legitimacy, and the full verification gates required before calling the build complete.

For hybrid first-party plus creator/vendor marketplaces, load `references/hybrid-creator-marketplace-fulfillment.md`. It covers rights-reviewed creator-post media, seller ownership, per-line dropship fulfillment, the idempotent 48-hour tracking watchdog, mixed-cart refund allocation, delivery/return holds, Stripe Connect transfers, creator/admin portal boundaries, and webhook-authoritative payouts.

Before committing any newly scaffolded standalone app inside a larger portfolio workspace, run `git rev-parse --show-toplevel` from the child and confirm the Git root is the child directory. Scaffolding tools may inherit the parent repository; never use broad staging until this boundary is verified.

### Node inspect debugging

When `console.log` is not enough:

- Start with `node inspect` or `node --inspect-brk`; use PTY/background process handling for interactive stepping.
- Use `sb(...)`, `cont`, `bt`, `repl`, and `exec` to inspect locals and call stacks.
- For scripted CDP, install `chrome-remote-interface` in a throwaway path and drive breakpoints/scope capture programmatically.
- Prefer `--inspect-brk` when first-breakpoint timing matters; bind inspector to `127.0.0.1` unless isolated.

### Exploratory web QA / dogfood

For QA passes:

1. Build a scope/sitemap.
2. Navigate pages with browser tools.
3. Check console after every navigation and significant interaction.
4. Capture screenshot evidence for every issue.
5. Classify by severity/category and produce a structured report.

## Support Package Index

Additional active references:

- `references/osrs-clan-competition-service-pattern.md` — public OSRS clan competition service pattern: live Wise Old Man clan/member data, OSRS Wiki theme/image usage, no-faux-data empty states, and RuneLite leader fight-agreement fields.

Archived source packages absorbed into this umbrella are preserved under `references/absorbed/<old-skill-name>/` when available:

- `client-editable-django-sites/` — full Django CMS/site playbook, Render deployment references, and admin templates.
- `collectible-card-scanner-apps/` — scanner, OCR, condition-lens, watchlist, and AR-overlay notes.
- `dogfood/` — browser QA workflow, issue taxonomy, and report template.
- `node-inspect-debugger/` — Node inspector and CDP debugging recipes.
- `osrs-plugins/` — RuneLite plugin portfolio, scaffolding, API, UI, and plugin-hub references.
- `references/runelite-social-tracking-panel.md` — social tracking panel pattern: empty defaults, source tabs, rescan interval, ignored members, and default side-panel width constraints.
- `project-portfolio-roadmapping/` — workspace inventory, merge/retire, tracker, and source-of-truth documentation patterns.

## Common Pitfalls

1. Summarizing without writing durable project artifacts when the user asked to organize or steer a portfolio.
2. Calling a static shell a working app because a public URL returns HTTP 200.
3. Claiming deployment or push success without verifying the remote or endpoint.
4. Ignoring support files when consolidating a project-specific skill into this umbrella.
5. Printing secret values while inspecting env files.
6. Using generic web-app advice when a domain playbook has concrete constraints and verification commands.
7. Assuming migration files are repeat-safe because a schema-version row exists; rerun the complete set and use delimiter-aware, conditional compatibility DDL.
8. Writing audit/movement rows unconditionally after a conditional update; make dependent writes select from the successful `UPDATE ... RETURNING` CTE.
9. Removing fictional evidence from the database while leaving invented handles, engagement, post counts, or derived heat claims hard-coded in public components.
10. Scoping an authentication cookie to `/admin` or `/creator` when mutations live under `/api/admin/*` or `/api/creator/*`; the browser will omit the cookie from those APIs even though the protected page renders.
11. Modeling creator fulfillment/refunds/payouts only at whole-order level; mixed carts require immutable per-line seller, fulfillment, refund, and earning ledgers.
12. Marking Stripe refunds or creator payouts terminal from a cron/API response. Store them as submitted and finalize from signature-verified, idempotent webhooks.

## Verification Checklist

- [ ] Existing project state, docs, trackers, and git status inspected.
- [ ] Domain-specific subsection and absorbed references checked when relevant.
- [ ] Code/docs changed in the right repo or workspace boundary.
- [ ] Tests/builds/browser checks/debugger evidence run as appropriate.
- [ ] Credentials redacted and nested repo hygiene preserved.
- [ ] Final response names changed files, commands run, and remaining blockers.
