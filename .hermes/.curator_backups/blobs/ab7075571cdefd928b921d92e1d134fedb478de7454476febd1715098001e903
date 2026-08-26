# BIS Loadouts item-data, gear logic, and sidebar lessons

Use when working on `/opt/data/HeRmEz/projects/osrs-plugins/pr-review-pending/BisLoadouts` (formerly BossReadinessScore). The GitHub repo is `ItMeansBigMountain/bis-loadouts-osrs`.

## Data-source stance

Do **not** scrap GearScape just because a few recommendations are stale/noisy. The user says the plugin is mostly accurate because GearScape has practical live equipment/weapon/boss combat stats that older BiS-style sources do not keep current.

Preferred runtime source stack:

1. **GearScape** monster/equipment/weapon endpoints for machine-readable combat stats, `two_handed`, subcategory, and ranged `ammunition` compatibility IDs.
2. **OSRS Wiki** as the always-updated canonical item/name/main-game source. Use wiki mapping/category/page data as reliability and freshness validation around GearScape, not as a replacement for combat-stat shape.
3. **Local curated fallback items/ammo** for current main-game gear that live APIs may lag on or omit.

Before changing filters or item logic, run a quick research scan against OSRS Wiki mapping + GearScape equipment/weapon data and inspect actual names/ids that would pass. Do not implement filters from memory.

## Main-game vs excluded items

The user wants **main-game** recommendations. Exclude seasonal/PvP-mode-only rows that leak from GearScape, including patterns found in research scans:

- `(dmm)`, `deadman`, `deadman's`
- `(bh)`, `bounty hunter`
- `vesta's`, `statius's`, `morrigan's`, `zuriel's`
- `fractured archive`, `dogsword`, `thunder khopesh`
- temporary Gauntlet variants: `corrupted`, `attuned`, `perfected`, `(basic)`, etc.
- Leagues/seasonal cosmetics: `leagues`, `trailblazer`, `shattered relics`, `raging echoes`, `relic hunter`, broad `seasonal`/`competitive` terms.

Do **not** block main-game minigame rewards just because they are minigame-sourced. Allowed examples:

- Castle Wars/LMS halos (`saradomin halo`, `zamorak halo`, etc.)
- `swift blade`
- other current main-game rewards if they are real wearable OSRS gear.

Avoid broad substring filters like `gauntlet`: `confliction gauntlets` are real current OSRS gear and should be allowed. Use explicit temporary-item patterns instead.

## Known current item corrections

- `confliction gauntlets` are real current OSRS gear, item id `31106`; they should be recommended over tormented bracelet when offensive magic stats make them stronger. They require 90 Hitpoints in-game, but current `GearItem` requirement modeling may not include HP requirements yet — note this until HP requirements are modeled.
- `aranea boots` are real current OSRS tribrid boots, item id `29806`; no requirements; offensive stats include +5 magic, +6 ranged, +4 melee strength. Add/keep them as local curated fallback if live sources lag.

## Recommendation logic expectations

- Gear recommendations should be **max-DPS / offensive-stat first**, respecting boss style weakness, player stats, budget, weapon compatibility, and main-game filters. Defensive/readiness messaging is secondary.
- Alternatives for each slot must be ordered strongest-to-weakest. The left/default item is the strongest; right arrow moves to weaker alternatives.
- Do not mix 1H and 2H weapons in one cycling list. Maintain separate weapon alternative sets:
  - 2H weapon set
  - 1H weapon set
- Expose those sets through **one compact state-labeled toggle beside the primary `Analyze` action**, not two permanent buttons below the equipment grid. The button text is the active state (`1H` or `2H`); one click switches to the other set. Initialize from the strongest recommended weapon, reset weapon/shield/ammo indices on mode changes, and omit the toggle entirely unless both handedness sets exist so `Analyze` can keep the full row width.
- Preserve the recommendation model while moving the control: this is a UI consolidation, not a new scoring mode. If a 1H weapon is displayed, recommend/cycle a compatible shield/offhand. If a 2H weapon is displayed, suppress/disable shield display but keep shield alternatives internally so they reappear when switching back to 1H.
- Add a focused Swing regression test on the EDT that recursively finds buttons and verifies: exactly one `1H`/`2H` button exists, it shares the same immediate parent row as `Analyze`, its initial label follows the recommended weapon, and one click flips the label/state. This catches both duplicate-control and wrong-row regressions that a build-only test misses.
- Use GearScape `two_handed` boolean when available. Fall back to known-name/subcategory heuristics only when the live boolean is missing.

