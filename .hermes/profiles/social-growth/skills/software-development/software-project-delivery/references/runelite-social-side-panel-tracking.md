# RuneLite social side-panel tracking notes

Use when building RuneLite plugins that track friends, clan chat, or friends chat in a side panel.

## UI constraints

- RuneLite side panels must fit the default side-panel width. Do not assume players will resize the client.
- Prefer compact controls: a top tab row with a small icon button (e.g. `↻`) for refresh instead of a full-width `Rescan` row.
- Keep tab labels readable but narrow; if labels overflow, shorten labels before shrinking the panel-host width.
- Replace verbose row buttons like `Remove` with compact icon buttons such as `×` plus a tooltip.
- Disable horizontal scrolling for plugin panels and make text wrap intentionally at a conservative width.
- Test with real RuneLite client screenshots; Swing layout that compiles can still be visually too wide.

## Social source scanner API pattern

Useful RuneLite APIs observed for social list reads:

- Friends list: `client.getFriendContainer()` → `FriendContainer.getMembers()` → `Friend.getName()`, `Friend.getWorld()`.
- Friends chat: `client.getFriendsChatManager()` → `FriendsChatManager.getMembers()` → `FriendsChatMember.getName()`, `getWorld()`.
- Clan chat: `client.getClanChannel()` → `ClanChannel.getMembers()` → `ClanChannelMember.getName()`, `getWorld()`.

Scanner behavior:

1. Return a supported snapshot with zero members when the API is present but the list is empty.
2. Return an unsupported/status snapshot when the source is unavailable, null, or the user is logged out/no clan/no friends chat.
3. Derive online/offline status from `world > 0` when available.
4. Preserve source tags separately (`FRIEND`, `CLAN`, `FRIENDS_CHAT`) even when the same player appears in multiple lists.
5. Keep removed/ignored members out of future scans until the user explicitly re-adds or clears ignored state.

## Refresh cadence

- Rescan on plugin startup.
- Rescan whenever the player reaches `GameState.LOGGED_IN`.
- Provide a manual refresh icon/button near the tabs.
- Add a configurable integer refresh interval in minutes; default to 60 minutes for social tracking to avoid wasteful polling.
- Gate scheduled refreshes using a timestamp so `GameTick` does not rescan every tick.

## Product staging

Start with local social tracking (names/source/world/status/remove/ignore/cap) before external Wise Old Man or TempleOSRS enrichment. External XP/KC calls should enrich the tracked-member model later, not be required for the panel to feel useful.
