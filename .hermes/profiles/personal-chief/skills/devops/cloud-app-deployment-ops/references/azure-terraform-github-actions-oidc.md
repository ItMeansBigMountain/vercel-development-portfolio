# Azure Terraform + GitHub Actions OIDC Pattern

Use this pattern for Azure-hosted services where the user wants Terraform-managed infra and separate app deployment with approval gates.

## Trigger phrases

- User asks to set Hermes up with Azure / `az login` / PIM.
- User says **"pim up"**: start Azure CLI device-code login and provide the login URL/code.
- User wants GitHub Actions to run Terraform and a separate app deployment pipeline.
- User references their AZ-204 style repo/workflows.

## Auth model

Prefer GitHub Actions OIDC instead of long-lived Azure secrets.

Older examples in the user's repos used:

```text
AZURE_CREDENTIALS
AZURE_CLIENT_SECRET
publish-profile secrets
ACR username/password
```

Modern replacement for infra/app deployment auth:

```text
AZURE_CLIENT_ID       # GitHub variable, not secret
AZURE_TENANT_ID       # GitHub variable, not secret
AZURE_SUBSCRIPTION_ID # GitHub variable, not secret
permissions: id-token: write
azure/login@v2 with client-id/tenant-id/subscription-id
```

Do not ask the user to paste Azure tokens or service principal JSON. For local/bootstrap, use:

```bash
az login --use-device-code
az account set --subscription "<subscription>"
az account show --query '{tenantId:tenantId, subscriptionId:id, name:name}' -o table
```

If device-code login shows a subscription selection prompt in a tracked PTY, submit Enter to accept the `*` default. If MFA is required or the initial login reports a tenant-specific error, rerun with the tenant explicitly:

```bash
az login --use-device-code --tenant "<tenant-id>"
```

After login, verify the account was actually stored with `az account show`; browser success alone is not enough.

## Environment-gated federated credentials

Create one federated credential per GitHub Environment so approval gates matter:

```text
repo:<OWNER>/<REPO>:environment:infra-dev
repo:<OWNER>/<REPO>:environment:app-dev
repo:<OWNER>/<REPO>:environment:infra-prod
repo:<OWNER>/<REPO>:environment:app-prod
```

Use GitHub Environments:

```text
infra-dev   # Terraform dev plan/apply; require approval while learning costs
app-dev     # app deployment to dev
infra-prod  # always approval-gated
app-prod    # always approval-gated
```

## Pipeline split

Same repo can have multiple workflows. For service repos, keep infra and app separate:

```text
.github/workflows/infra-terraform.yml
.github/workflows/app-deploy.yml
```

Infra workflow path filter:

```yaml
paths:
  - 'infra/**'
  - '.github/workflows/infra-terraform.yml'
```

App workflow path filter:

```yaml
paths:
  - 'api/**'
  - 'web/**'
  - 'tests/**'
  - '.github/workflows/app-deploy.yml'
```

Rules:

- Infra pipeline runs `terraform fmt`, `init`, `validate`, `plan`, and only applies on manual dispatch + approval.
- Add an explicit preflight step before `azure/login` that fails clearly if `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, or `TFSTATE_*` variables are missing; otherwise `azure/login` fails with a less helpful “Not all values are present”.
- App pipeline tests/packages/deploys Function App or Static Web App code; it does not run Terraform.
- Terraform state should live outside the app resource group, e.g. `rg-cwb-tfstate` + storage container `tfstate`.
- If an apply fails and the immediate retry reports `state blob is already locked`, wait briefly/check the lock; many locks clear after the failed runner exits. Only `terraform force-unlock` a known stale lock after confirming no active run is using it.

## Terraform layout

Use service-owned infra:

```text
service-repo/
  infra/terraform/
    versions.tf
    providers.tf
    main.tf
    variables.tf
    outputs.tf
    env/dev.tfvars
    env/prod.tfvars
```

For AzureRM provider with OIDC:

```hcl
provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
  use_oidc        = true
}
```

Use backend config from Actions rather than hardcoding state account names.

## Cost guardrails for near-free Azure services

- Azure Functions Consumption plan: `sku_name = "Y1"`.
- Cosmos DB free tier: `free_tier_enabled = true`; create correctly the first time.
- Cosmos shared throughput should be capped between 400 and 1000 RU/s.
- Static Web App SKU should be Free.
- Avoid Front Door, App Gateway, Premium Functions, AKS, VMs, and paid App Service plans for MVP.
- Add budget alerts before public traffic.

## Verification

When Terraform is available, run:

```bash
terraform fmt -recursive -check infra/terraform
terraform -chdir=infra/terraform init -backend=false
terraform -chdir=infra/terraform validate
```

Also parse workflow YAML and run app tests before committing/pushing.
