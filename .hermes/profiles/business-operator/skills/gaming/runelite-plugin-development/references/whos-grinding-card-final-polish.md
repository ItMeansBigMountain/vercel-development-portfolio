# Who's Grinding card final polish notes

Use when the user is reviewing screenshots of the Who's Grinding Panel expanded player card.

## Target card layout

- Row click expands/collapses a grinding-only card directly under that player.
- No links/source/debug rows in the card unless explicitly requested.
- Everything inside the card is vertical, one item per line:
  - `Skills:` then each skill XP gain on its own line.
  - `Bosses:` then each boss KC on its own line.
  - `Activities:` then each activity/minigame score on its own line.
- Use readable text: about 12f for title/section headers and 11f for stat lines.
- Use minimal margins: left edge tight, only a couple pixels of right padding (~3px), no blank vertical filler.
- Avoid a single giant HTML label for the whole card; use separate left-aligned `JLabel` rows and compute the card height from row preferred heights.

## Lightweight category markers

Until real RuneLite/OSRS sprite icons are deliberately wired:

- `▴` skill/XP
- `⚔` boss KC
- `★` activity/minigame score

Friendly WOM label examples:

- `last_man_standing` -> `LMS`
- `bounty_hunter_hunter` -> `Bounty Hunter`
- `bounty_hunter_rogue` -> `Bounty Hunter Rogue`

## No-stats fallback

When WOM gained data is missing or zero:

1. Try gained endpoint for selected period.
2. If that fails, POST `/v2/players/{name}` to start/update tracking.
3. Retry gained endpoint.
4. If still no positive gains, show a compact actionable fallback: tracking was started/updated if needed; try 30/365 days; check again after XP/KC/activity changes.

## Verification

For screenshot-driven UI work, build success is not enough. Generate or inspect a sidebar-width render using live representative data such as `oyama`, then check:

- no cutoff/trailing text
- no large left margin
- slight right padding
- no blank card height
- every card stat is line-by-line
- text is readable
