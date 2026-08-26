# Who's Grinding Panel: WOM grinding summary and compact row UX

Session-derived implementation notes for wrapping the RuneLite Who's Grinding Panel.

## Current target UX

- The main list should be compact: rows around 28px high, narrow enough for default RuneLite sidebar, no trailing text/buttons even when the desktop window is maximized.
- Avoid right-side row action buttons unless absolutely necessary; they caused trailing/width problems in the default panel.
- Player rows should expand/collapse inline: click once to show the player's grinding card below that row, click again to collapse. Prefer this over a separate bottom detail card.
- The expanded card should showcase only the grinding summary. Remove source/details clutter such as WOM/Temple/Hiscore URL rows, data-links sections, source lists, and modal popups.
- The expanded card text needs to be readable (larger than tiny 9-10pt detail text; 12pt worked better) and should use all available safe width with minimal/no left padding.
- Preserve horizontal safety: set `JScrollPane.HORIZONTAL_SCROLLBAR_NEVER`, constrain max/preferred widths, and make HTML labels wrap within the safe width.

## WOM gained summary semantics

The `Grinding` section means: what the player has gained during the configured period in RuneLite settings.

Use Wise Old Man gained API:

```text
GET https://api.wiseoldman.net/v2/players/{player}/gained?period={day|week|month|year}
```

`GainsPeriod` mapping:

- Day -> `day`
- 7 days -> `week`
- 30 days -> `month`
- 365 days -> `year`

Summarize gained data by section so XP does not drown out other activity:

- Skills: `experience.gained` as XP
- Bosses: `kills.gained` as KC
- Activities: `score.gained` as score, including LMS, clues, bounty hunter, soul wars, collection log, league points, etc.

Recommended compact output shape:

```html
<b>Skills</b>: Ranged: +379,085 xp; Slayer: +120,000 xp<br>
<b>Bosses</b>: Zulrah: +43 kc; Vorkath: +8 kc<br>
<b>Activities</b>: Last Man Standing: +34 score; Clue Scrolls Hard: +3 score
```

## Start tracking fallback

If the gained endpoint fails because the player is not tracked on WOM yet, try to start/update tracking, then retry gained:

```text
POST https://api.wiseoldman.net/v2/players/{player}
GET  https://api.wiseoldman.net/v2/players/{player}/gained?period={period}
```

Treat 200/201 from POST as success. Keep this on a background worker (`SwingWorker`) so RuneLite UI does not freeze. Cache by normalized player name + period.

## Plugin Hub/disclosure

External lookups send the selected player name to Wise Old Man. Keep a config toggle such as `Enable WOM lookups` with a clear description that player names are sent to wiseoldman.net.

## Windows run command

For this repo, the working Windows task is:

```bat
.\gradlew.bat run
```

Do not default to `runClient` for WhosGrindingClanPanel unless `run` is absent or fails.
