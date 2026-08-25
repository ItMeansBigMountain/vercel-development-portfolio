# Who's Grinding Panel: compact line-by-line card layout

Session lesson: user-reviewed RuneLite sidebar screenshots showed that a single HTML blob in the expanded player card made the card drift right, wrap poorly, and create excessive blank height. Build the card from individual rows instead.

## Required card behavior

- Expanded row card is inline under the clicked player row; click again collapses.
- Everything in the card is line-by-line:
  - every skill XP gain gets its own row
  - every boss KC gets its own row
  - every activity/minigame score gets its own row
- Use readable text: approximately 12f title and 11f item rows.
- Keep the left edge tight, but add a tiny right safety padding (~3px) so text does not touch the sidebar icon rail.
- Keep the card height content-sized only; no blank vertical filler.

## Swing implementation pattern

Do not render the whole card as one giant HTML `JLabel`.

Preferred pattern:

```java
JPanel card = new JPanel();
card.setLayout(new BoxLayout(card, BoxLayout.Y_AXIS));
card.setAlignmentX(Component.LEFT_ALIGNMENT);
card.setBorder(BorderFactory.createCompoundBorder(
    BorderFactory.createMatteBorder(0, 0, 1, 0, ColorScheme.DARK_GRAY_COLOR),
    BorderFactory.createEmptyBorder(0, 0, 4, 3)
));

int cardHeight = 0;
JLabel title = cardLine("<span style='color:#d3972b'><b>Grinding " + period + "</b></span>", 12f);
card.add(title);
cardHeight += title.getPreferredSize().height;

for (String line : summary.split("<br>"))
{
    JLabel row = cardLine(line, 11f);
    card.add(row);
    cardHeight += row.getPreferredSize().height;
}
cardHeight += 4;
card.setPreferredSize(new Dimension(PANEL_TEXT_WIDTH, cardHeight));
card.setMaximumSize(new Dimension(PANEL_TEXT_WIDTH, cardHeight));
```

Each row should be left-aligned and zero-margin:

```java
label.setAlignmentX(Component.LEFT_ALIGNMENT);
label.setBorder(BorderFactory.createEmptyBorder(0, 0, 0, 0));
label.setMaximumSize(new Dimension(PANEL_TEXT_WIDTH, label.getPreferredSize().height));
```

Also set `Component.LEFT_ALIGNMENT` on source selector rows and member rows so BoxLayout does not center narrower components.

## WOM summary formatting

- Join all sections with `<br>` between every item, including skills.
- Friendly text markers are acceptable before real sprite support:
  - `▴` skill/XP
  - `⚔` boss KC
  - `★` activity/minigame score
- Friendly labels:
  - `last_man_standing` -> `LMS`
  - `bounty_hunter_hunter` -> `Bounty Hunter`
  - `bounty_hunter_rogue` -> `Bounty Hunter Rogue`

## No-stats fallback

When a player has no useful stats:

1. Try WOM gained endpoint.
2. If missing/untracked, `POST /v2/players/{name}` to start/update tracking.
3. Retry gained endpoint.
4. If still no positive gains, show a compact message such as:

```text
No recent gains found. WOM tracking was started/updated if needed. Try 30/365 days or check again after XP/KC changes.
```

Do not tell the user or UI simply that data cannot be found without explaining the next useful action.
