# Coding School Azure Production Promotion — Required Setup

This document records the Azure and GitHub configuration required for the
`coding-school-release.yml` (Production Promotion) workflow to function correctly.

## 1. GitHub Environment: `coding-school-production`

Create a GitHub Environment named `coding-school-production` with the following settings:

### Protection Rules
- **Required reviewers**: 1+ (e.g., the repository owner or a designated approver)
- **Deployment branch policy**: `main` (exact match) — only deployments from `main` branch
- **Wait timer**: 0 minutes (or as desired)

### Environment Variables (not secrets)
| Name | Value | Scope |
|------|-------|-------|
| `AZURE_CLIENT_ID` | Azure AD App (Service Principal) client ID | Environment |
| `AZURE_TENANT_ID` | Azure AD tenant ID | Environment |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID | Environment |
| `AZURE_RESOURCE_GROUP` | Resource group containing the Static Web App | Environment |
| `AZURE_STATIC_WEB_APP_NAME` | Name of the Azure Static Web App | Environment |
| `AZURE_PRODUCTION_URL` | Production URL (e.g., `https://coding-school-platform.azurestaticapps.net`) | Environment |

> **Note**: These are configuration variables, not secrets. They are referenced via `${{ vars.* }}` in the workflow.

### Environment Secrets
None required — authentication uses GitHub OIDC workload identity federation.

## 2. Azure OIDC Workload Identity Federation Setup

### Prerequisites
- Azure CLI (`az`) installed and authenticated
- Owner/Contributor access to the Azure subscription
- Azure AD App Registration (Service Principal) for GitHub Actions

### Steps

#### 1. Create Azure AD App Registration (if not exists)
```bash
# Create or reuse an app registration
az ad app create --display-name "github-actions-coding-school-production" --web-redirect-uris "https://github.com" --sign-in-audience "AzureADMyOrg"
```

Record the `appId` (this is `AZURE_CLIENT_ID`) and `tenantId` (this is `AZURE_TENANT_ID`).

#### 2. Create Service Principal
```bash
az ad sp create --id <APP_ID>
```

#### 3. Assign Least-Privilege RBAC Role
Assign `Static Web Apps Contributor` role on the specific Static Web App resource (not subscription-wide):
```bash
az role assignment create \
  --assignee <APP_ID> \
  --role "Static Web Apps Contributor" \
  --scope "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Web/staticSites/<STATIC_WEB_APP_NAME>"
```

#### 4. Configure Federated Identity Credential
Link the GitHub repository to the Azure AD App via OIDC:
```bash
az ad app federated-credential create \
  --id <APP_ID> \
  --parameters '{
    "name": "github-actions-coding-school-production",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:ItMeansBigMountain/HeRmEz:environment:coding-school-production",
    "description": "GitHub Actions OIDC for the protected Coding School production environment",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

> **Critical**: The `subject` must exactly match `repo:ItMeansBigMountain/HeRmEz:environment:coding-school-production`. The GitHub environment independently restricts deployments to exact branch `main`.

#### 5. Record Configuration
| Setting | Value |
|---------|-------|
| `AZURE_CLIENT_ID` | `<APP_ID>` |
| `AZURE_TENANT_ID` | `<TENANT_ID>` |
| `AZURE_SUBSCRIPTION_ID` | `<SUBSCRIPTION_ID>` |
| `AZURE_RESOURCE_GROUP` | `<RESOURCE_GROUP>` |
| `AZURE_STATIC_WEB_APP_NAME` | `<STATIC_WEB_APP_NAME>` |
| `AZURE_PRODUCTION_URL` | `https://<STATIC_WEB_APP_NAME>.azurestaticapps.net` (or custom domain) |

Add these as **Environment Variables** (not secrets) to the `coding-school-production` GitHub Environment.

## 3. Azure Static Web App Configuration

### Create Static Web App (if not exists)
```bash
az staticwebapp create \
  --name <STATIC_WEB_APP_NAME> \
  --resource-group <RESOURCE_GROUP> \
  --location "East US 2" \
  --sku Standard \
  --login-with-azure-ad disabled \
  --branch main
```

### Build Configuration
- **App location**: `projects/coding-school-platform/app` (handled by CI artifact)
- **Output location**: `dist`
- **Build command**: Not used — `skip_app_build: true` in workflow
- **Deployment**: Prebuilt artifact from CI quality gates

### Domains
- **Default Azure URL**: `https://<STATIC_WEB_APP_NAME>.azurestaticapps.net`
- **Custom domain** (optional): Configure in Azure Static Web App → Custom domains

## 4. GitHub Repository Settings

### Branch Protection (`main`)
- Require PR reviews (1+)
- Require status checks to pass (from `coding-school-ci-quality-gates.yml`):
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

## 5. Workflow Behavior

### Triggers
- `workflow_dispatch` with `promote_production: true` input
- Only runs on `main` branch (enforced by `if` condition and environment branch policy)

