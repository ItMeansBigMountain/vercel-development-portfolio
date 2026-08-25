---
name: vercel-app-deployments
description: "Triage, deploy, and manually verify Vercel apps from existing project folders."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Vercel, deployment, frontend, preview, manual-testing]
    related_skills: [github-repo-management]
---

# Vercel App Deployments

Use this skill when auditing existing app folders for Vercel, redeploying Vercel projects, building a deployment URL tracker, or diagnosing why Vercel preview/production URLs are not manually testable.

## Principles

- Treat Vercel URLs as part of a manual testing workflow: record production URL, preview URL, alias/friendly URL, status, and notes in the workspace README.
- Never print or commit Vercel tokens, bypass tokens, environment values, or project secrets.
- Verify both deployment creation and anonymous/manual browser accessibility. A deployment can exist but still return `401 Unauthorized` due to deployment protection.
- Classify projects before deploying: frontend app, backend/API, monorepo, project plan/spec, or script/archive.

## Access check

Check for token/CLI without exposing secrets:

```bash
python - <<'PY'
import os
for n in ['VERCEL_TOKEN','VERCEL_API_TOKEN','VERCEL_ORG_ID','VERCEL_PROJECT_ID']:
    print(f'{n}=' + ('set' if os.getenv(n) else 'missing'))
PY
if command -v vercel >/dev/null 2>&1; then vercel --version; else echo 'vercel cli missing; use npx vercel'; fi
```

If the CLI is unavailable, use `npx vercel` or the REST API with the token from `VERCEL_TOKEN`/`VERCEL_API_TOKEN`.

Before a deploy, verify the token in the exact execution context that will run `npx vercel` (same terminal/session/workdir), because higher-level wrappers or different tool backends may have different environment injection. If neither `VERCEL_TOKEN` nor `VERCEL_API_TOKEN` is present there, stop after local build/preview verification and report the deploy-auth blocker without exposing secrets.

## Inventory existing Vercel projects via API

```bash
python - <<'PY'
import os, json, urllib.request
TOKEN=os.environ.get('VERCEL_TOKEN') or os.environ.get('VERCEL_API_TOKEN')
assert TOKEN, 'Missing Vercel token'
req=urllib.request.Request('https://api.vercel.com/v9/projects?limit=100', headers={'Authorization':'Bearer '+TOKEN})
data=json.load(urllib.request.urlopen(req, timeout=30))
for p in data.get('projects', []):
    latest=p.get('latestDeployments') or []
    print(p.get('name'), p.get('framework'), latest[0].get('url','') if latest else '')
PY
```

## Local project triage

For each candidate folder:

1. Look for `package.json`, `vercel.json`, lockfiles, framework configs, and sub-apps.
2. Read scripts and key dependencies:

```bash
node -e "let p=require('./package.json'); console.log(p.scripts||{}); console.log({...p.dependencies,...p.devDependencies})"
```

3. Run the least destructive local build/check available:
   - Create React App: `npm run build`
   - Vite: `npm run build`
   - Next.js: `npm run build`
   - Angular: `npm ci && npm run build`
   - Expo web: inspect Expo version; old SDKs often need dependency/export fixes before Vercel.
4. Note missing env vars from `.env.example`/templates by key name only, not value.
5. Decide whether backend/API components belong on Vercel serverless or a service better suited for long-running apps/databases (Render/Railway/Fly/etc.).
6. If a folder is only a README/SCOPE/PROJECT plan but the user asks to begin work across projects, do not leave it as inert triage. Pick the highest-leverage low-risk plan-only app and build the smallest Vercel-ready MVP from the stated scope, favoring static/local-first implementations that avoid credentials, payments, official trademarked assets, and databases until manual review proves value.

## Workspace deploy queue for many projects

