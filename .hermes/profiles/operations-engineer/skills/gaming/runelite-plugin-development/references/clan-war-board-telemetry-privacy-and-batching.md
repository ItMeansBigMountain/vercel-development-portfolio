# Clan War Board telemetry privacy and batching

Use this when continuing Clan War Board RuneLite plugin/service work after the PvP tracking research and first telemetry slice.

## Durable product decisions

- Online board sync is required for Clan War Board; do not reintroduce an `Enable Online Sync` option. Basic registration for clan identity and leader authorization is part of board sync and must be clearly disclosed.
- **Do not conflate required board sync with combat telemetry consent.** War telemetry sends substantially broader data (opponent names, event types, damage, world/tick/time, evidence/confidence, and region/tile/plane) and must have a separate explicit `Share War Telemetry` control that defaults to `false`.
- When `Share War Telemetry` is off, return from combat/death subscribers before attribution, do not enqueue heartbeat/combat/location events, do not drain or upload batches, and clear buffered telemetry plus combat-attribution state immediately when the option is disabled or identity changes. Recheck the volatile consent state inside already-scheduled upload workers and before failure requeue: a batch drained just before opt-out must be discarded, never transmitted or restored.
- Members separately control whether already-consented player-level performance appears publicly on the website through `Show My Player Stats Publicly`, default `false`. That publication setting must never silently enable telemetry collection.
- Attach an in-client third-party-data warning to the setting that enables transmission, describing the destination and actual payload categories. If the current RuneLite `PluginDescriptor` API has no warning attribute, use the enabling `ConfigItem` name/description and verify the warning is visible before opt-in; README disclosure alone is insufficient.
- Fight worlds may be public for submitted/scheduled fights, but telemetry still requires explicit consent. Private-by-default data includes member/player identity and leader notes/rally details.
- Validate both config states by capturing actual requests and comparing them against documentation and server persistence/publication behavior.

## Anti-lag telemetry pattern

The user explicitly warned that wars may have ~200 visible players per client and API calls can explode exponentially. Do **not** poll or upload every visible player every tick/frame.

Preferred MVP plugin pattern:

1. Track only local-player-observable events first.
2. Queue events locally in memory.
3. Flush small batches on a timer or important terminal events.
4. Never send one HTTP request per visible player, per hitsplat, or per frame.
5. Use backend aggregation/merge to combine multiple clients' points of view.

Current constants from the first implementation:

- Max batch size: `50` events.
- Minimum flush interval: `10s`.
- Heartbeat interval: `100` game ticks.
- Death/kill-candidate events may flush immediately.

Current plugin classes:

- `ClanWarBoardTelemetryEvent`
- `ClanWarBoardTelemetryBuffer`
- `ClanWarBoardApiClient.submitTelemetry(...)`

Current event types:

- `heartbeat`
- `location_sample`
- `damage_dealt` (non-own-clan target during a confirmed fight)
- `friendly_fire_damage` (target found in the local primary-clan roster)
- `damage_taken`
- `third_party_damage`
- `death`
- `kill_candidate`
- `return`

Current service endpoints:

```text
POST /api/plugin/events/batch
GET  /api/plugin/me/metrics
```

Failed client batches are requeued. Server event IDs are deterministic so retries upsert rather than double-count.

Response policy currently includes:

```json
{
  "worldIsPublic": true,
  "playerWebsiteTrackingDefaultsPrivate": true,
  "recommendedClientFlushSeconds": 10,
  "recommendedMaxEventsPerBatch": 50
}
```

## Current persistence and aggregation state

The live service persists accepted telemetry into Cosmos and exposes authenticated private player aggregates through `GET /api/plugin/me/metrics`.

Persistence rules:

- Store only events matched to a confirmed fight's participating clan, accepted world, and scheduled time window.
- Use deterministic event IDs so failed-batch retries upsert instead of double-counting.
- Requeue failed client batches ahead of newer events.
- Key private aggregates by a one-way normalized player/clan hash so totals survive plugin reinstalls without exposing private display names publicly.
- Keep public player identity opt-in; authenticated private metrics remain available to that player.

Pre-submission correctness rules:

- Retain observed opponent/attacker display names because completed-fight analytics provide per-opponent and per-event verbose insights. Escape all names before website DOM insertion.
- Store evidence, confidence, relation, world/tick/time, and region/tile/plane with each accepted event so derived claims remain auditable.
- A `kill_candidate` requires recent local damage to the same normalized target name and remains labeled observed rather than authoritative.
- A `return` is the first confirmed combat observation after the local player's death, counted once per death.
- Incoming damage amount is exact. Include attacker identity only when exactly one nearby player is interacting with the local player; label this source inference separately from amount confidence.
- Classify actors outside the primary clan roster as `non_own_clan`, not definitively as the agreed opposing clan or a third party.
- Publish individual event timelines, cumulative clan/player/opponent metrics, evidence/confidence distributions, and location hotspots only after the agreed fight window ends. Before completion, keep exact rally terms and telemetry private to authenticated participants.
- Players with public tracking disabled use a stable anonymous label in completed public analytics.

## Verification pattern

For plugin work:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon --console=plain
```

For service work:

```bash
python3 -m unittest discover -s tests -v
```

Live endpoint smoke shape:

```bash
curl -i 'https://salmon-dune-01c80c60f.7.azurestaticapps.net/api/plugin/me/metrics'
```

Expected without a plugin session: HTTP `401` with `invalid_session`. Do not create synthetic production installations or fights for smoke tests. Verify authenticated persistence/aggregation with the service regression suite and use consenting real clans for production end-to-end validation.
