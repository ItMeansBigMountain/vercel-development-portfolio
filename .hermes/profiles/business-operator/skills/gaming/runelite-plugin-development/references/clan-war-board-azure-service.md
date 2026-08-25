# Clan War Board Azure Service Planning

Session-derived pattern for the Clan War Board / CompetitionOverlay pivot when the user wants game-wide shared data rather than local share codes.

## Organization

Keep the RuneLite Plugin Hub repo and the backend service separate.

Preferred workspace layout:

```text
projects/osrs-plugins/
  in-progress/ClanWarBoard/                 # RuneLite plugin only / Plugin Hub-facing
  services/
    clan-war-board-service/                 # backend/service project
      api/                                  # Azure Functions API
      web/                                  # optional Static Web Apps frontend
      infra/                                # service-owned Bicep/Terraform IaC
      docs/                                 # cost, privacy, security, API contract
```

Important user correction: keep `infra/` **inside the service** because the infra belongs to the service; do not keep a separate top-level osrs-plugins infra directory for this backend.

## Naming consistency

When pivoting `CompetitionOverlay` to the product direction, rename consistently to `Clan War Board`:

- Gradle root project: `ClanWarBoard`
- package: `com.itmeansbigmountain.clanwarboard`
- classes: `ClanWarBoardPlugin`, `ClanWarBoardConfig`, `ClanWarBoardPanel`
- config group: `clanwarboard`
- Plugin Hub display name: `Clan War Board`
- repo/path target: `clan-war-board-osrs`, `in-progress/ClanWarBoard`

If moving the plugin folder as a submodule, update `.gitmodules`, remote URL, child remote, parent gitlink, and verify both child and parent push SHAs.

## Backend direction

The user rejected local/share-code persistence for this class of work. For Clan War Board, plan a central backend API plus public/static leaderboard instead:

- initial public API: `GET /api/health`, `GET /api/leaderboard`, `GET /api/clans/{clanId}`
- leaderboard should be static/sample-backed first, then Cosmos-backed
- public leaderboard uses completed/sanitized war summaries only
- do **not** expose upcoming world/time/hotspot/rally intel publicly

## Free Azure target

Preferred near-free Azure stack:

```text
Azure Static Web Apps Free
Azure Functions Consumption
Azure Cosmos DB Free Tier
```

Cost/security constraints:

- Cosmos DB must be created with `enableFreeTier=true`; it cannot be toggled later.
- Cosmos free tier allows 1000 RU/s and 25 GB storage; keep shared DB throughput <= 1000 RU/s.
- Functions Consumption has a monthly free grant, but the required storage account is separate and can incur small cost.
- Static Web Apps Free is suitable for public/admin static pages.
- Add budget alerts before public traffic.
- Avoid VMs, paid App Service plans, Premium Functions, Front Door, Application Gateway, AKS, Cosmos serverless, and noisy telemetry for MVP.

## Security stance

Assume attackers because public PvP/clan infrastructure attracts abuse:

- fake clans/leaders
- spam war creation
- leaderboard manipulation
- scraping upcoming war intel
- API flooding to burn free-tier quota
- payload abuse and log-cost abuse

MVP can be community-trust based with plugin-observed clan/rank, but label unverified clans. Later add clan claiming, Discord OAuth/bot role verification, and verified leader accounts.

Plugin Hub warning must disclose online sync sends player name, clan name, observed clan rank, plugin version, and war actions to the service.

## Wise Old Man integration

Wise Old Man has groups/clans. Treat WOM as optional enrichment only:

Allowed after opt-in:

- WOM group ID/name
- public member list/player names
- public WOM ranks/scores/metrics

Not authority for:

- leader permissions
- private war details
- upcoming world/hotspot/time

Cache WOM reads and identify the service with a User-Agent when implemented.
