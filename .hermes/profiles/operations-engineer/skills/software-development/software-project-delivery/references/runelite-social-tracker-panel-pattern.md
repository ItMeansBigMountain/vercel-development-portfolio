# RuneLite social tracker side-panel pattern

Use this when building an OSRS/RuneLite plugin that tracks players from social sources such as friends list, clan chat, and friends chat.

## Product shape

Prefer a state-driven side panel over hardcoded/sample rows:

- Top-level tabs for the user's requested social views: `Friends Chat`, `Clan Chat`, `Friends List`.
- Each tab filters the same tracked-member state by source tag.
- A rescan/refresh action lives near the tabs.
- Each tracked member row should have an explicit remove/untrack action.
- Removed members should be persisted as ignored names so rescans do not immediately re-add them.

## State boundary

Create a local tracking service before wiring live RuneLite APIs:

- `TrackedMember` with normalized display name, source tags, status, first seen, last seen, last status change, last world, and activity summary.
- `TrackedMemberSource` enum for `FRIEND`, `CLAN`, `FRIENDS_CHAT`.
- `TrackedMemberStatus` enum for `ONLINE`, `OFFLINE`, `UNKNOWN`.
- `SocialTrackerState` immutable-ish snapshot for panel rendering.
- `SocialTrackingService` that owns the map, merges duplicate names across sources, caps max tracked members, serializes ignored members, and exposes snapshots.
- `SocialSourceSnapshot` as the scanner/service boundary so seeded data and real RuneLite source scanners share the same path.

This lets the plugin become useful locally before Wise Old Man/TempleOSRS enrichment exists.

## Config pattern

Useful config items:

- Enable/disable friends list tracking.
- Enable/disable clan tracking.
- Enable/disable friends chat tracking.
- Maximum tracked members for memory/API control.
- Hidden newline-separated ignored-member config string for removed members.

Keep ignored/removed persistence compact. Do not store large event histories in RuneLite config.

## Implementation sequence

1. Capture product direction in a repo-local `PRODUCT_DIRECTION.md`.
2. Add the state model and tracking service with tests for merge/remove/cap behavior.
3. Replace panel hardcoded rows with state-driven rendering.
4. Add top tabs for `Friends Chat`, `Clan Chat`, `Friends List` when the user wants distinct views.
5. Wire plugin startup/login/config-change to rescan and refresh panel state.
6. Keep live RuneLite social API scanners behind the `SocialSourceSnapshot` boundary; use seeded snapshots only as a temporary local-development adapter.
7. Only after local tracking works, add external XP/KC enrichment in background workers.

## Verification

Run Java 11 Gradle checks after each slice:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon --console=plain
```

Then manually smoke-test the side panel in RuneLite with:

```bash
./gradlew run --no-daemon --console=plain
```

Confirm the tabs render, switching tabs filters members, `Rescan` updates state, and `Remove` persists ignored members.

## Pitfalls

- Do not treat passing Gradle tests as proof that RuneLite UI works; side panels need manual client smoke testing.
- Do not leave `All` as the only or default view when the user asked for separate tabs.
- Do not let removed members reappear on the next scan; persist ignored names or the remove button feels broken.
- Do not wire external APIs before local social tracking is stable; API failures should enrich/fail gracefully, not block core tracking.