## Ranged ammo compatibility — critical pitfall

The user explicitly complained when cycling ranged weapons did not update ammo and again when no ammo was recommended. Treat this as a blocking regression.

Authoritative OSRS Wiki ammunition rules:

- bows use arrows
- crossbows use bolts
- ballistae use javelins
- toxic blowpipe uses darts
- salamanders use herb tar
- crystal/self-contained ranged weapons use charges, not conventional ammo

Use GearScape weapon `ammunition` IDs when available and filter the displayed ammo slot to compatible ammo only:

- `twisted bow`, `dark bow`, `venator bow`, `scorching bow` → arrow IDs
- `rune crossbow`, `zaryte crossbow` → bolt IDs
- `toxic blowpipe` → dart IDs
- `bow of faerdhinen`, `crystal bow`, `webweaver bow`, `craw's bow` → self-contained/charge behavior; do not force generic arrows.

Implementation pitfall: do **not** permanently replace/remove the full ammo alternatives list with only the currently selected weapon's compatible ammo. Keep the full ammo pool internally so switching bow → crossbow → blowpipe can recalculate arrows → bolts → darts. Only the displayed/selected ammo should be filtered for the currently displayed weapon.

Also avoid relying only on GearScape live ammo rows. Add local curated ammo fallbacks from OSRS Wiki so recommendations never go blank when live data omits ammo:

- arrows: `dragon arrow`, `amethyst arrow`, `rune arrow`
- bolts: `dragon bolts`, `ruby dragon bolts (e)`, `diamond dragon bolts (e)`, `runite bolts`, `amethyst broad bolts`
- darts: `dragon dart`, `amethyst dart`, `rune dart`

Test requirements for future changes:

- Bow accepts arrows and rejects bolts.
- Crossbow accepts bolts and rejects arrows.
- Blowpipe accepts darts and rejects arrows.
- Self-contained bowfa/crystal-style weapons reject generic arrows.
- Ranged recommendations include arrow, bolt, and dart alternatives in the internal ammo pool so UI cycling can recalculate ammo by weapon type.

## Current boss data and freshness strategy

Boss support has two distinct layers; audit both before concluding that a new boss is unsupported:

1. The checked-in fallback/index list provides offline autocomplete.
2. Runtime refresh merges GearScape's boss index with OSRS Wiki `Category:Bosses`.

A new boss can therefore appear in autocomplete while still receiving generic fallback stats. Do not treat name presence as complete support. For every newly released repeatable boss, verify whether GearScape has a detailed monster ID/profile; when it does not, add a curated OSRS Wiki-backed local `BossTarget` containing combat level, HP, base combat stats, style defences, attributes, release date, and Wiki URL. Keep resolution priority as **live GearScape detail → curated local Wiki profile → generic fallback** so a curated snapshot never overrides a newer machine-readable profile.

Research rules:

- Start from the OSRS Wiki boss index/category, then inspect each post-boundary boss page individually.
- Include released, repeatable encounters; exclude unreleased proposals, quest-only forms, and League-only encounters.
- Model distinct repeatable forms separately when they have materially different stats, e.g. Brutus vs Demonic Brutus and quest vs post-quest Mad Angel.
- For paired encounters, support the encounter search term plus individual combatants where users may search either, e.g. `Royal Titans`, `Branda the Fire Queen`, and `Eldric the Ice King`.
- Prefer the repeatable post-quest form for a repeatable boss. Raw Wiki template/switch data may be necessary when the rendered summary exposes only the quest form.
- Preserve unusual mechanics in attributes/source notes instead of inventing numeric stats. Example: Gemstone Crab has effectively infinite HP; use its documented 300 effective HP for ruby bolts for the numeric display and explicitly label the infinite-HP mechanic.
- Avoid `Integer.MAX_VALUE` or other sentinel values in displayed boss fields even when they do not affect scoring; sidebar metadata must remain readable.

