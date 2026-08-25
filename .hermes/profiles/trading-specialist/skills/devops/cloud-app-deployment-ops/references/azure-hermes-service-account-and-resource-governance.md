# Azure Hermes Service Account and Resource Governance Pattern

Use when the user wants Hermes/GitHub Actions to deploy Azure/Terraform projects repeatedly without device-code login every session, while avoiding surprise costs.

## Identity pattern

- Prefer one reusable Entra application/service principal for Hermes-managed Terraform deployments in the target subscription.
- GitHub Actions should use OIDC federated credentials scoped by GitHub Environment, not stored Azure client secrets.
- Local Hermes CLI sessions may use a service-principal credential stored outside any repo, with `0600` permissions, plus a helper script that logs in and selects the subscription.
- Do not print the client secret or commit it. Document the secret file path and helper script path, but never the secret value.

Example local helper shape:

```bash
#!/usr/bin/env bash
set -euo pipefail
AZ=(/path/to/python -m azure.cli)
SECRET_FILE="/opt/data/secrets/<service-principal>.env"
set -a
source "$SECRET_FILE"
set +a
"${AZ[@]}" login --service-principal \
  --username "$AZURE_CLIENT_ID" \
  --password "$AZURE_CLIENT_SECRET" \
  --tenant "$AZURE_TENANT_ID" \
  -o none
"${AZ[@]}" account set --subscription "$AZURE_SUBSCRIPTION_ID"
"${AZ[@]}" account show --query '{subscription:id,tenant:tenantId,user:user.name}' -o json
```

## Roles

- For broad Hermes Terraform work in a subscription: `Contributor` at subscription scope is usually sufficient for resource creation.
- Add `Storage Blob Data Contributor` on the Terraform state storage account so Terraform can read/write remote state.
- Avoid `Owner` by default. If Terraform must create role assignments, add the narrowest extra role intentionally and document why.

## Cost and resource safety

- Creating Entra apps, service principals, federated credentials, role assignments, and local login helper files is free.
- Do not create paid resources just to create a deployment identity.
- Verify resource inventory after identity setup to ensure no VMs/App Service plans/AKS/Front Door/App Gateway/Premium plans appeared.

## Tags and naming

Always tag live resources and Terraform defaults with app identity and Hermes provenance:

```text
AppName=<HumanAppName>
AppSlug=<app-slug>
Project=<ProjectName>
Service=<service-slug>
Environment=<dev|prod|shared>
ManagedBy=Terraform
DeployedBy=HermesAgent
DeploymentTool=HermesAgent
IaC=Terraform
Repository=<owner/repo>
CostGuard=near-free
Purpose=<TerraformState|...>   # when relevant
```

Do not casually rename existing Azure resources. Resource groups and Cosmos DB accounts cannot be safely renamed in place; renaming usually means recreate/move. For Cosmos DB Free Tier, replacement can collide with the one-free-tier-account-per-subscription limit. Prefer safe tag updates unless the user explicitly approves recreation and cost risk.

## Resource group / portal links

When reporting Azure resources, return Azure Portal URLs for resource groups and important resources using this shape:

```text
https://portal.azure.com/#@<tenant-id>/resource/subscriptions/<subscription-id>/resourceGroups/<resource-group>/overview
https://portal.azure.com/#@<tenant-id>/resource/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/<provider>/<type>/<resource-name>/overview
```

## Verification checklist

- `az account show` succeeds as either user or service principal.
- Service principal role assignments are listed and match intended scope.
- GitHub repo variables/environments/OIDC subjects exist.
- Resource inventory is reviewed for cost surprises.
- Tags are applied live and committed to Terraform defaults.
- Terraform validates after tag/default changes.
