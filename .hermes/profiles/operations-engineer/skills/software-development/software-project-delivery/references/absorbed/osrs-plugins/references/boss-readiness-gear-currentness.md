# BossReadinessScore gear currentness + 2H handling

Use this when maintaining the BossReadinessScore recommendation engine or any OSRS equipment recommendation UI.

## Durable lessons from user corrections

- The user expects current main-game OSRS bossing gear, not only whatever a live third-party API returns.
- Treat live API gear as helpful input, not as the source of truth. Merge it with curated OSRS Wiki/RuneLite-ID fallback rows.
- Curated local rows should override same-name live rows when they carry important metadata such as `twoHanded`, canonical names, fallback item IDs, or game-mode filtering.
- Do not recommend items that only exist for temporary/game-mode/minigame contexts.
- Two-handed weapons must be visible as weapon alternatives and must suppress/disable the shield slot when selected, including when the user cycles to a 2H alternative.

## Main-game-only filters

Filter before items enter recommendations, both for parsed live API items and local fallback rows. Exclude temporary/minigame/game-mode gear patterns such as:

- Corrupted Gauntlet temporary gear: `corrupted`, `attuned`, `perfected`, `(basic)`, `(attuned)`, `(perfected)`, `basic bow/staff/halberd`.
- Deadman / Deadman Mode items.
- Leagues items: `league`, `trailblazer`, `twisted league`, `shattered relics`, `raging echoes`, `relic hunter`.
- Seasonal/competitive/trophy items.

Avoid over-filtering normal main-game names: e.g. `crystal bow` and `bow of faerdhinen` are valid main-game items; `corrupted bow (perfected)` is not.

## Current OSRS fallback candidates to keep covered

Keep high-impact OSRS Wiki-backed fallback rows and item IDs for modern bossing gear, especially where external APIs may be stale:

- `tumeken's shadow` — item ID 27275 — 2H magic megarares weapon.
- `twisted bow` — item ID 20997 — 2H ranged megarares weapon.
- `scythe of vitur` — item ID 22325 — 2H melee megarares weapon.
- `bow of faerdhinen` — item ID 25862 — 2H bow.
- `toxic blowpipe` — item ID 12926 — 2H ranged weapon.
- `scorching bow` — item ID 29591 — 2H demonbane bow from While Guthix Sleeps.
- `zaryte crossbow` — item ID 26374 — one-handed crossbow; should not suppress shield.
- `purging staff` — item ID 29594 — one-handed magic demonbane staff; should not suppress shield.
- `emberlight` — item ID 29589 — one-handed demonbane sword.
- `soulreaper axe` — item ID 28338 — 2H axe.
- `noxious halberd` — item ID 29796 — 2H halberd.
- `eye of ayak` — current OSRS powered staff from Doom of Mokhaiotl; page is on Old School RuneScape Wiki.
- `dizana's quiver` — item ID 28951 — current ranged ammo/cape-slot style upgrade.

## 2H recognition patterns

Do not only hard-code megarares. Future-proof with name patterns while guarding one-handed exceptions:

- 2H-ish patterns: `twisted bow`, `bow of faerdhinen`, `scorching bow`, any normal bow that is not a crossbow, `toxic blowpipe`, `tumeken's shadow`, `scythe`, `halberd`, `soulreaper axe`, `godsword`, `maul`, `greataxe`, `2h sword`, `colossal blade`, `barrelchest anchor`, `spear`.
- Explicit non-2H checks/tests: crossbows such as `zaryte crossbow`; one-handed magic weapons such as `purging staff`.

## Regression tests to add/maintain

- Fallback item IDs are case-insensitive for all current curated items.
- 2H weapons suppress the shield slot in the generated recommendation.
- Cycling to a 2H weapon alternative updates the shield slot to disabled/blank/`2H weapon` in the UI.
- Game-mode/minigame items are filtered and normal main-game items are not over-filtered.
- Generated wiki links start with `https://oldschool.runescape.wiki/w/` and never use RuneScape 3 domains.
