# RuneLite social side-panel UI and live scanner notes

Use this when building RuneLite side-panel plugins that track friends, clan, or friends chat members.

## Default-width side panel rules

RuneLite side panels must fit the default sidebar width without requiring the player to resize the client.

Practical UI rules:

- Avoid horizontal tab sets for 3+ views; they often overflow or hide action buttons.
- Prefer a compact `JComboBox` source selector plus a small icon button for refresh/actions.
- Explicitly constrain Swing controls when using `BoxLayout`:
  - set `setPreferredSize(...)`
  - set `setMaximumSize(...)`
  - disable horizontal scrollbars on the panel `JScrollPane`
- Keep content padding small, usually 4–6 px.
- Use compact action buttons such as `↻` for refresh and `×` for per-row remove.
- Use HTML label body widths well under the panel width, e.g. 150–170 px for summary text and narrower widths for row text when an action button sits beside it.
- If a `JComboBox` displays enum names like `FRIENDS_CHAT`, override `toString()` on the enum to return a friendly label.

Example selector row pattern:

```java
JPanel row = new JPanel(new BorderLayout(3, 0));
row.setMaximumSize(new Dimension(PANEL_TEXT_WIDTH, CONTROL_HEIGHT));
row.setPreferredSize(new Dimension(PANEL_TEXT_WIDTH, CONTROL_HEIGHT));

JComboBox<SocialSourceFilter> sourceDropdown = new JComboBox<>(SocialSourceFilter.values());
sourceDropdown.setPreferredSize(new Dimension(PANEL_TEXT_WIDTH - 30, CONTROL_HEIGHT));
sourceDropdown.setMaximumSize(new Dimension(PANEL_TEXT_WIDTH - 30, CONTROL_HEIGHT));
row.add(sourceDropdown, BorderLayout.CENTER);

JButton refreshButton = new JButton("↻");
refreshButton.setPreferredSize(new Dimension(26, CONTROL_HEIGHT));
refreshButton.setMaximumSize(new Dimension(26, CONTROL_HEIGHT));
refreshButton.setMargin(new Insets(0, 3, 0, 3));
row.add(refreshButton, BorderLayout.EAST);
```

## Social list scanner APIs

For live social tracking, RuneLite exposes useful APIs through `Client`:

- Friends list: `client.getFriendContainer()` → `FriendContainer.getMembers()` → `Friend.getName()`, `Friend.getWorld()`.
- Friends chat: `client.getFriendsChatManager()` → `FriendsChatManager.getMembers()` → `FriendsChatMember.getName()`, `getWorld()`.
- Clan chat/channel: `client.getClanChannel()` → `ClanChannel.getMembers()` → `ClanChannelMember.getName()`, `getWorld()`.

Implementation pattern:

1. Keep a source-agnostic tracking service/model boundary.
2. Convert each source into a normalized snapshot: name, source tag, status, world, summary.
3. Merge the same normalized name across sources.
4. Preserve source tags separately so one player can be `FRIEND` and `CLAN`.
5. Let users remove/ignore members individually and skip ignored names on future scans.
6. Rescan on login, manual refresh, config change, and a configurable minute interval.
7. If a source is unavailable, show a clear status message instead of fake/demo people.

## Pitfalls

- Do not seed fake default people in user-facing plugin panels; start empty until live sources provide data.
- Do not let a dropdown, tab set, or button row expand vertically under `BoxLayout`; lock maximum/preferred dimensions.
- Do not rely on passing Gradle tests alone for UI fit; RuneLite panel width must be manually smoke-tested in the client.