When the user asks to review every project or create a work queue, create/update a durable queue document in the workspace (for this user's project workspace, `/opt/data/HeRmEz/projects/WORK_QUEUE.md`) with:

- an "Active now" ranked section,
- every project classified as live app, app scaffold, backend/API candidate, plan-only app, or script/archive,
- the current deployment path,
- the next work item,
- explicit blockers.

Keep `/opt/data/HeRmEz/projects/README.md` as the public URL tracker and `/opt/data/HeRmEz/projects/VERCEL_TRIAGE.md` as the detailed evidence log. The work queue is the operator view for choosing what to build next; the README is the review URL table.

For full-workspace sweeps where the user wants every project tested/deployed/smoke-tested with agents, use the Kanban portfolio-sweep pattern in `references/vercel-app-deployments/kanban-portfolio-sweep.md`: seed one durable PBI per project, create a controller card, run small dispatcher batches, require local build/test + Vercel deploy + anonymous HTTP + browser click-through evidence, and create child fix PBIs until each project is shippable or externally blocked.

### Choosing the next app after a deployment pass

When the user says "what's next" or "move on" after a project pass, do not only recite the top row of the queue. Actively inspect the next ranked candidate's live URL/source enough to classify whether it is already a useful product, a raw demo, or a plan-only opportunity. Then give an operator recommendation:

- If the next ranked app is a raw technical demo (for example, a canvas/Three.js cube with no product wrapper), say so plainly and suggest either a quick productization pass or skipping to a higher-leverage MVP.
- Compare queue order against business/demo value: a lower-ranked plan-only app with a clear monetizable workflow can be the smarter next build than polishing a generic visual sandbox.
- Keep the response short and decisive: URL/status, what was observed, and the recommended next move.
- If proceeding to build, update the queue/readme after the work; if only recommending, avoid stale tracker edits.

### Bulk deploy-all urgency pattern

When the user says they need **all projects deployed now** and Vercel credentials are available, do not leave plan-only/script/archive folders as inert blockers. Start a bulk deployment pass:

- Existing `package.json` apps: build/deploy the app or obvious frontend subdir.
- Plan-only/script/archive folders: create honest static Vite/React **review shells** under `_vercel_mvp/<project>` and deploy those.
- For static Vite/React review shells, always include a local `vercel.json` with `buildCommand: "npm run build"`, `outputDirectory: "dist"`, and `framework: "vite"`. This prevents linked/existing Vercel projects with stale settings from expecting an old `build` output directory and returning 404/build failures.
- Verify anonymous HTTP access for each URL and write a durable report such as `DEPLOY_ALL_REPORT.md`.
- If only a few URLs fail after the bulk pass, create a small `_vercel_mvp_fix/<project>` shell with explicit `vercel.json`, redeploy those targets, then re-run HTTP verification across the whole URL table.
- Run the long pass in a background process with completion notification, then update README/triage trackers.

See `references/vercel-app-deployments/bulk-deploy-all-static-review-shells.md` for the detailed pattern and pitfalls. See `references/vercel-app-deployments/static-review-shell-vercel-output-directory.md` for the recovery pattern when generated Vite shells deploy into linked Vercel projects whose stale settings expect a `build` output directory instead of Vite's `dist`, plus the workspace review-sheet artifacts to maintain.

## Deployment protection / 401 pattern

If a Vercel URL returns `401 Unauthorized` in anonymous checks, do **not** assume deployment failed. It usually means deployment protection/authentication is enabled or the public alias is not configured as expected.

Ask/resolve one of:

- disable deployment protection for manual testing,
- provide the intended public alias/domain,
- provide the approved Vercel deployment-bypass mechanism.

When the user approves disabling protection, patch each project with `ssoProtection: null` via the Vercel API, then re-test anonymously:

```bash
python - <<'PY'
import os,json,urllib.request
TOKEN=os.environ.get('VERCEL_TOKEN') or os.environ.get('VERCEL_API_TOKEN')
assert TOKEN, 'Missing Vercel token'
headers={'Authorization':'Bearer '+TOKEN,'Content-Type':'application/json'}
projects=json.load(urllib.request.urlopen(urllib.request.Request('https://api.vercel.com/v9/projects?limit=100',headers=headers),timeout=30)).get('projects',[])
for p in projects:
    name=p['name']
    req=urllib.request.Request(
        f'https://api.vercel.com/v9/projects/{name}',
        data=json.dumps({'ssoProtection': None}).encode(),
        headers=headers,
        method='PATCH',
    )
    detail=json.load(urllib.request.urlopen(req,timeout=30))
    print(name, 'ssoProtection=', detail.get('ssoProtection'))
PY
```

A Bearer Vercel API token is not necessarily enough to bypass deployment protection on the public app URL; verify with an anonymous request after changing settings.

## Vercel Postgres / Neon durable storage

When a Vercel serverless app needs durable writes or OAuth token persistence, do not rely on SQLite in the deployed bundle. `/tmp` SQLite can keep a demo alive temporarily, but it is ephemeral and should be reported as non-durable.

When the user asks to add a database and make sure it is free, prefer a free-tier hosted Postgres path first (usually the Vercel Neon integration for Vercel apps). Verify the app is already Postgres-ready, then attempt the integration. If marketplace terms acceptance blocks provisioning, report the exact user action needed; do not treat `/tmp` SQLite as the free durable answer.

Use the Vercel integration path for Neon/Postgres and verify the exact CLI surface before assuming commands. If `vercel integration add neon` or equivalent returns a marketplace terms / `action_required` blocker, stop and ask the user to accept/authorize the terms; do not accept account/legal terms on their behalf without explicit approval. After provisioning, set both framework-standard and app-specific DB env vars when relevant (`DATABASE_URL`, plus aliases like `MUSICAI_DATABASE_URL`/`MUSICAI_TOKEN_DB`), redeploy, and verify the live `/healthz` or storage-status endpoint reports a durable Postgres backend. See `references/vercel-app-deployments/vercel-postgres-neon-marketplace.md`.

## Free/SQLite backend defaults

For legacy projects, prefer the lowest-friction deploy path before asking for paid infrastructure:

- Frontend-only apps: Vercel static/site deployment, no database.
- Demo APIs: SQLite or bundled JSON/sample data.
- Prototype games/quizzes that only use accounts for high scores: remove login friction first; collect a display name after the game and post anonymous leaderboard rows. Add durable score storage later only if leaderboard persistence matters.
- Django/Flask apps with durable writes: SQLite on a host with persistent disk (Render/Railway/Fly/etc.) unless there is a reason to use serverless.
- Vercel serverless backends: avoid relying on local SQLite for durable writes; use read-only seed data or a free hosted DB.
- Firebase/Supabase: use only when the app needs hosted auth/realtime or already depends on it.

## HeRmEz legacy-project triage reference

For this user's imported legacy project workspace, see `references/vercel-app-deployments/hermez-vercel-triage.md` for the classification pattern, common user inputs, and README/triage-doc approach. See `references/vercel-app-deployments/hermez-imported-project-redeploys.md` for working redeploy patterns discovered while continuing the imported projects: linked Vercel redeploys, Express API subdirectory routing, Sequelize/MySQL serverless fixes, nested Expo web exports, anonymous HTTP verification, and tracker updates. See `references/vercel-app-deployments/hermez-static-mvp-reframe-and-card-intel.md` for the pattern of reframing a plan-only/legacy folder into a static Vite MVP, renaming misleading project folders, deploying with token fallback, disabling protection on newly-created projects, and verifying a Pokémon card price-scanner MVP. See `references/vercel-app-deployments/realtime-camera-ocr-overlays.md` for extending static scanner/search MVPs with browser `getUserMedia`, throttled canvas OCR, and AR-style price overlays without adding backend infrastructure. See `references/vercel-app-deployments/vercel-protection-and-free-data.md` for the exact Vercel `ssoProtection` API patch and free SQLite/sample-data planning pattern. See `references/vercel-app-deployments/oauth-and-third-party-credentials.md` for safely handling Spotify/Genius/Watson/Agora/Imgflip-style credentials, redirect URLs, and redacted status docs during deployment setup. See `references/vercel-app-deployments/flask-spotify-oauth-on-vercel.md` for Flask/Vercel Spotify OAuth callback setup, proper authorize URL encoding, and redirect mismatch verification. See `references/vercel-app-deployments/flask-oauth-ai-vercel.md` for the legacy Flask + OAuth/API credential pattern: add a Vercel Python entrypoint, deploy with explicit env vars, expose no-login health/API verification routes, and confirm provider redirect URLs exactly. See `references/vercel-app-deployments/flask-watson-musicai-vercel.md` for deploying a legacy Flask app with a non-standard entry module to Vercel, wiring Watson NLU env vars, and adding public `/healthz` plus direct text-analysis routes so integrations can be verified before OAuth callback review. See `references/vercel-app-deployments/flask-package-json-vite-build-pitfall.md` for the common failure where adding `package.json`/Playwright to a Flask app makes Vercel infer a Node/Vite build; fix by adding explicit `api/index.py` and `vercel.json` Python routing. See `references/vercel-app-deployments/flask-spotify-oauth-on-vercel.md` for Flask/Vercel Spotify OAuth callback setup, proper authorize URL encoding, redirect mismatch verification, safe production OAuth diagnostic endpoints, callback correlation logging, `/tmp` token-cache handling, and live Vercel log-follow workflow. See `references/vercel-app-deployments/vercel-postgres-neon-marketplace.md` for the Vercel Postgres/Neon marketplace terms blocker pattern, redacted env setup, and durable-storage health verification. See `references/vercel-app-deployments/free-database-marketplace-blockers.md` for the user-facing pattern when they specifically request a free database and provisioning is blocked by marketplace/legal acceptance. See `references/vercel-app-deployments/active-project-static-mvp-deploy.md` for the pattern of turning the current active docs/scripts project into an honest static Vite MVP, deploying it, verifying the public alias, updating the README, and committing source changes.

## Plan-only app reframes

When a project folder is mostly README/SCOPE/PROJECT scaffolding and the user changes the product direction, treat the latest user direction as the source of truth rather than preserving the imported legacy concept. If the old folder name is misleading and no deployed external integration depends on it yet, rename the folder and update project-local docs plus workspace trackers from the new path. Prefer a static Vercel-ready MVP using public/no-key APIs and browser-only logic before adding accounts, databases, or paid API keys. See `references/vercel-app-deployments/plan-only-app-reframes.md` for the detailed reframe workflow and pitfalls.

## Static data-atlas apps with optional enrichers

When the user asks for a complete searchable/explorable database app but the desired domain has no reliable all-in-one public API, ship a credential-free bundled seed atlas first and make APIs import-time enrichers rather than runtime blockers. Add tests for data shape/search, create no-key import scripts where possible, include rate-limit fallbacks for public APIs, and clearly document seed coverage plus future licensed/keyed enrichers. See `references/vercel-app-deployments/static-data-atlas-with-api-ready-imports.md` for the CombatAtlas-derived pattern.

## Project decommission / deletion workflow

When the user says to delete, remove, retire, or stop resurfacing a project, treat it as a full decommission rather than just deleting one folder:

1. Identify both the source project folder and any generated static review shell, such as `_vercel_mvp/<project>`.
2. Remove the local folders only after confirming they are the intended target and not an adjacent active app.
3. Remove or mark the project in durable trackers so it does not reappear in future queue work: `WORK_QUEUE.md`, workspace `README.md`, `VERCEL_TRIAGE.md`, deployment reports, and any bulk-deploy script/static project map that could recreate the shell.
4. If Vercel credentials are available and the project has a remote Vercel app, delete the Vercel project via API/CLI unless the user only asked to remove local files. Then verify it no longer appears in the Vercel project list.
5. Verify local absence (`test ! -e ...`) and queue absence (`search_files`/content search) before reporting completion.
6. When the user frames the project as a joke/mistake and says to remove it completely, remove it from active queue/tracker tables entirely rather than leaving a visible active row marked deleted. Keep only concise historical notes in deployment report/history files such as “deleted per user request / formerly URL” so future agents understand why a once-deployed URL is gone.
7. Check bulk-deploy/static-shell source maps and generated MVP directories so the deleted project cannot be recreated by the next deploy-all pass.

See `references/vercel-app-deployments/project-decommission-workflow.md` for a concise checklist based on the HeRmEz `consumer-advocate-app` deletion pass.

## Alias drift and placeholder-shell checks

In legacy workspaces that have both real app deployments and generated static review shells, verify the friendly alias by page content before assuming it points at the real app. A public HTTP 200 is not enough: the alias may be serving a placeholder shell while the real app still exists at an older production deployment URL. If so, repoint it explicitly with:

```bash
TOKEN="${VERCEL_TOKEN:-$VERCEL_API_TOKEN}"
npx vercel alias set <real-deployment-host>.vercel.app <friendly-alias>.vercel.app --token "$TOKEN"
```

Then reload the alias in the browser and confirm expected app UI, not just status code. For nested Expo apps, run tests from the parent only if that is where tests live, then run `npx expo export --platform web` and deploy from the actual Expo subdirectory. See `references/vercel-app-deployments/vercel-alias-drift-and-legacy-polish.md` for the full pattern and quiz-app QA checklist.

## URL tracker

Create/update a workspace README table like:

```markdown
| Project | Status | Vercel production / preview URL | Alias / friendly URL | Manual testing notes |
|---|---|---|---|---|
| my-app | Deployed / needs manual review | https://...vercel.app | https://my-app.vercel.app | Login works; mobile nav needs polish |
```

When the user explicitly deprioritizes or skips projects during triage, immediately mark those rows as `Skipped for now` (including paired API/backend rows), add a short note such as `User said to skip <project> for now`, and update the triage doc's recommended next order so future sessions do not keep resurfacing the skipped projects.

## Pitfalls

- Do not deploy every legacy folder blindly; many are specs/scripts, not apps.
- When the user changes a project direction, update/replace stale README/SCOPE/PROJECT/tracker text immediately and rename the folder if the old name will mislead future work.
- Do not commit `.vercel/`, `.env`, `node_modules`, build outputs, local DBs, or generated credentials.
- Do not expose Vercel tokens, protection bypass tokens, API keys, OAuth client secrets, or environment values in chat, commits, docs, or logs.
- Do not report a URL as manually testable until it returns a public 200/expected response or the user has a protection bypass path.
- For OAuth apps on Vercel, verify the *generated live authorization URL*, not just the local env value. Provider redirect errors often come from hand-concatenated query strings, unencoded `redirect_uri`, raw spaces/trailing spaces in `scope`, or a trailing-slash mismatch between the Vercel callback and provider dashboard. If the UI appears to “refresh” after login, inspect callback logs and avoid silent home redirects; render provider/API errors explicitly and reduce OAuth scopes to the minimum needed for the current demo. For Spotify specifically, a successful code exchange followed by `/v1/me` returning `403 Active premium subscription required for the owner of the app` means the development-mode app owner lacks active Spotify Premium or Spotify has not yet recognized it; see `references/vercel-app-deployments/flask-spotify-oauth-on-vercel.md` before changing code again. For SoundCloud, current API app access may require Artist Pro/paid access; if the user does not want that subscription, leave SoundCloud as roadmap rather than blocking the Vercel deploy.
- For nested legacy apps, run the build/export/deploy command from the actual deployable subdirectory and verify `.vercel/project.json` there points at the intended Vercel project; parent and child folders can be linked to different projects.

- If login/signup routes time out because a legacy serverless API defaults to localhost MySQL and no `DATABASE_URL`/`MYSQL_URL` exists, do not stop at “needs DB” when the user needs a live demo. Add a clearly documented demo-mode in-memory fallback that preserves the frontend response contract (for example, signup/login both return JWTs), then verify signup → login → private-route remotely. See `references/vercel-app-deployments/hermez-imported-project-redeploys.md`.
- For Sequelize/MySQL APIs on Vercel, `mysql2` in `package.json` may not be enough. If logs show “Please install mysql2 package manually,” require `mysql2` and pass `dialectModule: mysql2` in the Sequelize constructor.
- For Expo web apps, prefer `npx expo export --platform web` with `outputDirectory: "dist"`; if `export:web` fails, do not assume the app is undeployable — use the export command that matches the installed Expo SDK/bundler. In monorepos/nested legacy projects, run this from the actual Expo app subdirectory, not from a parent folder that only contains tests or an API.
- For imported quiz/education apps whose question images are missing, duplicated placeholders, or unavailable in the web export, do not reflexively chase asset paths. If the user wants curriculum review, replace image prompts with deterministic rendered lesson/code cards and add source tests for curriculum coverage; see `references/vercel-app-deployments/hermez-imported-project-redeploys.md`.
- For quiz/education app visual QA, check the first active question screen, not just the start page. Ensure header buttons are readable and all answer choices are visible or clearly scrollable in the initial viewport; compact spacing before calling the app polished.
- After any bulk static-shell deployment pass, watch for friendly aliases pointing at shells instead of real app deployments; fix with `vercel alias set` and document the corrected production URL.
