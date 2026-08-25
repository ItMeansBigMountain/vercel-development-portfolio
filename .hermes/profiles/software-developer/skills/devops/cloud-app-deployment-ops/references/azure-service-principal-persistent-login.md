# Azure Service Principal Persistent Login Pattern

Use when the user wants Hermes to keep working with Azure/Terraform after a one-time interactive `az login`/PIM bootstrap, without repeatedly asking for device-code auth.

## What to create

1. Reuse or create one Entra application/service principal for Hermes-managed Terraform deployments.
2. Use GitHub OIDC federated credentials for Actions pipelines; do **not** put a client secret in GitHub Actions when OIDC works.
3. For local Hermes CLI/Terraform sessions only, create a service-principal credential and store it outside any repo in a chmod `600` env file.
4. Create a chmod `700` helper script that sources the env file and runs `az login --service-principal`.

## Role model

Minimum practical baseline for a subscription-wide Terraform deployer:

```text
Contributor                    /subscriptions/<subscription-id>
Storage Blob Data Contributor  /subscriptions/<subscription-id>/resourceGroups/<tfstate-rg>/providers/Microsoft.Storage/storageAccounts/<tfstate-storage>
```

Avoid granting Owner by default. If Terraform must create role assignments, add a narrow extra role intentionally and document why.

## Secret-safe local login helper

Example shape; never print or commit the env file:

```bash
# /opt/data/secrets/<name>.env, chmod 600
AZURE_CLIENT_ID=<client-id>
AZURE_TENANT_ID=<tenant-id>
AZURE_SUBSCRIPTION_ID=<subscription-id>
AZURE_CLIENT_SECRET=<secret>
```

```bash
#!/usr/bin/env bash
set -euo pipefail
AZ=(/path/to/python -m azure.cli)
SECRET_FILE="/opt/data/secrets/<name>.env"
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

Important shell pitfall: if the Azure CLI command includes spaces, define it as a Bash array (`AZ=(python -m azure.cli)`), not a scalar string, otherwise the helper may try to execute the entire string as a path.

## Device-code/PIM bootstrap pitfall

When using `az login --use-device-code`, Azure CLI may prompt:

```text
Select a subscription and tenant (Type a number or Enter for no changes):
```

In a PTY/background process, submit Enter after the user finishes the browser/MFA flow, otherwise the login may appear stuck even though browser auth succeeded.

## Cost guardrails

Entra app registrations, service principals, federated credentials, role assignments, and local credentials are free. This setup should not create paid resources by itself.

Before/after bootstrapping, verify live Azure resources with `az resource list` and call out any pre-existing resources separately from newly-created ones. Avoid adding VMs, AKS, Front Door, Application Gateway, Premium Functions, paid App Service plans, or high-volume telemetry unless the user explicitly approves cost.

## Pipeline pattern

- GitHub Actions: OIDC federation per GitHub Environment (`infra-dev`, `app-dev`, `infra-prod`, `app-prod`).
- Local Hermes: service-principal credential stored outside repo and used by helper script.
- Terraform state: central storage account/container with `Storage Blob Data Contributor` for the deployer identity.
- After Terraform apply, capture outputs and set GitHub variables for app deployment rather than hardcoding resource names.
