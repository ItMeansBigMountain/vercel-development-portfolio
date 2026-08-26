# Clan War Board service integration + public site UX lessons

Use this when continuing Clan War Board, or any RuneLite plugin backed by a public web/API service.

## Product rules learned

- Clan War Board is not a local/share-code plugin; the plugin requires online service sync to function as a real multi-clan competition board.
- Do not expose an `Enable Online Sync` user toggle for Clan War Board. Keep a service URL override if useful, but sync itself is required.
- The plugin should call the service on startup/login and show connection status, public clan count, and open challenge count in the RuneLite panel.
- Website copy must be public/product-facing. Do not mention internal development reminders such as “real clans / no fake data” as copy; encode that as behavior.
- No faux clan/fight data on the public site. Do **not** promote random external clan directories; Clan War Board clan listings should come only from clans seen/registered through the RuneLite plugin or leader registration. Show empty states until real plugin clans/fights/telemetry exist.

## Current service/API integration shape

- Service base URL used in the plugin: `https://salmon-dune-01c80c60f.7.azurestaticapps.net`.
- Read endpoints the plugin can safely use now:
  - `GET /api/health`
  - `GET /api/clans`
  - `GET /api/public/availability`
- Current Java API client pattern:
  - Java 11 `HttpClient`
  - 8 second timeout
  - `Accept: application/json`
  - `User-Agent: ClanWarBoard-RuneLite/1.0`
  - `X-Clan-War-Board-Client: runelite`
- Live Java smoke test pattern used successfully:
  - instantiate `ClanWarBoardApiClient`
  - call `fetchStatus(DEFAULT_SERVICE_URL)`
  - require `online=true`; do **not** require a positive clan count because the correct plugin-only state can be zero registered clans until real clans use the plugin.

## Website/source rules

- Clan data source: **Clan War Board plugin registrations/telemetry only**. Do not use Wise Old Man, TempleOSRS, or other public directories to populate/promote clans on the public site; those sources are only optional enrichment after a plugin clan exists.
- OSRS imagery/theme source: OSRS Wiki MediaWiki API pageimages for pages such as Wilderness, Clan Wars, Revenant Caves.
- Public fights/results must stay empty until real plugin submissions/telemetry exist.
- Clan detail pages should be fight-history-first: member count, wins/losses/draws, kills/deaths, returns, damage dealt/taken, upcoming challenges, past battles, and public/private member stat filtering.
- Direct challenge system should support: open challenge, direct challenge, counter offer, accept terms.
- Match terms belong at the bottom of the home page, not as a separate nav tab.
- Separate website pages should be clean routes for: `/`, `/clans`, `/fights`, `/leaderboard`, `/results`.

## Winner/leaderboard model

- Leaderboard should exist as its own tab/page.
- Clan ratings remain `unrated` until completed Clan War Board fights exist.
- Only completed, non-disputed fights with enough confidence should count toward rating.
- Winner signals to surface:
  - kills
  - deaths
  - returns
  - duration/location control
  - damage pressure
  - third-party interference adjustment
- Outcomes: win, loss, draw, disputed, no contest.
- The winner system must be tied to accepted match terms: both leaders accept the same terms hash; changing terms requires reconfirmation.

## Visual/theme preferences

- The public site should feel like an OSRS clan adversary site, not a generic SaaS page.
- Preferred direction: darker burned Wilderness forest + stone castle theme.
- Use charcoal/burned forest backgrounds, stone-like card borders, ember red accents, ash-gold highlights.
- After darkening the theme, visually check contrast: page headings can become too dark on the background; make external page headings light with text shadow while keeping card titles dark.

## Deployment/site routing gotchas

- Azure Static Web Apps clean routes (`/clans`, `/leaderboard`, etc.) need `navigationFallback` in `staticwebapp.config.json`.
- For this repo’s deploy shape, `staticwebapp.config.json` must be included under the deployed `web/` app root as well as any repo-root copy; otherwise direct routes can 404 after deployment.
- Verify direct routes with curl status checks after deployment, not just client-side navigation.

## Verification checklist

1. Service tests: `python3 -m unittest discover -s tests -v`.
2. Plugin build: `JAVA_HOME=/opt/data/jdks/current-java11 ./gradlew clean test assemble --no-daemon --console=plain`.
3. Live API checks for `/api/health`, `/api/clans`, `/api/leaderboard`, `/api/challenge-system`, `/api/judging-system`.
4. Live direct route checks for `/`, `/clans`, `/fights`, `/leaderboard`, `/results`.
5. Browser visual check for OSRS theme, route-specific content, contrast, and no development-copy leakage.
