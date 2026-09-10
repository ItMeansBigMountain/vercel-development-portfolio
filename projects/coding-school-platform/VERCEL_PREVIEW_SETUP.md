# Coding School Vercel Preview — Required Setup

This document records the Vercel and GitHub configuration required for the
`coding-school-vercel-preview.yml` workflow to function correctly.

## 1. GitHub Environment: `coding-school-preview`

Create a GitHub Environment named `coding-school-preview` with the following settings:

### Protection Rules
- **Required reviewers**: 1+ (e.g., the repository owner or a designated reviewer)
- **Deployment branch policy**: `main` (exact match) — only deployments from `main` branch
- **Wait timer**: 0 minutes (or as desired)

### Environment Variables (not secrets)
| Name | Value | Scope |
|------|-------|-------|
| `VERCEL_ORG_ID` | `team_9IP8D1xXFQSrBMZrMjRnl9sD` | Environment |
| `VERCEL_PROJECT_ID` | `prj_2RTTGwmqepGM9TMkyX2iXX9jbrNt` | Environment |

### Environment Secrets
| Name | Value | Scope |
|------|-------|-------|
| `VERCEL_TOKEN` | Project-scoped Vercel token (≤90 days expiry) | Environment secret |

> **Token generation**: In Vercel Dashboard → Settings → Tokens → Create → Scope to `coding-school-platform` project only. Set expiry ≤ 90 days. Record owner, scope, project, issue date, expiry, rotation date in secure ops log (never the token value).

## 2. Vercel Project Configuration

### Project Identity
- **Project ID**: `prj_2RTTGwmqepGM9TMkyX2iXX9jbrNt`
- **Project Name**: `coding-school-platform`
- **Team/Org ID**: `team_9IP8D1xXFQSrBMZrMjRnl9sD`
- **Framework**: Vite (Expo web export outputs static `dist/`)

### Vercel Project Settings (via `vercel.json` in app/)
```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "buildCommand": "npm run build:web",
  "outputDirectory": "dist",
  "github": {
    "enabled": false
  },
  "headers": [...]
}
```

> **Note**: `github.enabled: false` — we use GitHub Actions for deployment, not Vercel's native GitHub integration. This keeps secrets in GitHub Environments, not Vercel.

### Domains
- **Preview/Development**: Immutable URLs only (e.g., `coding-school-platform-<sha>-itmeansbigmountains-projects.vercel.app`)
- **Production alias**: `coding-school-platform.vercel.app` — **NOT managed by this workflow**. Production aliasing is handled by the separate `coding-school-release.yml` workflow with `promote_production` input.

## 3. GitHub Repository Settings

### Branch Protection (`main`)
- Require PR reviews (1+)
- Require status checks to pass:
  - `Linter & Format Check` (quality)
  - `TypeScript Type Check` (typecheck)
  - `Curriculum & Role Tests (Python)` (domain)
  - `Security & Dependency Audit` (security)
  - `Web Build + Smoke + Input Gates` (web-build-and-test)
  - `Android Export Validation` (android-validation)
  - `iOS Export Validation` (ios-validation)
  - `Gate Summary (required for protection)` (gate-summary)
- Require conversation resolution before merging
- Dismiss stale PR approvals when new commits pushed
- No force push
- CODEOWNERS for `.github/workflows/**`, `ops/**`, lockfiles

### Actions Permissions
- Selected actions only
- Require SHA pinning for all `uses:` references

### Default GITHUB_TOKEN Permissions
- Read-only (contents: read)

## 4. Workflow Behavior

### Triggers
- `push` to `main` with path filter for `projects/coding-school-platform/**`
- `workflow_dispatch` (manual trigger)

### Deployment Flow
1. **verify-config** — Validates environment has `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`; verifies project binding matches expected IDs
2. **deploy** — Downloads `coding-school-web-<sha>` artifact from `coding-school-ci-quality-gates.yml`, pulls Vercel project settings, builds precompiled artifact, deploys immutable preview, emits metadata JSON
3. **browser-smoke** — Downloads deployment metadata, runs Playwright tests against **immutable URL** (not alias), asserts identity string "Algorithm Academy" in title/body on desktop + mobile viewports

### Security Controls
- `VERCEL_TOKEN` only in deploy step env (not workflow/job global)
- No Azure credentials in this workflow
- No production domain assignment
- Immutable URL tested first; alias never touched
- Build artifact comes from CI quality gates (verified build)

### Concurrency
- One deployment per environment at a time (`cancel-in-progress: false`)
- Separate from CI concurrency group

### Artifacts
- Deployment metadata: 90 days retention
- Browser smoke results: 90 days retention

## 5. Rollback Procedure (Break-Glass)

If a bad preview is deployed and needs immediate revert:

```bash
# 1. Record incident
cat > ops/rollback-evidence/rollback-<incident-id>.json <<'EOF'
{
  "incident_id": "<INCIDENT_ID>",
  "actor": "<GITHUB_ACTOR>",
  "approver": "<APPROVER>",
  "timestamp_utc": "<ISO_8601>",
  "reason": "<HUMAN_READABLE>",
  "app": "coding-school-platform",
  "old_deployment_id": "<DEPLOYMENT_ID>",
  "old_immutable_url": "<URL>",
  "new_deployment_id": "<DEPLOYMENT_ID>",
  "new_immutable_url": "<URL>",
  "canonical_alias": "https://coding-school-platform.vercel.app",
  "vercel_project_id": "prj_2RTTGwmqepGM9TMkyX2iXX9jbrNt",
  "commit_sha_old": "<SHA>",
  "commit_sha_new": "<SHA>",
  "verification": { "smoke_passed": true, "identity_asserted": true }
}
EOF

# 2. Re-alias (break-glass) — ONLY for production alias, not preview
vercel alias set <old-immutable-url> https://coding-school-platform.vercel.app --scope team_9IP8D1xXFQSrBMZrMjRnl9sD --token "$VERCEL_TOKEN"

# 3. Reconcile via GitHub Actions (within 1 business day)
#    - Push rollback-evidence commit
#    - Trigger vercel-preview.yml workflow_dispatch
#    - Verify immutable URL matches old deployment
```

## 6. Verification Checklist

After setup, verify by:

1. Push a commit to `main` touching `projects/coding-school-platform/`
2. Watch `Coding School CI Quality Gates` complete (all 7 gates + gate-summary)
3. Watch `Coding School Vercel Preview` trigger and complete
4. Check workflow summary for `### Immutable Vercel Preview` with URL
5. Open the immutable URL — should show "Algorithm Academy" app
6. Verify no Vercel login redirect (public access)
7. Verify browser smoke artifact shows 2/2 passed (desktop + mobile)

## 7. Current Status

- **Workflow file**: `.github/workflows/coding-school-vercel-preview.yml` ✅
- **Browser smoke script**: `projects/coding-school-platform/app/ops/browser-smoke.mjs` ✅
- **Vercel project linked**: `.vercel/project.json` verified ✅
- **Build verified locally**: `npm run build:web` + `npm run smoke:web` ✅
- **Commit SHA**: `7608c19d8`
- **Branch**: `fix/tbtl-vercel-project-identity-v2`

> **Next step**: Create GitHub Environment `coding-school-preview` with variables/secrets above, then push to `main` to trigger first automated preview deployment.