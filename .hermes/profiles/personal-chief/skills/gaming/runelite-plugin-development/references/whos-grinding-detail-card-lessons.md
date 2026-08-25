# Who's Grinding detail-card lessons

Session lessons for RuneLite sidebar detail UX after user review of Wise Old Man screenshots and in-client layout complaints.

## User-facing detail-card rules

- Keep the card narrow and vertical; RuneLite sidebar width is the hard constraint.
- Remove low-value visualizations when space is tight. The activity heatmap was explicitly rejected because it used too much space.
- Avoid a separate `Sources` line in the selected-player detail card when external profile URLs are present. WOM/TempleOSRS/hiscore URLs provide enough source/context detail.
- Use readable detail/member text; 9f felt too small in practice, 10f is a better default for these rows/cards.
- Prefer an in-panel selected-player card over `JOptionPane` popups.

## `Grinding` field semantics

Be careful explaining or labeling `Grinding`:

- Current implementation may only hold a local RuneLite social-scan summary, e.g. `Friends chat • world 486`, `Clan chat • world 330`, or `Friends list • offline`.
- That is not yet true WOM/TempleOSRS XP/KC inference.
- Do not claim the plugin knows the player is training a skill/boss until external gained data is actually fetched and cached.
- Target semantics for `Grinding`: recent WOM/TempleOSRS gained summary such as likely skill/boss, XP/KC gained, levels/rank/EHP deltas, and selected period.

## Preferred card fields

Current compact target:

- Name
- Status / world
- Grinding
- Period
- WOM gained URL
- TempleOSRS URL
- Official hiscore URL
- Seen timestamp range

Avoid adding back `Sources` unless the user explicitly asks for it.
