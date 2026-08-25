# Clan War Board PvP telemetry research notes

Use when extending Clan War Board from scheduling/website into real PvP telemetry and clan/player performance tracking.

## Public repos reviewed

- `Matsyir/pvp-performance-tracker` — BSD-2-Clause RuneLite plugin. Strongest source for deep 1v1 PvP analytics patterns.
- `LogicalSoIutions/osrs-pvp-performance-tracker-website` — Next.js/PostgreSQL PvP-Hub website for uploaded fight analysis/merge patterns.
- `findarian/pvp-leaderboard` — BSD-2-Clause RuneLite plugin. Strongest source for leaderboard/MMR, match submission, multi-opponent fight state, and cached ranking shard patterns.
- RuneLite Plugin Hub manifests disclose third-party server warnings for PvP Leaderboard and PvP-Hub-style uploads.

Do not depend on private APIs or copy large code sections. The durable value is the strategy: event sources, state model, privacy pattern, and aggregation architecture. If code is reused directly, preserve BSD license/copyright notices.

## Useful OSRS/RuneLite data sources

- Wise Old Man: public groups, members, account/build metadata; good for clan roster enrichment, not live PvP telemetry.
- TempleOSRS: player progress/history enrichment; not live PvP telemetry.
- Official OSRS hiscores: current totals, LMS/PvP Arena/BH where available; snapshot diffs needed for gains.
- OSRS Wiki APIs: item/location/media/theme assets and item metadata.
- RuneLite client events/API: primary live telemetry source.

## PvP Performance Tracker lessons

Good for detailed fight analytics:

- Uses `InteractingChanged`, `AnimationChanged`, `HitsplatApplied`, `StatChanged`, `FakeXpDrop`, `PlayerDespawned`, `GameTick`, `GameStateChanged`.
- Tracks attack count, successful off-pray attacks, expected damage, actual damage, magic hits, ghost barrage count, HP healed, robe hits, deaths, combat levels, fight logs, inventory snapshots, gear snapshots, overhead/offensive prayers, and special weapon handling.
- PvP-Hub upload is opt-in, warns about third-party server/IP/RSN, supports delayed public visibility, hidden RSN, and synced/unsynced fight display.
- Website merges opposing POVs by fight ID, attacker/opponent names, tick/time offsets, attack logs, style/prayer success, gear/ammo, and hidden-name handling.

For Clan War Board: use fight logs and POV merge concepts, but do not start with expected-damage/KO-chance complexity. Those are phase 2/3.

## PvP Leaderboard lessons

Good for clan-war MVP architecture:

- Maintains `activeFights` keyed by opponent for simultaneous/multi fights.
- Uses `HitsplatApplied`, `ActorDeath`, `GameTick`, multi-combat varbit, idle cleanup, per-opponent suppression, inbound PvP damage cache, and death finalization.
- Tracks per-opponent damage dealt/received and `wasInMulti`.
- Uses TrueSkill/MMR-style ratings, match buckets, match history, WebSocket matchmaking/lobbies, cached rank shards, and static leaderboard/rank histogram artifacts.
- Uses client install identity headers and caching/backoff to avoid hammering APIs.

For Clan War Board: adopt event-driven multi-opponent state and static leaderboard snapshots. Do not use plugin-embedded shared secrets as a strong security boundary; Java clients can be decompiled.

## Current implemented telemetry slice

- Plugin has required online sync and no disable toggle.
- Member setting `Show My Player Stats Publicly` defaults to `false`; telemetry still syncs for clan scoring, but public website player names should remain private unless opted in.
- World is intentionally public for Wilderness revival; backend policy exposes `worldIsPublic: true`.
- Plugin currently batches local-player events rather than scanning/uploading every visible player:
  - event types: `heartbeat`, `damage_dealt`, `damage_taken`, `death`, `kill_candidate`;
  - `MAX_EVENTS_PER_BATCH = 50`;
  - minimum flush interval `10s`;
  - heartbeat interval `100` game ticks;
  - death/kill candidate flushes immediately.
- Live endpoint shape: `POST /api/plugin/events/batch` returns accepted/rejected counts and policy. Current deployed implementation validates/acks batches; Cosmos persistence/materialized scoring is the next slice.
- Important performance rule: never create “200 visible players × every client × constant API calls.” Track local-player events, queue them, and upload small batches.

## Recommended Clan War Board telemetry MVP

Plugin classes to add/shape:

- `ClanWarTelemetryTracker`
- `FightEvent`
- `FightEventBatch`
- `TrackedOpponent`
- `ParticipantHeartbeat`

Start with event sources:

- `HitsplatApplied` — damage dealt/taken, third-party damage candidates.
- `ActorDeath` or `PlayerDespawned` — death/kill candidates, with delayed finalization for double deaths/cleanup.
- `GameTick` — heartbeats, location-control samples, idle cleanup, batched upload cadence.
- `InteractingChanged` — target/opponent hints.
- `GameStateChanged` — reset/flush on login/logout/world hop.
- `Client.getVarbitValue(Varbits.MULTICOMBAT_AREA)` — multi-combat flag.
- Clan channel APIs — player/clan/rank attribution.

Telemetry event shape should include:

```json
{
  "fight_id": "...",
  "terms_hash": "...",
  "event_id": "...",
  "event_type": "damage|death|heartbeat|return|location_sample|third_party_damage",
  "source_player": "...",
  "source_clan_id": "...",
  "target_player": "...",
  "target_clan_id": "...",
  "amount": 31,
  "world": 330,
  "region_id": 12345,
  "tick": 123456,
  "timestamp": "...",
  "was_in_multi": true,
  "client_install_id": "..."
}
```

## Backend/API MVP

Add endpoints:

- `POST /api/plugin/events/batch`
- `POST /api/plugin/fights/{fightId}/complete`
- `GET /api/plugin/fights/{fightId}/live`

Store/aggregate:

- `fight_events`
- `fight_participants`
- `fight_summaries`
- `player_fight_stats`
- `clan_fight_stats`

Backend computes kills, deaths, returns, attendance, control time, damage pressure, third-party interference, winner confidence, and leaderboard eligibility.

## Winner and leaderboard policy

Only affect public leaderboard when:

- both leaders accepted the same terms hash;
- fight is completed;
- result is non-disputed;
- confidence exceeds threshold;
- telemetry coverage is sufficient for both clans.

Score signals:

- kills;
- deaths;
- returns;
- duration/location control;
- damage pressure;
- third-party interference adjustment;
- participant coverage confidence.

Use TrueSkill/MMR-style ratings by bucket: overall, pure, zerker, main, multi, DMM/seasonal, and matched-size bracket.

## Free/near-free scaling pattern

For website/read-heavy traffic, generate static snapshots rather than querying Cosmos per request:

- `/snapshots/leaderboard-overall.json`
- `/snapshots/leaderboard-pure.json`
- `/snapshots/clans/{id}.json`
- `/snapshots/fights/recent.json`

Serve snapshots from Static Web Apps/CDN. Plugin/API writes use authenticated/batched endpoints with idempotency keys and rate limits.

## Privacy and anti-abuse

- Upcoming exact world/location/rally details stay private until both leaders accept.
- Public results can be delayed after fight completion.
- Public member stats should be leader-configurable or confidence-gated.
- Treat all plugin submissions as untrusted; use server-side dedupe, idempotency, rate limits, anomaly detection, terms hashes, and multi-client corroboration.
- Do not claim RuneLite traffic can be perfectly proven.
