# Who's Grinding Panel: social sources, detail views, and gains windows

Session-derived product/implementation notes for the user's RuneLite social activity panel.

## Source model

Do not collapse RuneLite social sources into only Friends List / Friends Chat. The user explicitly wants three separate panel/filter sources:

- Friends List — `Client#getFriendContainer()` / `FriendContainer#getMembers()`
- Friends Chat — `Client#getFriendsChatManager()` / `FriendsChatManager#getMembers()`
- Clan Chat — `Client#getClanChannel()` / `net.runelite.api.clan.ClanChannel#getMembers()`

Important API namespace pitfall: current RuneLite exposes clan types under `net.runelite.api.clan.*`, not `net.runelite.api.ClanChannel`.

Recommended user-facing labels:

- `Friends List`
- `Friends Chat`
- `Clan Chat`

Keep Clan Chat as a real in-game functionality even if the plugin is no longer clan-only.

## Side-panel UX direction

The user reviewed screenshots and said the current list panel looked bad. Durable UX corrections:

- Make member names/text smaller and denser than default Swing labels.
- Do not waste vertical space on large explanation sections when real player rows/details are the product.
- Keep source selection compact, but preserve all three sources above.
- Display what each player is currently grinding, not just online/source/world.
- Clicking a profile should not end at a basic `JOptionPane` dump; evolve it into an in-panel player detail view/card.

## Detail view target

For a clicked member, build toward a detail view inspired by Wise Old Man's gained page, but keep the RuneLite panel compact:

- Prefer inline expandable/collapsible rows: click a player row to expand the grinding card immediately below that row; click again to collapse.
- The primary visible detail should be `Grinding <period>`: top selected-period skills/bosses/activities from Wise Old Man gained data.
- If the user does not want profile/source details shown, remove the separate selected-player card, profile URLs, source lines, and any `Data links` section entirely.
- Avoid a `JOptionPane` modal and avoid a visually detached bottom card unless explicitly requested.
- If links are kept in a future variant, keep them behind a compact details interaction rather than always occupying sidebar space.
- Last-updated/source/caching status should be short and only shown when it helps diagnose loading.

## Configurable gains windows

The user requested configurable windows:

- Day / 1 day
- 7 days
- 30 days
- 365 days

For Wise Old Man links/API mapping, use:

- Day -> `period=day`
- 7 days -> `period=week`
- 30 days -> `period=month`
- 365 days -> `period=year`

Prefer an enum such as `GainsPeriod` with `label()`, `days()`, and external API period mapping, plus tests.

## External API integration cautions

Wise Old Man and TempleOSRS are the best fits for current-grind/detail data. Do not query every visible player every tick. Use click-to-fetch, caching, explicit refresh, and bulk endpoints where available.

If external web/API calls are added, Plugin Hub review guidance requires clear config/plugin warnings describing what player data is sent to third-party services.
