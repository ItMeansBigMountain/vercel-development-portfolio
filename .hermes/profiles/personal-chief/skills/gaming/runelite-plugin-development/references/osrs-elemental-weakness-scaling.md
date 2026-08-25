# OSRS elemental weakness and magic-scaling implementation

Use this reference when a RuneLite gear/DPS plugin must incorporate elemental weaknesses without treating them as ordinary magic defence or a generic Magic-style multiplier.

## Source and data audit

1. Trace the complete current calculation path before editing: player levels, item attack bonuses, item magic-damage percentages, spell base damage, attack speed, target levels/defence bonuses, accuracy, max hit, DPS, and special multipliers.
2. Identify whether target data is live, curated, or generic fallback. GearScape monster detail currently exposes typed fields `weakness_type` and `weakness`; parse them rather than inferring weakness from names, attributes, negative Magic levels, or thematic appearance.
3. Keep elemental element and percentage as typed target fields. Preserve a backward-compatible constructor/default of `NONE, 0` for existing targets.
4. For curated fallback profiles, verify current values against the OSRS Wiki. Live detail should win when available; curated data should replace only generic/offline fallback.
5. Do not assign one false weakness to multi-target encounters. Model forms separately and add an encounter note where appropriate (for example, Royal Titans: Branda Water 50%, Eldric Fire 50%).

## Standard elemental spell scaling

Only matching standard-spellbook Strike, Bolt, Blast, Wave, and Surge spells receive elemental weakness effects. Powered-staff built-in spells do not.

Tier requirements and initial/base progression:

| Tier | Air | Water | Earth | Fire |
|---|---:|---:|---:|---:|
| Strike req/base | 1/2 | 5/4 | 9/6 | 13/8 |
| Bolt req/base | 17/9 | 23/10 | 29/11 | 35/12 |
| Blast req/base | 41/13 | 47/14 | 53/15 | 59/16 |
| Wave req/base | 62/17 | 65/18 | 70/19 | 75/20 |
| Surge req/base | 81/21 | 85/22 | 90/23 | 95/24 |

For the target element, select the highest tier whose matching spell is unlocked. Within that tier, an unlocked lower-element spell scales to the strongest elemental spell currently unlocked in the same tier. Test boundary levels directly.

For weakness `W` and applicable ordinary magic-damage bonus `G`:

```text
max hit = floor(base × (1 + G/100)) + floor(base × W/100)
```

The weakness portion is based on spell base damage and is additive, not a multiplier over the gear-boosted result.

## Accuracy-roll handling

Weakness boosts the accuracy **roll**, not final hit chance. Do not blindly calculate `hitChance × (1 + W)`.

If an existing estimator supplies only baseline hit chance `p`, convert through the OSRS roll-ratio relationship, multiply the attack-roll ratio, then convert back:

- For `p < 0.5`, implied attack/defence roll ratio is `2p`. Multiply it by the accuracy-roll multiplier. If the result is at most 1, new chance is `ratio/2`; otherwise it is `1 - 1/(2×ratio)`.
- For `p >= 0.5`, new chance is `1 - (1-p)/multiplier`.

This remains an estimate if the surrounding engine lacks raw effective levels, prayers, stances, boosts, defence drains, raid scaling, phase states, Slayer/Salve effects, or encounter caps. Document that boundary clearly.

## Weapon exceptions

Represent hidden effects separately from displayed equipment stats:

- Harmonised nightmare staff: one-handed; standard offensive autocast at 4 ticks; displayed +15% magic damage.
- Smoke battlestaff: 5 ticks; hidden +10% standard-spell accuracy and damage.
- Twinflame staff: one-handed; 6 ticks; hidden +10% standard-spell accuracy/damage; automatically chooses the assigned element when requirements/runes are met; delayed 40% second hit only for Bolt, Blast, and Wave—not Strike or Surge.
- Powered staves: built-in spell does not receive the target's elemental weakness bonus.

Audit hybrid item fields so melee/ranged strength cannot leak into magic-damage summation. Keep style-specific modifiers distinct where the item model supports it.

## Regression tests

At minimum test:

1. Spell unlock/tier boundaries and lower-element scaling.
2. Exact rounding, e.g. base 24, gear 30%, weakness 50% gives `floor(31.2)+floor(12)=43`.
3. Accuracy-roll conversion below and above 50% baseline hit chance.
4. Powered-staff exclusion.
5. Strong weakness can select an eligible standard-spell caster.
6. Minor/no weakness preserves the powered-staff path.
7. Live API weakness parsing and curated fallback values.
8. Opposite-form/multi-target encounter handling.
9. Full Java 11 `clean test assemble` plus official Plugin Hub build after immutable marker update.

## Documentation

README claims must distinguish formula-accurate elemental components from heuristic overall DPS. Link the OSRS Wiki pages for elemental weakness, standard spellbook, and maximum magic hit, plus Jagex Project Rebalance combat changes. State missing runtime inputs rather than presenting the estimator as tick-perfect.