As of the 29 July 2026 content boundary, the post-Araxxor curated set is: Amoxliatl, The Hueycoatl, Royal Titans, Branda the Fire Queen, Eldric the Ice King, Yama, Doom of Mokhaiotl, Gemstone Crab, Brutus, Demonic Brutus, Maggot King, and Mad Angel. Treat this as a dated research checkpoint, not a permanent complete roster; re-run the Wiki comparison whenever the user asks for newest bosses.

Test the data layer before networking: instantiate `BossDataService`, assert every newly researched boss is present in offline suggestions, and verify representative raw fields/source labels for at least a high-level boss, a mechanically unusual boss, and the newest boss. This catches the common regression where the live Wiki category masks a stale fallback list or generic profile.

## Boss weakness / defence display

The user wants selected boss defenses shown below the gear icon grid **in order from weakest to strongest**, but not as a dense one-line stat dump. OSRS players understand this better as an attack-style guide: low defence means the boss is weak to that style; high defence means avoid that style.

Preferred format is a light, larger, vertical bullet block that can use sidebar height freely:

```text
Boss attack style guide
• Weakest / best: Ranged def 45
• Good: Stab def 75
• Okay: Slash def 150
• Strong: Crush def 150
• Strongest / avoid: Magic def 150
```

Avoid paragraph-looking text under the gear grid. If all defenses are zero/missing from the source, show a single bullet such as `• Unknown from this data source`.

## Rename / repo cleanup checklist

When renaming an OSRS plugin project, update every layer together and verify each one:

1. Child repo internals: Gradle `rootProject.name`, `runelite-plugin.properties`, `plugin.json`, README/docs, Java package path, plugin/config/panel/test class names, config group, resource paths/icons, and user-agent/support URLs.
2. Build verification: run `./gradlew clean test assemble --no-daemon --console=plain` from the renamed child repo before pushing.
3. GitHub repo: rename the GitHub remote via API/gh, update local `origin`, push/verify local SHA equals `git ls-remote` on the new repo URL.
4. Parent HeRmEz submodule: rename the submodule path with `git mv`, update `.gitmodules` section name/path/url, run `git submodule absorbgitdirs <path>` if the moved worktree still has a real `.git/` directory, then `git submodule init/sync <path>` and verify `git submodule status <path>` has no leading `-`.
5. Parent docs: update OSRS cleanup plans / portfolio correlation docs, stage only exact OSRS paths, then commit/push parent.
6. Windows handoff after a submodule rename: tell the user to run `git pull`, `git submodule sync --recursive`, `git submodule update --init --recursive <new-path>`, then delete the stale old folder locally if it remains.

For GitHub cleanup of unused OSRS plugin repos, first compare current local active plugin directories + `.gitmodules` against GitHub OSRS/RuneLite repos. Present exact keep/delete lists and get explicit confirmation before destructive `DELETE /repos/{owner}/{repo}` calls. After deletion, verify each deleted repo returns 404 and re-scan remaining repos.

## UI preference

For BIS Loadouts, center the panel controls and status text inside RuneLite's narrow sidebar: boss selector, style buttons, Analyze button, headings, summary lines, muted notes, and equipment grid.

For explanatory text under gear recommendations, make it lighter/brighter than the previous muted gray, slightly bigger, and multi-line/bulleted. The user is comfortable using more vertical space; prioritize legibility over compactness.

Alignment lesson from screenshot review: text above the recommendation icons should align from the same left edge as the icon grid begins. For text below the recommendation icons, the user preferred the smaller-text version's alignment but the larger font size. Preserve the grid-aligned left edge/section width and increase only the font/line height. Section the below-grid text consistently using the same font/alignment for `Gear controls`, `Boss attack style guide`, and `DPS per style` (renamed from `Other styles`).

Boss search UX: do not use `None` as visible placeholder/search text or as a dropdown option because it interferes with searching. A blank boss search field means “no boss selected / best gear by stats”; if old UI state sends `None`, treat it as blank internally.

Keep explanatory text concise; the gear grid should answer: “what is the strongest legal main-game gear for my stats/budget against this boss?”