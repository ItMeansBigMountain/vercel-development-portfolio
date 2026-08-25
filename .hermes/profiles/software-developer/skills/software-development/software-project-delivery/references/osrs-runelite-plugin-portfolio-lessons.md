# OSRS / RuneLite plugin portfolio lessons

Session-derived guidance for this user's RuneLite plugin work.

## Default side-panel width is a hard UX constraint

RuneLite side panels must fit the default sidebar width. Do not assume players will resize RuneLite to see controls.

Practical UI rules:

- Avoid three horizontal tabs when labels are long; use a compact dropdown plus a small icon button instead.
- Do not put a full-width `Rescan`/action button below source selectors if vertical/horizontal space is tight.
- For Swing controls in `PluginPanel`, explicitly constrain preferred/maximum sizes when using `BoxLayout`; otherwise controls like `JComboBox` can stretch into oversized rows and push adjacent buttons off-screen.
- Use compact constants early, e.g. panel text around 150-170px, member row text around 95-115px, small outer padding (4-6px), no horizontal scrollbar, and compact remove buttons (`×`) with tooltips.
- If the user says controls trail off, fix layout first; do not just shrink fonts repeatedly.

## Social-list scanners

For RuneLite social tracking, inspect the installed `runelite-api` jar with `javap` when unsure of live APIs. Useful API paths observed:

- Friends list: `client.getFriendContainer()` → `FriendContainer#getMembers()` → `Friend#getName()`, `Friend#getWorld()`.
- Friends chat: `client.getFriendsChatManager()` → `FriendsChatManager#getMembers()` → `FriendsChatMember#getName()`, `getWorld()`.
- Clan chat/channel: `client.getClanChannel()` → `ClanChannel#getMembers()` → `ClanChannelMember#getName()`, `getWorld()`.
- If `getClanChannel()` is empty in client testing, next probes are `ClanChannelChanged`, `ClanMemberJoined`, `ClanMemberLeft`, `client.getClanChannel(int)`, `client.getClanSettings(int)`, and guest clan APIs.

## WhosGrindingPanel product direction

The plugin is broader than clan-only. Prefer the display/product name `Who's Grinding Panel` and keep sources configurable:

- Friends Chat
- Clan Chat
- Friends List

Add a boolean config for showing offline friends; default should hide offline friends to avoid huge initial lists.

Rows should show at-a-glance status with a compact icon and clickable player details. Detail views should converge with the account/intel feature family (SmartHiscoreLookup / AccountLegacyCard / NameChangeWatcher), not duplicate long-term account-card logic.

## Portfolio consolidation direction

Treat related thin plugins as product families rather than many separate submissions:

- Account/intel family: merge `AccountLegacyCard` and `NameChangeWatcher` into `SmartHiscoreLookup`; WhosGrindingPanel detail cards should eventually reuse/link to this account detail model.
- Rival/race/streak family: consolidate `RivalRadar`, `BossKCRivalLookup`, `BossRaceCreator`, `SkillRaceCreator`, `SkillNemesis`, `BossStreaks`, and `SkillStreaks` into one rivalry/competition plugin.
- Keep standalone/high-value plugins: `BossReadinessScore`, `IceBarrageTimer`, `PersonalProgressTimeline`, and `CompetitionOverlay` until the user's larger CompetitionOverlay idea is specified.

When doing cleanup, finish and push active child plugin fixes first, then update parent submodule pointers carefully. Do not force-push parent HeRmEz if it is behind/ahead with unrelated dirty automation files; report the blocker and keep child repos clean/pushed.
