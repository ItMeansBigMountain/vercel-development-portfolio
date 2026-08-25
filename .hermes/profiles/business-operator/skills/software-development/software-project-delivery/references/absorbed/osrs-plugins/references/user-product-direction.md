# User product direction for OSRS RuneLite plugins

Use this when shaping, pruning, or implementing the user's OSRS RuneLite plugin portfolio.

## Portfolio pruning

The user explicitly rejected these concepts and wanted both GitHub repos and local projects removed:

- Achievement Gap Finder
- Friend Progress Feed
- Nearby Player Snapshot

If these names reappear, do not recreate them unless the user explicitly reverses that decision.

## Account / lookup panels

### Account Legacy Card

The intended UX is a RuneLite side-panel dashboard for a looked-up username, not just a local login chat card. It should show the looked-up user's official hiscores plus richer account context from free OSRS APIs keyed by username.

Include source labels and freshness for fields from:

- Official OSRS Hiscores
- Wise Old Man
- TempleOSRS
- OSRS Wiki data/static APIs
- RuneProfile public API if it remains reliable/available

### Smart Hiscore Lookup

The intended plugin is one robust side panel that combines the information a player would normally visit several tracking websites to get. Do not position it as a simple URL builder. It should aggregate official hiscores, tracking-site snapshots/gains/records, collection-log/quest/diary/combat-achievement data where public APIs expose them, and graceful partial-data/error states.

Free data/API candidates found during the session:

- Wise Old Man API docs: open source OSRS tracker API for player progress, snapshots, gains, competitions, groups, records.
- TempleOSRS API: player info/stats/gains/datapoints, records, groups, competitions, pets, collection log, recent collections, rates, EHP/EHB.
- Official OSRS hiscores endpoints.
- OSRS Wiki APIs/static data for item, monster, boss, and gear metadata.
- RuneProfile public API may expose complete profile data including skills, quests, collection log, achievement diaries, and combat achievements; verify availability before depending on it.

## Rival / race consolidation

Boss rival, skill nemesis, skill race, boss race, and similar ideas should be consolidated into one plugin concept: set a rival by username and compare 1:1 using all available tracking APIs/endpoints. Optional deadline turns the comparison into a race; without a deadline it is an always-on comparison dashboard.

Target details:

- Configure one rival username.
- Optional race deadline/end date.
- Compare signed-in player vs rival across skills, bosses, clues, collection log, pets, recent gains, records, EHP/EHB, competitions/group data, and account metadata where APIs expose it.
- Show leads/trails, deltas since race start, progress needed before deadline, source freshness, and unavailable/private/untracked states.

Repos like BossKCRivalLookup, BossRaceCreator, SkillNemesis, and SkillRaceCreator should be treated as superseded by RivalRadar unless explicitly revived or deleted by the user.

## Clan panels

The user likes the clan concepts. The clan panel should use the player's real clan chat membership/roster, not friends chat.

Target side-panel UX:

- Show everyone in the clan chat roster in a scrollable RuneLite side panel.
- For each member, show inline skill/boss/activity icons for what they have gained most recently.
- Hover over icons to see source, timeframe, gained XP/KC/count, rank delta, last seen/update timestamp, and confidence/freshness.
- Fetch Wise Old Man / TempleOSRS data in the background with caching and partial-data states.

## Personal Progress Timeline

Once installed, this plugin should start tracking forward persistently. When the player opens the collection log, it should update/backfill with items already owned from RuneLite-visible state.

Target side panel:

- Scrollable timestamped milestones: levels, quests, combat achievements, collection-log items, pets, notable drops, boss KC milestones, clue milestones, etc.
- Persist locally across client restarts.
- Backfilled/observed milestones should not claim exact acquisition time when only snapshot evidence exists.
- Cross-check with Wise Old Man and TempleOSRS for robustness and timestamp/source confidence.

## PvP timers

Ice Barrage Timer is intended to track opponents' freeze and teleblock timers. It is not a self-freeze timer; that already exists.

Target behavior:

- Detect successful freezes/teleblocks applied by the player to opponents.
- Start/refresh opponent timers for freeze and teleblock durations.
- Show opponent name, status, remaining time, and expiry in overlay/panel.

## Boss readiness and gear

Boss Readiness Score should include best-in-slot / best-available gear recommendations inspired by GearScape, but simpler inside RuneLite.

Target UX:

- User selects boss/PvM target and optionally budget, owned/unowned item exclusions, combat style, and risk level.
- Panel shows readiness score, gear by slot, prayers/supplies, missing prerequisites, and simple upgrade priorities.
- Use OSRS Wiki-derived item/monster data where possible. Treat GearScape as product inspiration, not a private API dependency unless a stable public API is explicitly available.
