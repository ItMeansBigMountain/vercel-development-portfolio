# Clan War Board real-time zero-state and stale-data audit

Use when auditing Clan War Board site/API/plugin output after any data-source, registration, leaderboard, or public-copy change.

## Durable product rule

- Clan War Board public clan listings must be real-time/plugin-owned only.
- Do not populate or promote clans from Wise Old Man, TempleOSRS, or other external directories unless that clan already exists through Clan War Board plugin registration/telemetry and the external source is only enrichment.
- Zero registered plugin clans is a valid production state. Show `0`, not placeholders, fake examples, or sampled external clans.

## Audit checklist

1. Check live API truth, not just local tests:
   - `GET /api/clans` should return `source: Clan War Board plugin` and the actual registered list.
   - If no real plugin registrations exist, `clans` must be `[]` with a clear empty state.
   - `GET /api/leaderboard` should return only plugin-completed fight standings; zero standings is valid.
2. Check rendered website, not just JSON:
   - Homepage counters should show `0 registered plugin clans`, `0 tracked members`, `0 open challenges` when empty.
   - Avoid placeholders such as `— plugin clans` that look like stale/unknown data.
   - Clan page copy should say only clans using the plugin appear; no developer-facing “no fake data” copy except as polished product wording.
3. Check RuneLite plugin panel/client wording:
   - Use `Registered plugin clans`, not `Public clans indexed`.
   - Java API smoke should not require a positive clan count; `registeredPluginClans=0` can be correct.
4. Grep active source and tests for stale fixtures before claiming it is clean:
   - Fake clan names: `Rival Clan`, `Pure Fury`, `Weekend Wilderness War`.
   - Fake fight defaults: `Saturday 8 PM`, `Lava Dragons`, `Multi only`.
   - External-source promotion: `Wise Old Man Groups`, `womScore`, `sourceStanding`.
   - Misleading copy: `clans indexed`, `public members`, `Public clans indexed`, `clans=25`.
5. Remove fake/default fight config values from the plugin. Defaults should be blank/TBD until a real leader sets terms.

## Preferred verification pattern

- Run service tests and Plugin build/tests.
- Curl live `/api/clans` and `/api/leaderboard` after deployment.
- Browser-navigate/visual inspect homepage and `/clans` to verify the user-facing zero state.
- Run a Java client smoke against the live service and verify `registeredPluginClans=0` is accepted when no real clans exist.

## Pitfall from this session

Do not answer from the API alone. In this session the API was already returning `[]`, but the website initial counters and RuneLite panel wording still implied old/stale data. The correct audit spans API, rendered HTML, browser snapshot, plugin panel copy, plugin defaults, and tests.