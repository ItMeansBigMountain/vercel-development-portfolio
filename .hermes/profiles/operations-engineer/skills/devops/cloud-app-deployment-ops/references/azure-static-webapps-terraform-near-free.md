# Azure Static Web Apps + Terraform near-free deployment lessons

Use this for Azure near-free web/API services, especially when avoiding surprise costs.

## Free-safe identity pattern

- Use an Entra app/service principal as the deployment identity; app registrations and service principals are free.
- Prefer GitHub Actions OIDC/federated credentials for pipelines; do not store a client secret in GitHub.
- A local persistent login may use a client secret stored outside the repo with `600` permissions and a helper script with `700` permissions, but never print or commit the secret.
- Minimal roles used successfully:
  - `Contributor` on the subscription for Terraform resource deployment.
  - `Storage Blob Data Contributor` on the Terraform state storage account.
- Do not grant `Owner` unless role assignment management is genuinely required.

## Terraform state/bootstrap pattern

- Bootstrap a dedicated state resource group + storage account + blob container.
- Apply app/resource tags to both state and app resources:
  - app/project name
  - environment
  - repo
  - `ManagedBy=Terraform`
  - `DeployedBy=HermesAgent`
  - cost guardrail tag such as `CostGuard=near-free`
- Tagging is free and safe. Renaming Azure resource groups/Cosmos accounts can force moves/recreates and should not be done casually, especially with Cosmos free-tier limits.

## Azure Functions quota workaround

- If Azure blocks Function/App Service Plan creation with zero quota, do not jump to paid App Service or VMs.
- Keep the near-free path by using Azure Static Web Apps Free with managed API when possible.
- This can host static frontend plus API without a separate Function App/App Service Plan resource.

## Static Web Apps routing gotchas

- Clean frontend routes need `navigationFallback` in `staticwebapp.config.json`.
- When deploying a `web/` app root, include `staticwebapp.config.json` under `web/` so Static Web Apps actually applies it.
- Verify direct routes (`/clans`, `/leaderboard`, etc.) with HTTP status checks after deployment; client-side navigation alone can hide 404s.

## Workflow trigger rules

- Keep infra and app pipelines separate.
- Infra workflow should trigger only on `infra/**` and the infra workflow file, plus manual dispatch.
- App workflow should trigger only on app/API/frontend/deploy-config files and the app workflow file, plus manual dispatch.
- Do not trigger app deploys just because unrelated tests/docs changed unless those tests/docs are part of the deploy validation contract.

## Cost guardrails

Avoid by default unless explicitly accepted:

- App Service paid plans
- Functions Premium
- VMs
- AKS
- Front Door / Application Gateway
- Cosmos DB non-free-tier or multi-region writes

Prefer early MVP shape:

- Azure Static Web Apps Free
- Cosmos DB Free Tier when storage is needed
- GitHub Actions OIDC
- Terraform remote state in cheap storage
