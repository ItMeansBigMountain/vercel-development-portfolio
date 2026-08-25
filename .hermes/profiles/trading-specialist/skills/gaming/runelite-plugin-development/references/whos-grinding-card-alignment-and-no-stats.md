# Who's Grinding Panel: card alignment and no-stats fallback

Session lesson from user screenshots: a Swing `BoxLayout` expanded player card can still look badly spaced even when its preferred/max height is content-sized if the body is rendered as one large HTML `JLabel`. The label can visually push right and create the appearance of a wide left gutter.

## Card rendering fix

Prefer building the expanded grinding card as multiple left-aligned rows:

- Parent card: `BoxLayout.Y_AXIS`.
- Set `setAlignmentX(Component.LEFT_ALIGNMENT)` on:
  - selector/control rows,
  - member rows,
  - expanded card,
  - every label inside the card.
- Do **not** render all skills/bosses/activities as one giant HTML blob.
- Create one `JLabel` per logical line/row, e.g.:
  - `Grinding 7 days`
  - compact skills line(s),
  - each boss KC line,
  - each activity/minigame score line.
- Compute card height by summing each row label’s preferred height, then set both preferred and maximum card size to that exact height.
- Use a helper like `cardLine(html, fontSize)` that sets `margin:0; padding:0`, zero border, left alignment, and max size to the safe panel width.

## Formatting rules

- Boss KC: one boss per line.
- Activities/minigames: one activity per line, including LMS, Bounty Hunter, PvP Arena, clue scrolls, collection log, Soul Wars, etc.
- Skills may stay compact if that preserves sidebar space.
- Use friendlier labels for common WOM activity keys:
  - `last_man_standing` -> `LMS`
  - `bounty_hunter_hunter` -> `Bounty Hunter`
  - `bounty_hunter_rogue` -> `Bounty Hunter Rogue`

## If WOM cannot find useful stats

The product behavior should be explicit and useful, not a dead error:

1. Try gained data for the selected period.
2. If the player is not tracked / gained fetch fails, POST `/v2/players/{name}` to start/update WOM tracking and retry.
3. If the retry succeeds but has no positive gains, show a compact card message such as:
   `No recent gains found. WOM tracking was started/updated if needed. Try 30/365 days or check again after XP/KC changes.`

Interpretation for the user: there may be no gains in the selected period, WOM may have just begun tracking, or the player needs to gain XP/KC/activity score before WOM can show a useful delta.

## Verification expectation

Build success is not enough for spacing bugs. For screenshot-driven spacing complaints, generate or inspect a sidebar-width render using representative data (e.g. `oyama`) and verify visually that:

- the expanded card starts at the left edge of the list/card region,
- there is no giant blank card height,
- rows are individually scannable,
- no text trails off the side panel.
