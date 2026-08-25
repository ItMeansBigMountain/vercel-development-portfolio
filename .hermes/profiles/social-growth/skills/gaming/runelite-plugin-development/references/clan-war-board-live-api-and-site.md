# Clan War Board live API + production website lessons

Use when continuing Clan War Board RuneLite/plugin/service work.

## Product and UX rules

- Public website must use real data only. Do not show faux/example clans, fake fights, fake battle summaries, or placeholder copy that implies production data exists.
- If no real leader-posted fights or completed telemetry exist yet, show clean empty states:
  - Open fights: “No open challenges yet.”
  - Results: “No published results yet.”
- Website should feel like an OSRS clan adversary site: parchment/brown/gold panels, old-brick accents, OSRS/Wilderness imagery, and customer-facing clan competition language.
- Keep public navigation focused: Home, Clans, Open fights, Results. Put match/setup terms at the bottom of the home page, not in a separate tab.
- Avoid customer-visible developer language on public pages: API, fake data, seed data, endpoints, RuneLite write endpoints, source panel, deployment notes, or internal implementation caveats.

## Current free Azure site/API stack

- Azure Static Web Apps Free with managed Python API under `api/`.
- Public site under `web/`.
- Clean client routes require `web/staticwebapp.config.json` with `navigationFallback` to `/index.html`; keeping only a root-level `staticwebapp.config.json` did not make `/clans`, `/fights`, etc. load directly.
- App pipeline should deploy only when app/API/site/config workflow paths change; infra pipeline only when `infra/**` or its workflow changes.

## Real data sources used

- Wise Old Man Groups API:
  - `GET https://api.wiseoldman.net/v2/groups?limit=N` returns real public groups.
  - `GET https://api.wiseoldman.net/v2/groups/{id}` returns group detail including `memberships` with player metadata such as role/build/status/type.
- OSRS Wiki MediaWiki API:
  - Use `action=query&prop=pageimages&piprop=thumbnail|original&pithumbsize=...&titles=Wilderness|Clan Wars|Revenant Caves` for real OSRS imagery.
  - OSRS Wiki theme colors include parchment/browns/gold/old-brick values; use them rather than generic SaaS styling.

## RuneLite plugin integration pattern

- Online Sync must default off.
- Config should include `Enable Online Sync` and `Service URL`.
- Disclosure should mention that online sync contacts the Clan War Board service and future write endpoints may send display name, clan name, rank, leader actions, and fight telemetry.
- Read-only API calls that are safe to wire first:
  - `GET /api/health`
  - `GET /api/clans`
  - `GET /api/public/availability`
- Add headers from plugin calls:
  - `User-Agent: ClanWarBoard-RuneLite/<version>`
  - `X-Clan-War-Board-Client: runelite`
- Keep network calls off the Swing UI thread. Use a background future/executor, then update the panel on the Swing thread.
- Panel should show concise status only: connected/unavailable, public clans indexed, open challenges.

## Verification checklist

- Service tests: `python3 -m unittest discover -s tests -v`.
- Plugin build: `JAVA_HOME=/opt/data/jdks/current-java11 ./gradlew clean test assemble --no-daemon --console=plain`.
- Java API smoke: compile/run a tiny class that instantiates the plugin API client against the live base URL and verifies `online=true` and `clans > 0`.
- Live website verification:
  - `/`, `/clans`, `/fights`, `/results` return HTTP 200.
  - Home page contains the match/setup terms section.
  - Nav does not include Match Terms.
  - Browser-rendered pages load OSRS-themed styling and real WOM clan cards.