### Deployment Flow
1. **Download artifact** — Downloads `coding-school-web-<sha>` artifact from `coding-school-ci-quality-gates.yml`
2. **Validate artifact** — Verifies `dist/` directory exists in artifact
3. **Validate OIDC config** — Checks all required Azure environment variables are set
4. **Azure login** — Uses `azure/login` v2 with OIDC (no secrets)
5. **Obtain ephemeral token** — Calls `az staticwebapp secrets list` to get one-time deployment token
6. **Deploy** — Uses `Azure/static-web-apps-deploy` v1 with `skip_app_build: true`
7. **Verify production identity** — Fetches production URL, asserts "Algorithm Academy" in HTML

### Security Controls
- **No long-lived secrets**: Uses GitHub OIDC workload identity federation
- **Least-privilege RBAC**: Service Principal has `Static Web Apps Contributor` on single resource only
- **Ephemeral deployment token**: Token fetched at deploy time, masked in logs, not stored
- **Protected environment**: Requires manual approval in GitHub UI before production job runs
- **Branch restriction**: Only `main` branch can trigger (OIDC subject + environment branch policy + workflow `if`)
- **Serialized production**: Concurrency via GitHub environment (one production deploy at a time)

### Artifacts
- No artifacts produced by this workflow (uses upstream CI artifact)

## 6. Rollback Procedure (Break-Glass)

If a bad production deployment needs immediate revert:

```bash
# 1. Record incident
cat > ops/rollback-evidence/production-rollback-<incident-id>.json <<'EOF'
{
  "incident_id": "<INCIDENT_ID>",
  "actor": "<GITHUB_ACTOR>",
  "approver": "<APPROVER>",
  "timestamp_utc": "<ISO_8601>",
  "reason": "<HUMAN_READABLE>",
  "app": "coding-school-platform",
  "target": "azure-production",
  "previous_commit_sha": "<SHA>",
  "current_commit_sha": "<SHA>",
  "azure_static_web_app": "<STATIC_WEB_APP_NAME>",
  "azure_resource_group": "<RESOURCE_GROUP>",
  "verification": { "smoke_passed": true, "identity_asserted": true }
}
EOF

# 2. Option A: Redeploy previous verified artifact (recommended)
#    - Find the previous successful `coding-school-web-<sha>` artifact
#    - Trigger workflow_dispatch with that SHA (requires workflow modification)
#    OR
#    - Use Azure Static Web App → Deployments → Redeploy previous deployment

# 3. Option B: Azure Portal rollback
#    - Go to Azure Static Web App → Deployments
#    - Find previous successful deployment
#    - Click "Redeploy" or "Promote to production"

# 4. Reconcile via GitHub Actions (within 1 business day)
#    - Push rollback-evidence commit
#    - Trigger production promotion with verified previous commit
```

## 7. Verification Checklist

After setup, verify by:

1. Ensure `coding-school-ci-quality-gates.yml` completes successfully on `main`
2. Ensure `coding-school-vercel-preview.yml` deploys verified immutable preview
3. Verify Oyama personally tests and approves the preview build (per 2026-09-02 policy)
4. Manually trigger `Coding School Production Promotion` workflow with `promote_production: true`
5. Watch production job:
   - Waits for required reviewer approval in GitHub UI
   - Downloads artifact from CI quality gates
   - Logs into Azure via OIDC
   - Deploys prebuilt artifact
   - Verifies "Algorithm Academy" identity
6. Open `AZURE_PRODUCTION_URL` — should show "Algorithm Academy" app
7. Verify production URL in workflow summary

## 8. Current Status

- **Workflow file**: `.github/workflows/coding-school-release.yml` ✅
- **CI Quality Gates workflow**: `.github/workflows/coding-school-ci-quality-gates.yml` ✅
- **Vercel Preview workflow**: `.github/workflows/coding-school-vercel-preview.yml` ✅
- **Build verified locally**: `npm run build:web` + `npm run smoke:web` + `npm run gate:inputs` ✅
- **GitHub Environment `coding-school-preview`**: Created, configured ✅
- **GitHub Environment `coding-school-production`**: Created with exact `main` branch policy; no required reviewer is configured because the private-repository plan exposes no environment-reviewer control and the repository has no independent collaborator ⚠️
- **Azure OIDC federated credential**: NOT VERIFIED; the six environment entries are placeholders, so the configured app registration cannot be identified safely
- **Azure Static Web App**: NOT VERIFIED from the placeholder configuration
- **Azure variables in `coding-school-production`**: All six names exist, but all six values are placeholders and must be replaced through GitHub Environment settings

> **Blocked on**: An independent GitHub reviewer must be added (and the plan upgraded if required), then configured with self-review prevention. The Azure owner must replace all six placeholder values, verify or create the Static Web App, and configure an exact OIDC credential with subject `repo:ItMeansBigMountain/HeRmEz:environment:coding-school-production`, issuer `https://token.actions.githubusercontent.com`, and audience `api://AzureADTokenExchange`. Do not promote production until both controls read back successfully.