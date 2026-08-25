# Clan War Board live service + plugin sync lessons

Use this when working on Clan War Board's RuneLite plugin, Azure service, or public website.

## Product/workflow corrections from the user

- The public website must read like a production OSRS clan adversary site, not a developer demo. Do not expose internal phrases like "fake data", "real clans/no fake data", "development tweak", "API" nav links, or implementation notes in public copy.
- Tabs/pages should be separate public pages for main sections (`/clans`, `/fights`, `/results`) rather than one cramped scroller. Exception: **match terms belong at the bottom of the home page**, not as its own nav tab.
- The plugin must use the online service by default. For Clan War Board, Online Sync is required for the product to work; do not provide an `Enable Online Sync` disable toggle. Keep only a service URL/config if needed.
- Upcoming fight details such as exact world, rally/location, time, and rules are PvP intel. Public website endpoints should show sanitized/public challenge data; sensitive details are for participating clans/plugin authorization later.

## Current live stack shape

- Service repo: `ItMeansBigMountain/clan-war-board-service`.
- Plugin repo moved to: `ItMeansBigMountain/clan-war-board-osrs`.
- Live service base URL used by the plugin: `https://salmon-dune-01c80c60f.7.azurestaticapps.net`.
- Hosting path that stayed near-free: Azure Static Web Apps Free with managed API under `api/`; avoid separate Function App/App Service Plan when subscription quota blocks Consumption/Y1 plan creation.
- Static Web Apps route fallback belongs in the deployed app root (`web/staticwebapp.config.json`), not only the repo root, for direct clean routes like `/clans` and `/fights` to return 200.

## Real data and OSRS theme

- Do not seed fake clan/fight data on the public site. Use real public sources where possible:
  - Wise Old Man Groups API for public clan/group directory and real group membership/build metadata.
  - OSRS Wiki MediaWiki API for real OSRS/Wilderness/Clan Wars/Revenant Caves imagery and theme assets.
- If no real fights or telemetry exist yet, render production empty states such as “No open challenges yet” / “No published results yet” rather than fabricated examples.
- Public website should feel OSRS-adjacent: parchment/brown/gold palette, serif headings, OSRS/Wiki imagery, competitive clan copy.

## Plugin integration pattern

- Add a small Java API client in the plugin (e.g. `ClanWarBoardApiClient`) using Java 11 `HttpClient` or RuneLite's HTTP client where appropriate.
- Always send identifying headers, e.g. `User-Agent: ClanWarBoard-RuneLite/1.0` and `X-Clan-War-Board-Client: runelite`.
- Read-only initial sync endpoints used by plugin:
  - `GET /api/health`
  - `GET /api/clans`
  - `GET /api/public/availability`
- Display service status in the narrow RuneLite panel: connected/unavailable, public clan count, open challenge count.
- Keep writes/auth as future work: leader availability posts, fight agreement, member telemetry, event batches, idempotency keys, and server-side validation.

## Verification checklist

- Website/service: run unit tests, parse HTML/config, deploy through app pipeline, verify live routes (`/`, `/clans`, `/fights`, `/results`) return 200, and browser-check rendered page copy.
- Plugin: run with Java 11: `./gradlew clean test assemble --no-daemon --console=plain`.
- Plugin/service integration: compile/run a tiny Java smoke using `ClanWarBoardApiClient.fetchStatus(DEFAULT_SERVICE_URL)` and require `online=true` plus a positive clan count.
- After child repo pushes, update/push the HeRmEz parent submodule pointer.
