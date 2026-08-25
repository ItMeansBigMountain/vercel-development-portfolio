# Who's Grinding Panel compact card rendering lessons

Use this when polishing the Who's Grinding Panel expanded player row/card in RuneLite's narrow sidebar.

## Durable UI rules learned from user review

- The expanded player card must be **content-sized**, not merely narrow. Avoid any `BoxLayout` component max height like `Short.MAX_VALUE` for the card, because it can stretch into a tall blank block.
- After adding the grinding `JLabel`, compute the card height from the label's preferred height and lock both preferred and max height:
  ```java
  JLabel grindingLabel = detailHtmlLine("Grinding " + config.gainsPeriod().label(), grindingSummaryFor(member), false);
  card.add(grindingLabel);
  int cardHeight = grindingLabel.getPreferredSize().height + 4;
  card.setPreferredSize(new Dimension(PANEL_TEXT_WIDTH, cardHeight));
  card.setMaximumSize(new Dimension(PANEL_TEXT_WIDTH, cardHeight));
  ```
- Keep card left/right padding at zero unless a screenshot proves text is touching badly:
  ```java
  BorderFactory.createEmptyBorder(0, 0, 4, 0)
  ```
- Card body text should use the full safe `PANEL_TEXT_WIDTH`; do not subtract arbitrary extra width for the card body because it creates a visible left/right gutter and more wrapping.
- The user cares more about compact, readable, no-blank-space layout than decorative cards. If the panel looks like there is unused real estate, remove padding/height before reducing text.

## WOM summary formatting rules

- Skills and activities can stay compact on a single wrapped line with semicolons.
- **Every boss KC must be on its own line**. Format the boss section with a line break after the heading and between each boss:
  ```java
  String separator = "Bosses".equals(title) ? "<br>" : "; ";
  String headingSeparator = "Bosses".equals(title) ? ":<br>" : ": ";
  sections.add("<b>" + title + "</b>" + headingSeparator
      + positiveLines.stream().map(GainedLine::format).collect(Collectors.joining(separator)));
  ```
- Add/keep a unit test that asserts multiple bosses render as:
  ```html
  <b>Bosses</b>:<br>Zulrah: +43 kc (KC)<br>Scurrius: +12 kc (KC)
  ```

## Verification pattern

- Do not rely only on `BUILD SUCCESSFUL` for sidebar layout complaints.
- Use `oyama` as a representative WOM player when verifying real gained data. It has recent XP, boss KC, and activities in the examples from this session.
- Probe the live WOM gained endpoint for representative data before debugging UI-level “no data” reports:
  ```text
  GET https://api.wiseoldman.net/v2/players/oyama/gained?period=week
  ```
- If a player is not tracked, use the existing WOM update fallback pattern: `POST /v2/players/{name}` then retry `GET /gained`.
- For visual confidence, generate or inspect a sidebar-width render/mock with representative `oyama` output and check: no cutoff/trailing text, no large left margin, and no blank card height.
