# Who's Grinding Panel: WOM grinding detail UI lessons

Session-derived implementation notes for wrapping the Who's Grinding Panel into a polished RuneLite sidebar plugin.

## User-approved product target

- The panel should showcase **what each player has been grinding during the selected period**.
- Do not surface source/debug clutter in the player detail card: no Friends/Clan source line, no WOM/Temple/Hiscore URL rows, no broad “data links” section.
- Player rows should be compact and expandable: click once to expand the grinding card directly under that row, click again to collapse.
- The expanded card should be only as tall as its rendered data. Avoid `Short.MAX_VALUE` max heights or anything that lets BoxLayout stretch a card into a huge blank block.
- Use essentially all available sidebar width: reduce left/right borders and HTML label width subtraction. If text trails/cuts off, make the safe width narrower and wrap earlier; if there is left blank space, remove card/content padding.
- Font must be readable; the expanded grinding card needed larger text than the player rows.

## WOM data wiring

- Selected-period grinding should come from Wise Old Man gained data:
  - `GET https://api.wiseoldman.net/v2/players/{name}/gained?period={day|week|month|year}`
  - map config periods via `GainsPeriod.wiseOldManPeriod()`.
- If gained lookup fails because a player is not tracked yet, start/update WOM tracking, then retry:
  - `POST https://api.wiseoldman.net/v2/players/{name}`
- Load WOM data in a background worker, not on the Swing EDT.
- Cache by normalized player + period so expanding/collapsing rows does not refetch every repaint.
- Include all WOM gained categories, grouped separately so XP does not drown KC/activities:
  - Skills: `experience.gained`
  - Bosses: `kills.gained`
  - Activities/minigames/LMS/clues/etc.: `score.gained`
- Test with a real known player such as `oyama`; WOM week data should include skill XP, boss KC, and activity score gains.

## Visual verification approach

When the user reports screenshot spacing issues, do not rely on build success alone. Produce or inspect a visual rendering if desktop RuneLite is not directly accessible:

1. Verify live WOM output for a known username (`oyama`) before blaming UI.
2. Render a small sidebar-width mock/screenshot using the same content shape.
3. Confirm visually: no large left margin, no trailing/cutoff text, no blank card height after the grinding data.
4. Then run `./gradlew clean test assemble --no-daemon --console=plain` and push child + parent pointer.

## Common Swing pitfalls from this session

- `BoxLayout` may stretch components if `maximumSize` is too tall. For content-sized cards, compute preferred height after adding labels and set both preferred and maximum height to that value.
- HTML `JLabel` width controls wrapping; too-wide labels can trail off, too-narrow labels can create excessive vertical height. Tune against `PluginPanel.PANEL_WIDTH`, scrollbar width, and explicit safety margin.
- Hidden padding accumulates: content border + row border + card border + HTML body width subtraction can visually push text right even when each looks small in isolation.
