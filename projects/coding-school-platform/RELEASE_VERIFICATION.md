# Coding School Platform release verification

Last verified: 2026-08-25

## Scope

Algorithm Academy / Coding School Platform currently ships as:

- A dependency-free Python domain package in `coding_school/` for curriculum, demo accounts, evidence submission, teacher review, parent-safe progress, admin metrics, and portfolio iteration workflows.
- An Expo SDK 57 universal app in `app/` for web, iOS, and Android learner, teacher, and admin demo paths.

All learner data in this release is demo-only. Real student production data, billing, legal terms, public domains, Apple developer credentials, Google Play credentials, and store metadata require owner decisions/credentials before public launch.

## Verified commands

From `projects/coding-school-platform`:

```bash
python3 examples/linear_search.py
python3 examples/demo_workflow.py
python3 -m unittest discover -s tests -v
python3 -m compileall coding_school examples tests
```

From `projects/coding-school-platform/app`:

```bash
npm run typecheck
npm run build:web
npm run smoke:web
npm run gate:inputs
npm run build:android
npm run build:ios
npx expo-doctor
npm audit --audit-level=high
```

`npm run smoke:web` serves the current `app/dist/` web export on a local ephemeral port by default. Run it after `npm run build:web`, before native exports overwrite `dist/`. Override with `SMOKE_URL=<url> npm run smoke:web` to test a deployed web URL.

`npm run gate:inputs` is the reusable Playwright input-quality monitor. It serves `app/dist/` locally by default, writes `app/input-quality-report.json`, and can test a public deployment with `INPUT_GATE_URL=<url> npm run gate:inputs`.

## Browser smoke coverage

The Playwright smoke test verifies:

- Mobile viewport: learner mission page loads.
- Secure coding preview iframe is sandboxed and script-free.
- Learner reflection can be saved as offline evidence.
- Teacher review queue shows the evidence and can approve mastery.
- Admin release console is reachable and shows demo-only operational gates.
- Desktop viewport preserves the approved learner progress count.
- No browser console/page errors occur during the smoke path.

## Input quality gate coverage

The Playwright input gate verifies every demo web flow at phone portrait, phone landscape, tablet, laptop, and wide-monitor viewports:

- Learner keyboard focus, textarea editor paste, fill-in-the-blank input, word bank selection, visible validation errors, autosave/reload, submission, and focus/scroll behavior.
- Teacher review queue feedback actions for submitted evidence.
- Parent weekly progress export and parent-safe note field.
- Admin release console and validation indicators.
- Accessibility button names, absence of browser console/page errors, and absence of horizontal overflow at every viewport.
- CI runs this gate on local exported web artifacts and on public Vercel/Azure URLs when the configured deployment environments are available.

## Cross-platform build coverage

Expo Metro exports pass for:

- Web static bundle in `app/dist/`.
- Android bundle export.
- iOS bundle export.

These prove the universal app compiles for all required targets. They are not signed store artifacts.

## Release blockers requiring owner credentials or decisions

- Production web domain and legal/privacy copy must be chosen before public traffic.
- Apple Developer account, bundle ID ownership, app privacy answers, screenshots, and TestFlight distribution are required for iOS release verification.
- Google Play Developer account, package name ownership, Data Safety answers, screenshots, and internal testing track are required for Android release verification.
- Real payments/billing are explicitly out of scope and must not be enabled without legal/payment choices.
- `npm audit --audit-level=high` passes with 0 high/critical findings, but Expo toolchain dependencies still report 10 moderate transitive `uuid` advisories where the offered fix is a breaking Expo downgrade.

## Rollback

The current web artifact is static. Roll back by redeploying the previous verified `app/dist/` build or reverting the release commit and rerunning `npm run build:web` before deployment.

## GitHub CI and preview environments

`.github/workflows/coding-school-release.yml` is the standing pull-request and `main` gate. It checks exact canonical-manifest/app parity, all domain role tests, high-severity dependency advisories, TypeScript, web/Android/iOS exports, and Playwright learner/teacher/parent/admin paths. A passing same-repository run deploys an immutable Vercel preview and verifies that public URL. Fork pull requests run without deployment secrets.

`.github/workflows/coding-school-eas-preview.yml` is a manual, separately gated native preview path. It queues Android, iOS, or both as EAS internal-distribution builds. Expo returns the exact device install URL in the workflow/EAS build record when the project and signing credentials support that platform.

GitHub environment configuration (repository Settings → Environments):

- `coding-school-preview`: variable `VERCEL_ORG_ID`, variable `VERCEL_PROJECT_ID`, and a project/team-scoped secret `VERCEL_TOKEN`. Do not expose it to fork runs.
- `coding-school-mobile-preview`: secret `EXPO_TOKEN` scoped to this Expo project. Require a reviewer before iOS builds because they can use Apple signing credentials.
- Protect `main`; require `Curriculum parity and role tests` and `Learner teacher admin and web build`, and disallow direct/force pushes.

Production aliases are intentionally separate from preview credentials and promotion. The previously claimed aliases were removed from the verified list on 2026-08-26 because they served stale or unrelated applications. Do not treat either alias as a Coding School release until the current Expo export is deployed and the public gates below pass.

Current web release endpoints are:

- Production: pending Vercel promotion (previous alias `https://coding-school-platform.vercel.app` is unverified/stale).
- Production alias: pending Vercel promotion (previous alias `https://algorithm-academy.vercel.app` serves an unrelated legacy site).
- Per-change preview: the exact `Preview:` URL in the `Secure Vercel preview` job summary and GitHub deployment environment.
- Native preview: the exact EAS install URL in the manually dispatched `Coding School EAS internal preview` run. This remains unavailable until `EXPO_TOKEN`, Expo project ownership, and platform signing credentials are configured.

### Rollback

1. Preview rollback is non-destructive: open the last known-good deployment in Vercel and promote/alias it, or re-run the workflow for the known-good commit.
2. For a bad `main` change, revert it through a protected pull request; do not force-push or reuse a failed artifact.
3. Verify every URL promoted into the endpoint list with HTTP 200 plus `SMOKE_URL=<url> npm run smoke:web` and `INPUT_GATE_URL=<url> npm run gate:inputs`.
4. EAS internal previews are immutable. Remove tester access to a bad build and queue a corrected build; store releases require their own staged rollback.

The workflow job summary is the source of truth for each exact immutable `Preview:` URL. Vercel project aliases are the source of truth for production.
