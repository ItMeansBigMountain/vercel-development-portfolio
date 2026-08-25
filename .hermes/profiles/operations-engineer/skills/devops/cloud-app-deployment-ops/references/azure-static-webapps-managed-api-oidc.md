# Azure Static Web Apps Managed API + OIDC Pattern

Use this when the user wants a near-free Azure API + website with Terraform/GitHub Actions and strict cost guardrails.

## Near-free stack that worked

When Azure Functions/App Service plan creation is blocked by subscription quota or risks paid capacity, keep the app on:

```text
Azure Static Web Apps Free
  web/      static frontend
  api/      managed Azure Functions API
Cosmos DB Free Tier
Terraform remote state in a Storage Account
GitHub Actions OIDC for deploy identity
```

Static Web Apps managed API lets the app deploy `web/` and `api/` together without a separately provisioned Function App/App Service Plan. This preserves a free/near-free deployment path and avoids surprise App Service plan capacity.

## Pipeline split

Use two workflows:

```text
.github/workflows/infra-terraform.yml
.github/workflows/app-deploy.yml
```

Infra should trigger only on:

```yaml
paths:
  - 'infra/**'
  - '.github/workflows/infra-terraform.yml'
```

App deploy should trigger only on real app/deploy-config changes:

```yaml
paths:
  - 'api/**'
  - 'web/**'
  - 'staticwebapp.config.json'
  - '.github/workflows/app-deploy.yml'
```

Do not trigger app deployment on `tests/**` alone unless the user explicitly wants redeploys for test-only changes.

## OIDC/service account shape

Use an Entra app/service principal as the deployment identity and federated credentials for GitHub environments:

```text
repo:<owner>/<repo>:environment:infra-dev
repo:<owner>/<repo>:environment:app-dev
repo:<owner>/<repo>:environment:infra-prod
repo:<owner>/<repo>:environment:app-prod
```

Roles that covered this class of deployment:

```text
Contributor on subscription or deployment scope
Storage Blob Data Contributor on Terraform state storage account
```

No client secret is needed in GitHub Actions. A local persistent service-principal login can be created for Hermes only if the user explicitly asks; store it outside repos, chmod 600, and never print it.

## Workflow preflight

Before `azure/login`, add explicit checks for blank GitHub variables so failures are actionable:

```text
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
TFSTATE_RESOURCE_GROUP
TFSTATE_STORAGE_ACCOUNT
TFSTATE_CONTAINER
```

For app deploy also require:

```text
AZURE_RESOURCE_GROUP
AZURE_STATIC_WEB_APP_NAME
```

## Static Web Apps deploy

Use Azure CLI OIDC to fetch the SWA deployment token at runtime, then pass it to `Azure/static-web-apps-deploy@v1`:

```bash
token=$(az staticwebapp secrets list \
  --name "$AZURE_STATIC_WEB_APP_NAME" \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --query "properties.apiKey" -o tsv)
```

This avoids storing a long-lived Static Web Apps deployment token as a repo secret.

## Resource naming and tags

If resources already exist, do not recreate/rename Cosmos DB just for aesthetics: Cosmos free tier is one-account-per-subscription and replacement can risk cost/downtime. Instead, apply/commit clear tags:

```text
AppName=<ProductName>
AppSlug=<product-slug>
Project=<ProductName>
Service=<service-slug>
ManagedBy=Terraform
DeployedBy=HermesAgent
DeploymentTool=HermesAgent
IaC=Terraform
Repository=<owner/repo>
CostGuard=near-free
Environment=<dev|prod|shared>
```

Return Azure Portal resource group URLs after deployment using:

```text
https://portal.azure.com/#@<tenantId>/resource/subscriptions/<subscriptionId>/resourceGroups/<rg>/overview
```

## Verification checklist

- `terraform fmt -recursive -check .`
- `terraform validate`
- GitHub workflow YAML parses
- App tests pass
- Infra workflow successful run URL captured
- App workflow successful run URL captured
- Live `/api/health` checked
- Live website checked visually when frontend changes
- Resource tags verified live
