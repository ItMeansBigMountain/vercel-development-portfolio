# Azure Static Web Apps free-tier deployment pattern

Use when deploying Hermes-managed web/API projects to Azure while avoiding surprise cost.

## Cost-safe identity pattern

- Prefer one reusable Entra app/service principal for Hermes-managed Terraform deployments in the subscription.
- GitHub Actions should use OIDC federated credentials, not stored client secrets.
- Local persistent login can use a service-principal credential stored outside repos with restrictive permissions; do not print or commit the secret.
- Assign only required roles:
  - `Contributor` on the subscription/resource group scope needed for Terraform.
  - `Storage Blob Data Contributor` on the Terraform state storage account.
  - Avoid `Owner` unless role assignments are explicitly required and approved.
- Creating Entra app credentials and GitHub OIDC federated credentials is free; verify no paid resources were added by listing actual Azure resources after setup.

## Static Web Apps + managed API pattern

- Azure Static Web Apps Free can host the public site plus managed API without a separate Function App/App Service plan.
- This is useful when the subscription has App Service/Functions plan quota blocked or when the user wants no surprise compute cost.
- Put frontend files under `web/` and API files under `api/`.
- Clean routes such as `/clans`, `/fights`, `/results` require `web/staticwebapp.config.json` with:

```json
{
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/api/*", "/*.{css,scss,js,png,gif,ico,jpg,svg,webp,avif}"]
  }
}
```

A repo-root `staticwebapp.config.json` alone may not apply when the app root is `web/`.

## Pipeline triggers

- Infra workflow should trigger only for `infra/**` and infra workflow file changes, plus manual `workflow_dispatch`.
- App workflow should trigger only for `api/**`, `web/**`, Static Web Apps config, app workflow changes, plus manual `workflow_dispatch`.
- Tests-only/doc-only changes should not deploy the app unless the workflow intentionally includes those paths.

## Tagging/naming

- Use app-specific Azure names and explicit tags:
  - `AppName`
  - `AppSlug`
  - `Project`
  - `Service`
  - `ManagedBy=Terraform`
  - `DeployedBy=HermesAgent`
  - `DeploymentTool=HermesAgent`
  - `IaC=Terraform`
  - `Repository`
  - `CostGuard=near-free`
- Avoid recreating resources solely for names if it risks cost/downtime; tag live resources safely and update Terraform defaults for future applies.
- Cosmos DB free tier is one account per subscription; do not casually recreate it to rename.

## Verification

- After deployment, return Azure Portal URLs for resource groups and important resources.
- Verify live endpoints with HTTP requests and browser-rendered pages.
- Confirm GitHub workflow runs succeeded and return workflow/run URLs.
