# Who's Grinding Panel card legibility polish

Session lesson: when refining the expanded player grinding card, the user evaluates screenshots visually and wants the card to read like a compact stat list, not a paragraph.

## Formatting rules

- Everything in the expanded player card should be line-by-line:
  - section heading on its own line (`Skills:`, `Bosses:`, `Activities:`)
  - every skill XP gain on its own line
  - every boss KC gain on its own line
  - every activity/minigame score on its own line
- Bold the actual gained value plus unit (`+379,085 xp`, `+37 kc`, `+34 score`), not the whole row.
- Use readable card font: roughly 12f for rows and 13f for the `Grinding <period>` heading if the sidebar still fits.
- Keep the left edge tight, but preserve a couple of pixels of right padding to prevent text from touching/trailing the edge.
- Safe inline text icons are acceptable before real RuneLite sprites are wired:
  - `▴` skills/XP
  - `⚔` boss KC
  - `★` activities/minigames

## No-data fallback

If WOM has no gains for the selected period after start/update fallback, show a short wrapped message instead of one long sentence. The user requested roughly every three words per line, e.g.:

```html
No recent gains<br>
found. WOM tracking<br>
was started/updated if<br>
needed. Try 30/365<br>
days or check<br>
again after XP/KC<br>
changes.
```

## Visual verification

For this class of UI tweak, build success is not enough. Render or screenshot with a representative player such as `oyama` and inspect that:

- no card text is pushed right,
- no giant blank card height appears,
- each stat is individually scannable,
- bold values are visible,
- right padding exists without wasting left space.
