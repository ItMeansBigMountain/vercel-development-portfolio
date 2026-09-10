# Coding School release runbook

## Trust chain

The `Coding School CI Quality Gates` workflow is the only build source. Its named quality, type, domain, security, web, Android, and iOS jobs must all succeed before `Gate Summary` permits the same-run reusable Vercel job to consume `coding-school-web`. The artifact includes a source manifest and file checksums; GitHub records its immutable artifact ID and SHA-256 digest.

Production accepts an explicit successful `coding-school` CI run ID and full commit SHA. It downloads that exact cross-run artifact, verifies the GitHub run event/ref/SHA/conclusion, artifact ID/digest, embedded manifest, and file checksums, then pauses at `coding-school-production`. Production is serialized by the fixed `coding-school-production` concurrency group.

## Required live controls

Do not provision or use production credentials until all controls read back successfully:

- GitHub plan/repository supports protected branches and environment reviewers.
- `coding-school` requires PRs, `Gate Summary (required for protection)`, stale-review dismissal, conversation resolution, no deletion/force push, and administrator bypass disabled.
- `.github/CODEOWNERS` review is required for workflows, the app lockfile, and release scripts.
- `coding-school-production` permits only `coding-school`, requires a reviewer other than the initiator, and disables administrator bypass.
- Repository Actions are restricted to approved actions and full-SHA references.
- `coding-school-preview` has `VERCEL_TOKEN` as its only secret and the exact expected org/project variables. Vercel native Git integration is disabled; API read-back must identify project `coding-school-platform` / `prj_2RTTGwmqepGM9TMkyX2iXX9jbrNt`.
- `coding-school-production` has no long-lived deployment secret. `AZURE_PRODUCTION_URL` is a non-secret variable. Azure Static Web Apps trusts the GitHub OIDC identity token for this repository/environment; no deployment token is fetched or passed.

## Preview and approval

1. Open a PR touching this app or its workflows.
2. Confirm every named gate and Gate Summary succeeds. A failed gate must leave `Verified Vercel Preview` skipped.
3. Record CI run URL, source run ID, source SHA, artifact ID/digest, Vercel `dpl_...` ID, immutable HTTPS URL, and workflow deployment record.
4. Open the immutable preview. Require HTTP 200, `Algorithm Academy`, security headers, no console/page errors or horizontal overflow, and the learner submission -> teacher approval flow at 1440x900 and 390x844.
5. Oyama personally approves that exact preview before production dispatch.

## Production promotion

From `coding-school`, dispatch `Coding School Production Promotion` with the approved `source_run_id`, exact 40-character `expected_source_sha`, `promote_production=true`, and `dry_run=false`. A non-release-branch dispatch or mismatched/currently stale SHA must fail closed. The production job must remain pending until the independent environment reviewer approves. After deployment, record the GitHub deployment/run and run the same desktop/mobile classroom workflow against `AZURE_PRODUCTION_URL`.

## Incident response

Stop further promotions; do not delete evidence. Record source run/SHA/artifact ID/digest, deployment IDs/URLs, initiator/approver, UTC timestamps, observed failure, browser/network logs, and current Azure deployment. Revoke or rotate the Vercel token if exposure is suspected. A suspected OIDC policy compromise requires disabling the Azure trust relationship before another deployment.

## Rollback

Rollback is a protected redeployment, never a force push. Select a previously successful `coding-school` CI run whose retained artifact and preview evidence are approved. First dispatch with `dry_run=true`; this validates the exact artifact, checksums, current-release-branch policy, production approval, and OIDC issuance without changing Azure. For an actual rollback, create a protected revert PR so the rollback commit becomes current `coding-school`, let all gates and preview checks pass, obtain Oyama preview approval, then dispatch production with that new run/SHA. Verify both viewports and retain both deployment records.

## Safe rehearsal

A safe rehearsal uses `dry_run=true`; success means the environment approval occurred, the exact artifact chain verified, and an OIDC token was issued. It does not call the Azure deployment action. Two dry runs may be dispatched to prove fixed concurrency queues rather than overlaps. A harmless negative rehearsal uses a non-release-branch ref or incorrect SHA and must fail before the production environment/deploy step.
