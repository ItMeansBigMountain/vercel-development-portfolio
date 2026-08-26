---
name: tweetbetweenthelines-deployment
description: "Deploy tweetBetweenTheLines via Vercel/GitHub Actions/EAS."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [devops, vercel, github-actions, eas, expo, deployment, tweetbetweenthelines]
    related_skills: [cloud-app-deployment-ops, github-workflows, kanban-orchestrator]
---

# tweetBetweenTheLines Deployment Pattern

## Overview

This skill captures the end-to-end deployment setup for the tweetBetweenTheLines TypeScript/Expo universal product, based on the project's `DEPLOYMENT_RUNBOOK.md` and `DEVELOPMENT_PLAN.md`.

## GitHub Environments & Secrets

| Environment | Secrets | Purpose |
|-------------|---------|---------|
| `tweet-between-the-lines-development` | `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` | Vercel development preview deployments (non-prod) |
| `tweet-between-the-lines-mobile-preview` | `EXPO_TOKEN` | EAS preview builds for iOS/Android |

## Workflows

### Vercel Development Preview (`.github/workflows/vercel-dev.yml`)

Triggers: push to `main` touching `apps/mobile/`, `packages/`, `package.json`, `package-lock.json`, `tsconfig.base.json`; manual dispatch.

Deploys prebuilt output to Vercel development environment (not `--prod`). Publishes immutable HTTPS URL in GitHub deployment environment and step summary. Retains `deployment-url.txt` for 30 days.

### EAS Preview Builds (`.github/workflows/eas-preview.yml`)

Manual dispatch with platform input: `ios`, `android`, or `all`. Uses `preview` EAS profile (internal distribution; Android emits APK). EAS owns signing credentials. Reports build-detail/install URLs in summary and retained JSON artifact.

## One-Time Setup Commands

```bash
# Link Vercel project (run once in project root)
cd /opt/data/HeRmEz/projects/tweetBetweenTheLines
vercel link  # creates .vercel/project.json with projectId + orgId

# Initialize EAS project (run once in apps/mobile)
cd apps/mobile
eas init  # creates eas.json with projectId, commit non-secret projectId
```

## Verification Gates

1. **Web smoke test** — `.hermes-public-web-smoke.cjs` must pass (iPhone viewport, synthetic demo flow, 0 console/page errors)
2. **Typecheck** — `npm run typecheck` passes
3. **Unit tests** — `npm test` passes (domain + API)
4. **Build** — `npm run build` passes
5. **Mobile builds** — `eas build --profile preview` succeeds for iOS/Android

## User Standing Directives (Override Common Blockers)

### GitHub Synchronization (Standing Approval)
Local project repositories should remain synchronized with their GitHub remotes. Routine appropriate project commits and pushes do not need separate approval; preserve unrelated changes and never force-push without explicit authorization.

**When a task blocks on "user decision: push to GitHub":** treat the standing directive as approval and proceed.

### Red-Team Timing
Defer red-team analysis until the production-readiness phase unless the user explicitly requests earlier review.

**Action:** Do not assign or consume red-team capacity on pre-production cards.

### Credential Delivery via Environment Variables
The user will provide `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`, `EXPO_TOKEN`, `GOOGLE_WORKSPACE_TOKEN` later as environment variables.

**Action:** Do not block cards waiting for these credentials. Annotate the card with a comment: `waiting for env var: VERCEL_TOKEN / EXPO_TOKEN / GOOGLE_WORKSPACE_TOKEN` and move on to the next doable task.

### Rate Limit Retries
When reviewer or worker tasks fail with HTTP 429 / provider rate limits, a user signal "rate limits refreshed" means unblock and retry the failed runs immediately.

**Action:** On 429/capacity error: record exact error, set `block_kind: capability` or leave unblocked. When user says "rate limits refreshed": `hermes kanban unblock <ids> --reason "Rate limits refreshed; retry"`.

## External Gate Annotation Pattern

For any card blocked on an external credential/account the user controls:

```bash
hermes kanban comment <id> "waiting for env var: VERCEL_TOKEN"
hermes kanban block <id> --kind capability
# (or leave ready if worker can poll for the env var)
```

## Quick Kanban Commands

| Pattern | Command |
|---------|---------|
| Approve GitHub push on blocked sync task | `hermes kanban unblock <id> --reason "Standing directive: routine GitHub sync approved; push project changes"` |
| Defer red-team card | `hermes kanban comment <id> "Deferred per standing directive: red-team only at production readiness"` + `hermes kanban block <id> --kind needs_input` |
| Annotate credential wait | `hermes kanban comment <id> "waiting for env var: VERCEL_TOKEN / EXPO_TOKEN / GOOGLE_WORKSPACE_TOKEN"` |
| Retry after rate limit | `hermes kanban unblock <ids> --reason "Rate limits refreshed; retry the failed runs"` |

## References

- `references/vercel-github-actions-workflows.md` — full workflow YAML templates
- `references/deployment-runbook-commands.md` — runbook commands and verification steps