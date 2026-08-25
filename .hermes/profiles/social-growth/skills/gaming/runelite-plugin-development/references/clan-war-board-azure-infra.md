# Clan War Board Azure infrastructure planning

Use when extending `projects/osrs-plugins/in-progress/CompetitionOverlay` / Clan War Board beyond local config into an online service.

## User preference and organization

- The user **does not want local/share-code-only storage** as the main solution for clan wars.
- The user wants to explore **near-free Azure hosting** for global game-wide war data.
- Keep infra separate from RuneLite Plugin Hub PR work:

```text
projects/osrs-plugins/
  in-progress/CompetitionOverlay/     # RuneLite plugin; Plugin Hub-facing only
  infra/
    clan-war-board-azure-plan.md      # plan/tracker
    clan-war-board-service/           # future backend service repo/submodule
```

The backend should become a separate project/repo, likely `clan-war-board-service`, mounted under `projects/osrs-plugins/infra/` as a submodule if/when implemented.

## Recommended Azure near-free MVP

Preferred stack:

```text
Azure Static Web Apps Free
Azure Functions Consumption
Azure Cosmos DB Free Tier
```

Rationale:

- Static Web Apps can host a public/admin web UI later.
- Functions Consumption avoids an always-on server.
- Cosmos DB Free Tier can persist clans/wars/acceptance data if explicitly enabled at account creation.

Avoid for MVP:

- always-on App Service plans
- VMs
- Application Gateway / Front Door
- paid database tiers
- heavy Application Insights/logging

Add Azure budget alerts immediately.

## Plugin/backend boundary

The RuneLite plugin should contain:

- clan/rank detection
- leader/member UI
- online-sync config toggle and data warning
- small HTTPS API client
- mocked API tests

The service repo should contain:

- Azure Functions API
- Cosmos DB data access
- optional Static Web Apps frontend
- Bicep/Terraform IaC
- privacy/API/deployment docs

Do not put Azure IaC or deployment secrets in the Plugin Hub-facing RuneLite repo.

## Privacy rules

Upcoming wilderness war details are PvP intel.

Public before war:

- clan names
- status such as proposed/confirmed
- broad category

Clan/member-only before war:

- exact date/time
- world
- hotspot/location
- rules/rally notes

Leader-only:

- drafts
- proposal/accept controls
- edit/cancel controls
- acceptance history

Public after war:

- sanitized completed-war summary if leaders mark it public.

## Agreement model

Backend owns agreement state. Do not use local import/export codes as the main solution.

Lifecycle:

```text
DRAFT -> PROPOSED -> CONFIRMED -> COMPLETED/CANCELLED
```

Store a `termsHash` over the mutually agreed terms:

```text
creator clan, opponent clan, war name, start time, duration, world, hotspot, rules, visibility
```

If any terms change after acceptance, set status to `RECONFIRM_REQUIRED` and require the other leader to accept the updated terms.

## V1 verification stance

RuneLite can observe local clan channel rank; a backend cannot perfectly verify that at first.

V1:

- plugin submits player name, clan name, and locally observed rank
- backend records actions as plugin-submitted
- clans can be marked unverified initially

V2:

- clan claiming
- Discord OAuth/bot verification for clan leader roles
- verified clan badges and stricter leader permissions

## First implementation steps

1. Create `projects/osrs-plugins/infra/clan-war-board-service` as a new service repo/submodule.
2. Add `infra/main.bicep` for Static Web Apps, Functions, and Cosmos DB Free Tier.
3. Implement `GET /api/health`.
4. Add data model for clan, war, acceptance, visibility.
5. Add plugin `Enable Online Sync` config and Plugin Hub-safe warning.
6. Wire plugin API client only after privacy warning and tests exist.
