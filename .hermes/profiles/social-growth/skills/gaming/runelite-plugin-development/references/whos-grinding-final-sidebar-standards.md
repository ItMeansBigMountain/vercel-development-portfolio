# Who's Grinding Panel: final sidebar standards from user review

Use this when polishing Who's Grinding Panel or future RuneLite sidebar plugins with narrow expandable cards.

## Approved width and inset standard

- Match the content width visually approved by the user: the same width as the top title/dropdown/control area.
- Do **not** use the full screenshot/window width as the target. RuneLite sidebars have a narrow real content budget; a maximized client can make a fixed-width column look unusually small without making the plugin's standard-width budget wrong.
- Align major content to the same left edge as the dropdown/title block.
- Keep only a tiny right safety pad, around 3 px.
- Avoid both trailing cutoff and large right gutters.
- If the whole column looks slammed against the left edge, add one small left inset to the shared `content` container. For Who's Grinding, `BorderFactory.createEmptyBorder(2, 4, 2, 0)` produced the requested subtle 4 px shift.
- Apply the shift to the shared container—not separate title, summary, control, member-row, and card margins—so all elements remain aligned and width logic stays centralized.
- Keep the inset as a named dimensions constant and assert its value in the dimensions test. Do not subtract it from or expand every child independently unless visual verification proves clipping.

## Expanded player card standards

- Inline expandable row: click player row to expand card under that row; click again to collapse.
- No separate bottom detail card.
- Grinding-only content: no data links, no source/debug rows, no WOM/Temple/hiscore URL rows.
- Content-sized height only. No `Short.MAX_VALUE` max-height on expanded cards.
- With Swing `BoxLayout`, set `Component.LEFT_ALIGNMENT` on the card, top controls, member rows, and every label row.
- Avoid one giant HTML label for complex cards. Split the card into individual `JLabel` rows so wrapping/height are predictable.
- Keep label borders/margins at zero; add only the small right card pad.

## Stat formatting

Every card item is line-by-line:

```text
Grinding 7 days
Skills:
▴ Ranged: +379,085 xp
▴ Hitpoints: +248,500 xp
Bosses:
⚔ Phantom Muspah: +37 kc
⚔ Scurrius: +19 kc
Activities:
★ PvP Arena: +132 score
★ LMS: +34 score
```

Rules:

- Skills, bosses, and activities all get one row per item.
- Gained values (`xp`, `kc`, `score`) should be bolded.
- Use readable card text around 12f for rows and 13f for card headings, unless clipping forces reduction.
- Friendly labels:
  - `last_man_standing` -> `LMS`
  - `bounty_hunter_hunter` -> `Bounty Hunter`
  - `bounty_hunter_rogue` -> `Bounty Hunter Rogue`

## No-data behavior

If WOM cannot find useful stats:

1. Start/update WOM tracking with `POST /v2/players/{name}`.
2. Retry gained data.
3. If still no positive gains, show a short wrapped message with roughly three words per line, e.g.:

```html
No recent gains<br>
found. WOM tracking<br>
was started/updated if<br>
needed. Try 30/365<br>
days or check<br>
again after XP/KC<br>
changes.
```

## Verification checklist

Before saying the UI is done:

1. Run `./gradlew clean test assemble --no-daemon --console=plain` with Java 11.
2. Use representative WOM data such as `oyama` to verify skills, bosses, and activities all render.
3. Generate or visually inspect a sidebar-width render/screenshot.
4. Confirm: no cutoff, no big left/right gutters, no blank card height, bold values visible, and card width matches the approved top control width.
5. Clean temporary render files before final repo status/push unless the user explicitly wants them committed.
