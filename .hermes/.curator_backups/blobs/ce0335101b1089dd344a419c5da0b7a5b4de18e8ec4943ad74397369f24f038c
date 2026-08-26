# RuneLite social/progress detail panels

Session-derived guidance for Who's Grinding Panel and adjacent OSRS plugins.

## Social sources: do not conflate these

RuneLite exposes three different player-social lanes that users expect as separate filters/panels:

- **Friends List** — `client.getFriendContainer()` / `FriendContainer.getMembers()`.
- **Friends Chat** — `client.getFriendsChatManager()` / `FriendsChatManager.getMembers()`.
- **Clan Chat / clan channel** — `client.getClanChannel()` / `net.runelite.api.clan.ClanChannel.getMembers()` and `ClanChannelMember.getName()/getWorld()`.

Pitfall: removing clan chat because the plugin should no longer be "clan-only" is wrong. The corrected product direction is **not clan-only**, but still includes Clan Chat as one source alongside Friends List and Friends Chat.

## Side-panel UX correction

The user showed the live RuneLite client and flagged these issues:

- Rows were too tall/sparse for the side panel.
- Names/text were too large.
- The heatmap/status block consumed too much vertical space compared with player rows.
- A `JOptionPane` click popup is not acceptable as the long-term detail UX.
- A clicked profile should show a real in-panel detail/card view.
- Player rows must surface what the person is likely grinding, not just `Online • W422 • Friend`.

Recommended pattern:

1. Main panel has compact source tabs/dropdown: Friends List, Friends Chat, Clan Chat.
2. Rows use small fonts (~9px), compact bullets/icons, and one-line summary where possible.
3. Clicking a player changes the side panel to a selected-player detail view instead of opening a modal.
4. Detail view includes quick links and cached external tracker data.
5. Keep heatmaps/status collapsible or below the core player list; do not let them crowd out rows.

## Progress/tracker APIs to use for detail views

### Wise Old Man

- Web: `https://wiseoldman.net`
- Docs: `https://docs.wiseoldman.net`
- API base: `https://api.wiseoldman.net/v2`
- Useful endpoints:
  - `GET /players/search?username=<partial>&limit=<n>`
  - `POST /players/:username` to update/track
  - `GET /players/:username`
  - `GET /players/:username/gained?period=week` or `startDate/endDate`
  - `GET /players/:username/snapshots/timeline?metric=overall&period=week`
  - `GET /players/:username/names`
  - `GET /players/:username/achievements`, `/records`, `/competitions`, `/groups`

Wise Old Man's gained page UX suggests the in-plugin detail card should include a compact gained table (Skill, Exp, Levels, Rank, EHP/EHB) plus a mini timeline/sparkline for the selected metric.

Caveat: probing from Hermes got HTTP 403 from WOM's API. Do not encode this as "WOM is unavailable"; for plugin work use a proper User-Agent, opt-in config, caching, and click-to-fetch/rate limiting.

### TempleOSRS

- Web: `https://templeosrs.com`
- Docs: `https://templeosrs.com/api_doc.php`
- Strong fit for clan/group competition workflows: player info/stats/gains/datapoints, group member stats, competitions, collection log, pets, EHP/EHB/rates.

### Crystal Math Labs

- Web: `https://crystalmathlabs.com`
- Useful for XP/rank tracking ideas and records, but generally secondary to WOM/Temple for first plugin integration.

### Official OSRS hiscores

Good fallback for current snapshot/rank/XP/KC. Not enough for historical "what are they grinding" unless we store snapshots locally.

## API usage policy inside RuneLite plugins

- External API integration must be opt-in or clearly explained in config/plugin warning per Plugin Hub guidance.
- Do not fetch every tracked player every tick.
- Prefer explicit refresh and clicked-player fetches.
- Cache responses and add last-updated/source labels.
- Prefer bulk endpoints for group/social lists when available rather than one request per member.
