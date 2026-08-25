# Clan War Board rank-gated planning pattern

Use for `/opt/data/HeRmEz/projects/osrs-plugins/in-progress/CompetitionOverlay`, now pivoted from generic `Competition Overlay` to **Clan War Board**.

## Product direction

Keep the concept simple and Plugin Hub-safe:

- The plugin helps OSRS clans set up/manage fights with other clans.
- It is not an enemy tracker, scout bot, or automated winner detector.
- It should detect whether the local player has a high enough rank in their current clan.
- High-rank players see a leader setup view; regular members see a read-only rally/member view.

Current display name/mission:

```text
Clan War Board — lets clan leaders set up wilderness fights while members see the current war board.
```

## Rank-gating implementation notes

RuneLite API surface confirmed in `runelite-api 1.12.32`:

```java
Client#getClanChannel()
ClanChannel#getName()
ClanChannel#findMember(String)
ClanChannelMember#getRank()
ClanRank#getRank()
```

Known rank values from `ClanRank`:

```text
OWNER = 126
DEPUTY_OWNER = 125
ADMINISTRATOR = 100
GUEST = -1
```

Pattern:

1. Get local player name from `Client#getLocalPlayer().getName()`.
2. Get current clan via `Client#getClanChannel()`.
3. Find the local player in that clan via `clan.findMember(playerName)`.
4. Compare `member.getRank().getRank()` against configured minimum leader rank.
5. If rank is high enough, render leader setup mode; otherwise render member view.

Default threshold should be Administrator or higher unless user changes it.

## UI expectations

Leader view should show/edit war planning details through config-backed fields:

- war name
- opponent clan
- date/time
- world
- hotspot/rally zone
- rules/notes

Member view should be read-only and focused on rally information:

- upcoming fight
- opponent
- when
- world
- hotspot/rally zone
- rules/notes

Keep wording clear that leaders configure fights and members consume the rally board.

## Future work boundaries

Good next features:

- saved war sessions
- hotspot presets for common multi wilderness locations
- start/stop local presence tracking
- post-war attendance/time-in-zone summaries
- copy-to-clipboard war plan
- optional tiny overlay with world/hotspot/time

Avoid in v1:

- global enemy tracking
- scouting across worlds
- automatic Discord/backend sync
- claims of official winner detection
- polling large player/clan datasets aggressively

Frame as event organization + local war board, not PvP intelligence automation.

## Validation

Use Java 11 and run from the plugin repo:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon --console=plain
```

For Windows handoff:

```bat
cd C:\Users\faree\Desktop\HeRmEz\projects\osrs-plugins\in-progress\CompetitionOverlay
gradlew.bat run --no-daemon --console=plain
```
