# Azure Free-Tier Service Planning Pattern

Use when planning a small backend/API where the user explicitly wants Azure and near-free hosting.

## Preferred near-free stack for lightweight APIs

```text
Azure Static Web Apps Free        # static site/admin/public pages
Azure Functions Consumption       # HTTP API, no always-on compute
Azure Cosmos DB Free Tier         # persistent data, provisioned throughput
```

Cosmos DB free-tier facts to verify at deployment time:

- `enableFreeTier=true` must be set when the account is created.
- Free tier cannot be enabled later on the same account.
- One Cosmos DB free-tier account per Azure subscription.
- Free tier is for provisioned throughput, not serverless accounts.
- Keep total free-tier use within 1000 RU/s and 25 GB storage.

Functions Consumption notes:

- Has a monthly free grant for executions/GB-s, but the backing Storage Account is separate and can incur small costs.
- Avoid Premium/Flex Always Ready/App Service plans when the user says free/near-free.

Static Web Apps Free notes:

- Good for public/static pages and a small admin UI.
- Keep assets small and bandwidth low.

## Cost-control checklist

- Dedicated resource group, e.g. `rg-<service>-dev`.
- Budget alerts before public traffic, e.g. warning at $5 and critical at $10.
- No VMs, AKS, Front Door, Application Gateway, Premium Functions, paid App Service plans, or paid Cosmos throughput for MVP.
- Minimize Application Insights/logging; no full request body logging.
- Design client polling conservatively; prefer manual refresh, ETags, caching, and static snapshots for public leaderboards.

## Service-owned infra organization

When the backend is a distinct product/service, keep IaC inside the service repo/project:

```text
service/
  api/
  web/
  infra/
  docs/
```

Do not keep a disconnected top-level infra folder if the user wants the service to own its deployment.

## Security-first planning for public game/community APIs

Assume hostile traffic for public competitive tools. Plan for:

- fake identities / impersonation
- spam submissions
- leaderboard manipulation
- scraping sensitive data
- request flooding that burns free-tier quotas
- log-volume cost abuse

Build privacy boundaries and rate limits into the first API contract, not after launch.
