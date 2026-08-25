# GearScape-inspired BiS / best-available setup research

Use this when the user asks for automatic best-in-slot or best-available OSRS boss gear recommendations inside RuneLite.

## Session learning

GearScape's Best Setup feature is not a simple public `best setup` API. The web app is Nuxt/Vue and does most setup ranking in client-side web workers. Use GearScape as algorithm/UX inspiration unless the maintainer publishes stable third-party API terms.

Observed public-ish GearScape data endpoints during research:

- `https://api.gearscape.net/api/monster`
- `https://api.gearscape.net/api/spell`
- `https://api.gearscape.net/api/equipment/all`
- `https://api.gearscape.net/api/weapon/all`
- `https://api.gearscape.net/api/equipment/ammunition`
- `https://api.gearscape.net/api/equipment/alias`
- `https://api.gearscape.net/api/prayer/overview`
- `https://api.gearscape.net/api/potion/overview`
- `https://api.gearscape.net/api/trailblazer/regions/all`
- item lookup example: `https://api.gearscape.net/api/item/id/24187`

Observed worker assets:

- Best setup worker: `https://gearscape.net/_nuxt/776157e.worker.js`
- Overkill worker: `https://gearscape.net/_nuxt/b1f90fe.worker.js`
- Other worker: `https://gearscape.net/_nuxt/56ab90e.worker.js`

## How GearScape's setup flow works

1. Load monster, item/equipment/weapon/ammunition, spell, prayer, potion, alias, and league/region data.
2. Collect player stats: Attack, Strength, Defence, Hitpoints, Magic, Ranged, Prayer, Mining.
3. Collect target details: monster/variant, defence reductions, wilderness/task/aoe flags, distance filters, special mechanics.
4. Collect constraints: budget, item cap/risk ammo, include/exclude/include-only items, locked slots, owned/custom items, potions, prayers, ranking mode, search depth, secondary-fill mode.
5. Spawn the best-setup worker once per style: stab, slash, crush, ranged, magic, sometimes atlatl.
6. Worker returns a result per style; UI sorts by `compareMetric` and auto-selects the best style/setup.

Observed worker payload keys include:

```text
style, monster, allStyleWeaponsUnfiltered, allStyleWeapons, styleWeaponCounts,
allStyleEquipment, allEquipment, allAmmunition, ammunitionList, equipmentSlots,
equipmentSets, equipmentLocks, extra, aoe, tasked, wilderness, specials,
experienceSettings, experiencePreference, include, exclude, includeOnly,
includeOnlySpells, initialBudget, riskAmmunitionCount, expensiveItemCap,
stats, effectiveAttack, effectiveStrength, potions, prayers, intensifyPrayers,
airPactPrayers, allSpells, trailblazerRegions, trailblazerRegionData,
bestMode, equipmentSecondaryFill, searchDepth, forceOnehanded
```

Observed worker result keys:

```text
dps, maxHit, averageDamage, hitChance, compareMetric, effectiveStyle,
boostKey, prayerKey, warning, equipment
```

## Example observed behavior

For `Zulrah (Serpentine)` with 99 stats, large budget, DPS mode, search depth 1, GearScape ranked magic first in the observed run:

- DPS around 10.864, max hit 42, hit chance around 93%
- gear included eye of ayak, occult necklace, elidinis' ward (f), imbued god cape, ancestral robes, confliction gauntlets, avernic treads (max), magus ring
- ranged/Twisted bow setup was second around 7.918 DPS
- melee slash/stab setups followed
- crush returned a no-weapon/distance warning

The key insight is that it is not a static BiS table: it ranks candidate gear against player stats, target defensive stats/mechanics, style, distance, and constraints.

## Live API integration update

OSRS Wiki MediaWiki API page/search calls do not require an API key. Use a descriptive User-Agent. The standard `api.php?action=opensearch` endpoint is good for canonical boss/item page URLs, while GearScape's public endpoints provide more convenient machine-readable monster/equipment stats:

- `https://oldschool.runescape.wiki/api.php?action=opensearch&format=json&limit=1&namespace=0&search=<name>`
- `https://api.gearscape.net/api/monster` returns the current monster index with `boss` flags.
- `https://api.gearscape.net/api/monster/id/<npc_id>` returns detailed monster stats/defences.
- `https://api.gearscape.net/api/equipment/all` and `https://api.gearscape.net/api/weapon/all` return item stat/requirement/price records.

A practical no-manual-update pattern is: keep local fallback presets for offline safety, refresh GearScape boss/item data in a background executor at plugin startup, resolve the user's free-text boss name against the live boss index, then attach an OSRS Wiki URL via `opensearch`. Do not block the RuneLite game/client thread on network calls.

## Recommended RuneLite implementation pattern

Do not clone the full calculator initially. Build a fast in-client MVP:

1. Use local RuneLite client stats for the player.
2. Use OSRS Wiki-derived checked-in/generated data for item stats, item requirements, prices, boss/monster stats, and mechanics. RuneLite item data can supply names/icons/IDs and local ownership where available.
3. Inputs: boss target, combat style or Auto, budget tier, owned-only/excluded items, potion/prayer/task/wilderness/spec assumptions.
4. Filter gear by requirements, style relevance, budget/owned status, locks/exclusions, two-handed conflicts, and ammo compatibility.
5. Generate candidates with bounded search:
   - top N legal weapons for selected style
   - greedy/beam-search slot filling by marginal DPS contribution
   - keep top K partial setups per slot
   - default search depth 1-2 for RuneLite responsiveness
6. Score with a DPS-ish metric: effective attack roll vs target defence, max-hit estimate, weapon speed, target weakness/resistance, style bonuses, known multipliers.
7. Output: best available setup for current stats first, theoretical BiS as optional comparison, alternative styles, upgrade deltas, and reasons items were skipped.

## UX guidance

For Boss Readiness Score or similar plugins, keep this simpler than GearScape:

- Boss dropdown
- Style dropdown with Auto
- Budget/owned-only controls
- Assumption chips: potion, prayer, Slayer task, wilderness, spec reductions
- Readiness score
- Slot-by-slot recommended gear with icons
- Upgrade-next list
- Warnings/missing requirements
- Beginner mode by default; advanced mode reveals DPS/hit chance/max hit/search assumptions

Tooltips should explain why an item was selected/skipped: missing level, over budget, excluded, wrong style, ammo mismatch, two-handed conflict, unavailable, or lower DPS.
