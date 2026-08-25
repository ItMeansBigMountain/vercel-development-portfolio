# Azure Static Web Apps Free + Python managed API notes

Use this pattern when the user wants a near-free Azure-hosted public website plus REST-style endpoints and strict cost guardrails.

## Free/near-free architecture

- Azure Static Web Apps Free for the public frontend.
- Static Web Apps managed Functions API for Python endpoints under `/api/*`.
- Cosmos DB Free Tier may be provisioned for persistence, but only one free-tier account is allowed per subscription; avoid recreating it casually.
- Avoid App Service Plans, Functions Premium, Container Apps, VMs, Front Door, Application Gateway, and AKS when the user says no surprise costs.

## Quota workaround

Some subscriptions have zero App Service/Functions plan quota even for Consumption/Y1. If Terraform fails creating an App Service plan with a quota message such as `Current Limit (Total VMs): 0`, switch to Static Web Apps managed API instead of requesting paid capacity.

## Static Web Apps clean routes

For client-side clean routes such as `/clans`, `/fights`, `/results`, place `staticwebapp.config.json` inside the deployed app root (for example `web/staticwebapp.config.json`), not only at repo root. Include:

```json
{
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/api/*", "/*.{css,scss,js,png,gif,ico,jpg,svg,webp,avif}"]
  }
}
```

Verify direct URL loads with `curl -I https://.../route` after deployment, not just client-side clicks.

## Pipelines

Split workflows:

- `infra-terraform.yml`: trigger only on `infra/**` and the workflow file, plus manual dispatch.
- `app-deploy.yml`: trigger only on application deploy inputs such as `api/**`, `web/**`, `staticwebapp.config.json`, and the workflow file, plus manual dispatch. Avoid deploying just because unrelated docs/tests changed unless tests are part of the deploy package.

Use GitHub OIDC with environment-specific federated credentials. Do not store Azure client secrets in GitHub when OIDC works. A local service-principal secret can be useful for the agent runner, but keep it outside repos with `0600` permissions and never print it.

## Resource naming and tags

Do not rename/recreate Azure resources just to improve names if it risks downtime or costs. Tag safely in place and update Terraform defaults. Useful tags:

- `AppName=...`
- `AppSlug=...`
- `Service=...`
- `ManagedBy=Terraform`
- `DeployedBy=HermesAgent`
- `DeploymentTool=HermesAgent`
- `IaC=Terraform`
- `Repository=owner/repo`
- `CostGuard=near-free`

Return Azure Portal resource-group URLs after provisioning/tagging.

## Product-stack caution

If the user asks for Django-style REST+HTML but also requires free Azure hosting, call out the tradeoff: traditional Django usually implies App Service/Container/VM-style hosting and may stop being reliably free. Preserve the Django product model via same-origin HTML + `/api/*` first, then only move to Django if the user accepts the cost/hosting tradeoff.
