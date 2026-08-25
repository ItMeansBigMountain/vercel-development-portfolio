# Azure near-free serverless backend pattern

Use when the user wants a low/near-free Azure-hosted backend for a small app/service without committing to always-on infrastructure.

## Preferred MVP stack

```text
Azure Static Web Apps Free
Azure Functions Consumption
Azure Cosmos DB Free Tier
```

Good for:

- lightweight HTTP APIs
- small public/admin web frontends
- document-shaped app data
- hobby/MVP traffic

Cost controls:

- explicitly enable Cosmos DB Free Tier at account creation
- one Cosmos DB free-tier account per subscription
- use Azure Functions Consumption, not Premium/App Service Plan
- use Static Web Apps free tier
- add budget alerts immediately
- keep logging/Application Insights low-volume
- avoid VMs, always-on App Service, Front Door, Application Gateway, paid database defaults

## Alternative relational option

If joins/reporting matter more than document simplicity:

```text
Azure Functions Consumption + Azure SQL Database free offer + Static Web Apps
```

Caution: verify the Azure SQL free database option is selected during deployment; Azure portal defaults can land on billable tiers.

## Project organization pattern

Keep infra/backend separate from client/plugin repos when the client is reviewed or distributed independently.

Example for OSRS RuneLite plugin + backend:

```text
plugin-repo/              # client-only, review-facing
infra/service-repo/       # Azure Functions, web UI, IaC, deployment docs
```

Use Bicep for Azure IaC unless Terraform is specifically needed.

## First implementation sequence

1. Create dedicated service repo/project.
2. Add `infra/main.bicep` for resource group resources.
3. Implement `GET /api/health`.
4. Deploy and verify live health URL before adding business logic.
5. Add database schema/containers with minimal throughput/free-tier settings.
6. Add privacy/cost docs and budget-alert setup.
