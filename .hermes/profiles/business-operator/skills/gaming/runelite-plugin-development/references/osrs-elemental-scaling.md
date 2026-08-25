# OSRS elemental weakness and Magic scaling

Use this when a RuneLite PvM recommendation plugin ranks standard elemental spells, powered staves, or bosses with typed elemental weaknesses. Current research baseline: 8 August 2026.

## Authoritative model

Elemental weakness applies only when a standard spellbook Strike/Bolt/Blast/Wave/Surge spell matches the NPC's assigned Air/Water/Earth/Fire weakness. Do not apply it to powered-staff attacks, Ancient/Arceuus/god spells, Iban Blast, Magic Dart, salamanders, or magic special attacks.

For weakness `W`:

```text
weakness accuracy roll = floor(ordinary attack roll × (100 + W) / 100)
weakness damage        = floor(base spell max × W / 100)
final max hit          = max hit before weakness + weakness damage
```

Do not multiply final hit chance or the already gear-boosted max hit. Ordinary magic-damage bonus and weakness damage floor separately.

For normal unboosted/unprayed PvM Magic accuracy:

```text
player attack roll = (visible Magic + 8) × (Magic attack bonus + 64)
NPC defence roll   = (NPC Magic level + 9) × (NPC magic defence bonus + 64)

if A > D: chance = 1 - (D + 2) / (2 × (A + 1))
else:     chance = A / (2 × (D + 1))
```

NPC ordinary Defence level is not part of standard Magic defence. Preserve the raw NPC Magic level in the boss model; do not substitute a transformed readiness/recommended-player level. Use Java `long` for rolls.

## Tier scaling

Within each tier, every castable elemental spell scales to the strongest element unlocked in that tier, but scaling never unlocks the matching spell itself.

| Tier | Required levels / scaled bases |
|---|---|
| Strike | 1/2, 5/4, 9/6, 13/8 |
| Bolt | 17/9, 23/10, 29/11, 35/12 |
| Blast | 41/13, 47/14, 53/15, 59/16 |
| Wave | 62/17, 65/18, 70/19, 75/20 |
| Surge | 81/21, 85/22, 90/23, 95/24 |

Select the highest tier for which the target's matching element is independently castable at the current visible Magic level.

## Equipment exceptions

- Powered staves use built-in attacks and get no elemental-weakness bonus.
- Most standard autocasts are 5 ticks.
- Harmonised nightmare staff autocasts standard offensive spells at 4 ticks.
- Smoke battlestaff/mystic smoke staff add a conditional 10% standard-spell accuracy and damage bonus; model it separately if absent from visible equipment stats.
- Twinflame staff is 6 ticks, adds the hidden 10% bonus, can substitute the assigned weakness element when spell/rune requirements are met, and produces a delayed `floor(first hit × 40 / 100)` second hit only for Bolt/Blast/Wave—not Strike/Surge.
- Chaos gauntlets add 3 to Bolt base max before percentage bonuses and before weakness damage is calculated.
- Elemental tome bonuses are equipment damage modifiers, not weaknesses; use the exact charged item variant and floor separately.
- Manual casting may be possible where autocast is not. If the product assumes sustained autocombat, represent autocast capability explicitly instead of claiming a spell is universally unusable.

## Boss-data model

Keep distinct fields for:

```text
raw NPC Magic level
NPC Magic defence bonus
elemental type and percent
attributes (demon, golem, draconic)
attribute-specific vulnerability
NPC/form/phase mechanics
```

Never infer element from flavour tags, name, negative Magic level, or ordinary Magic defence. Never inherit a boss weakness onto spawned NPCs or alternate forms without source evidence. Examples: Royal Titans require separate Branda Water/Eldric Fire targets; Yama's void flares, Doom larvae, and Amoxliatl unstable ice are separate targets.

Recent verified examples: Amoxliatl Fire 30; Hueycoatl Earth 60 plus draconic; Branda Water 50; Eldric Fire 50; Yama Water 50 plus 120% demonbane vulnerability; Doom none plus demon mechanics; Gemstone Crab none; Brutus/Demonic Brutus Earth 25 (Demonic Brutus is not a demon); Maggot King Fire 80; Mad Angel Earth 15 plus golem.

## GearScape integration

Current monster detail fields use `level_magic`, `level_hp`, `def_magic`, `weakness_type`, and `weakness`. Parse live detail first and use curated profiles only when live GearScape detail is unavailable. Preserve API field names in fixtures; a guessed `magic`/`hitpoints` key silently degrades exact scaling.

## Implementation workflow

1. Audit existing accuracy, max-hit, attack-speed, item-stat, and boss-data paths before editing.
2. Write boundary tests for each spell tier, separate-floor damage vectors, powered-staff exclusion, and attack/defence roll vectors.
3. Add a no-weakness control so weakness logic cannot inflate all Magic gear.
4. Keep exact elemental formulas separate from any surrounding heuristic DPS model, and document missing context such as prayers, boosts, Slayer/Salve, flat armour, raid scaling, defence drains, charges, and phases.
5. Validate live API schema, curated profiles, local fallbacks, and variant/attribute caveats independently.
6. Run Java 11 `clean test assemble`, then advance the immutable Plugin Hub marker only after the child SHA is remotely reachable.
7. In Plugin Hub checks, distinguish an actual `build` failure or `Changes are needed` from the expected aggregate `Requires maintainer review` gate.

## Sources

- https://oldschool.runescape.wiki/w/Elemental_weakness
- https://oldschool.runescape.wiki/w/Maximum_magic_hit
- https://oldschool.runescape.wiki/w/Standard_spellbook
- https://oldschool.runescape.wiki/w/Autocast
- https://oldschool.runescape.wiki/w/Twinflame_staff
- https://secure.runescape.com/m=news/a=13/project-rebalance-combat-changes?oldschool=1
- https://secure.runescape.com/m=news/summer-sweep-up-combat?oldschool=1
- Reference calculator: https://tools.runescape.wiki/osrs-dps/
