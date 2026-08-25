# Clan War Board PvP-world venue validation

Use when allowing arranged wars outside the Wilderness on dedicated PvP worlds, including world 392.

## World selection is dynamic

- World 392 is normally the always-active Australian members PvP world, but never make the number itself authoritative.
- Read `Client.getWorldList()`, find the selected `World.getId()`, and require `world.getTypes().contains(WorldType.PVP)` at selector-open, terms submission/acceptance, existing-fight display after updates, and login/world-hop.
- Presence in the live list means presently available; absence may be temporary or mean a rotating world is inactive. Preserve saved terms but mark the world unavailable rather than silently replacing it.
- Require `PVP` directly. RuneLite `WorldType.isPvpWorld(...)` also treats `DEADMAN` as PvP, so it is too broad for a normal PvP-world selector unless followed by an explicit exclusion.
- Treat `HIGH_RISK`, `MEMBERS`, and F2P/member compatibility as separate validation and warning dimensions.
- If the world list has not loaded, return an indeterminate/retry state rather than falsely rejecting the number. Once logged in, verify the actual current world via `client.getWorldType().contains(WorldType.PVP)`.
- Weekly world rotations and exceptional deployment/holiday periods make hardcoded active-world lists stale. UI may feature 392 as a convenience, but live RuneLite types govern validity.

## Mechanics relevant to terms

- Outside safe zones, ordinary PvP-world attack range is ±15 combat levels.
- In the Wilderness on a PvP world, effective attack range is `15 + wildernessLevel`; death/teleport mechanics still use the actual Wilderness level.
- Safe zones include most banks and respawn points, Grand Exchange, Ferox Enclave, and later protected subareas. A fight may briefly continue into safety after retaliation, so a boundary-adjacent named location is not sufficient validation.
- Multi status and PvP danger are independent. The crossed-swords multi indicator does not prove the tile is dangerous PvP, and a generally dangerous region may contain safe banks or minigame/private contexts.

## Venue model

Keep modes explicit:

- `WILDERNESS`: PvP works on every ordinary world; themed Wilderness-PK worlds add no special mechanics. Validate exact Wilderness multi geometry, plane, safe enclaves, singles-plus exceptions, and Wilderness level.
- `PVP_WORLD`: require a live `PVP` world and validate exact non-Wilderness tiles against both multi geometry and dangerous-PvP eligibility.

A PvP-world venue is the intersection:

`verified multi tiles ∩ dangerous open-world PvP tiles ∩ reachable content − safe/minigame/private exceptions`.

Store venue id/name, rectangle-union or tile geometry, plane, mode, membership requirement, safe-zone exclusions, and source revision. Validate the intended fighting footprint or clearance-eroded center, not merely a city/region name.

## Documented multi-area candidate universe

The OSRS Wiki says “Some multicombat areas include,” so this is not an exhaustive coordinate specification. Non-Wilderness entries include: most oceans; Abyss; Al Kharid Palace; Ape Atoll; Kharidian Desert Bandit Camp; Barbarian Village; battlefield south of West Ardougne; Draynor jail; most of Falador/White Knights’ Castle; Mole Hole; God Wars Dungeon; Hosidius cow pen; Jatizso and Neitiznot ice-troll areas; Jormungand’s Prison; Kalphite Lair; western Kharazi Jungle; Lighthouse Dungeon; Piscatoris Fishing Colony; Ranging Guild; northern Fremennik coast; first Stronghold of Security level; Mor Ul Rek; Varrock Sewers; Waterbirth Island Dungeon; White Wolf Mountain; inner Kraken Cove; Wizards’ Tower; and Woodcutting Guild.

Do not automatically offer multi minigame/private entries such as Barbarian Assault, Castle Wars, Fight Pits, Emir’s Arena, Pest Control, or POH fight arenas. Boats are non-attackable; Theatre of Blood is inaccessible on PvP worlds; Ancient Guthixian Temple is an NPC pseudo-multi exception that the game considers single-way. Explicit safe subareas, such as Ape Atoll bank, remain excluded even inside a broad multi region.

## Primary references

- PvP mechanics, safe areas, rotation: https://oldschool.runescape.wiki/w/PvP_world
- Current world roster/rotation: https://oldschool.runescape.wiki/w/World
- Documented multi areas: https://oldschool.runescape.wiki/w/Multicombat_area
- Wilderness level stacking: https://oldschool.runescape.wiki/w/Wilderness
- RuneLite world types: https://static.runelite.net/runelite-api/apidocs/net/runelite/api/WorldType.html
- RuneLite world fields: https://static.runelite.net/runelite-api/apidocs/net/runelite/api/World.html
- RuneLite client world list: https://github.com/runelite/runelite/blob/master/runelite-api/src/main/java/net/runelite/api/Client.java
