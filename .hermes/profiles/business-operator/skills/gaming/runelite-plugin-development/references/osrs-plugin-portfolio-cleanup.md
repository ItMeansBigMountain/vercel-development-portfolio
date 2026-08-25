# OSRS Plugin Portfolio Cleanup Notes

Captured from the July 2026 coding-channel OSRS plugin cleanup discussion. Use as current direction until superseded by a newer user instruction.

## Authenticated repo inventory

Authenticated GitHub access via `GITHUB_ACCESS_TOKEN` found 20 OSRS/RuneLite-related repos:

- `rival-radar-osrs`
- `smart-hiscore-lookup-osrs`
- `whos-grinding-clan-panel-osrs`
- `account-legacy-card-osrs`
- `boss-readiness-score-osrs`
- `skill-streaks-osrs`
- `skill-race-creator-osrs`
- `skill-nemesis-osrs`
- `personal-progress-timeline-osrs`
- `name-change-watcher-osrs`
- `ice-barrage-timer-osrs`
- `group-iron-progress-board-osrs`
- `competition-overlay-osrs`
- `clan-grind-heatmap-osrs`
- `boss-streaks-osrs`
- `boss-race-creator-osrs`
- `boss-k-c-rival-lookup-osrs`
- `osrs-plugins-boilerplate-osrs`
- `plugin-hub`
- `breach-check-osrs`

## Active local plugin workspace

Current narrowed active worktrees under `/opt/data/HeRmEz/projects/osrs-plugins`:

- `BossReadinessScore`
- `CompetitionOverlay`
- `IceBarrageTimer`
- `PersonalProgressTimeline`
- `RivalRadar`
- `SmartHiscoreLookup`
- `WhosGrindingClanPanel`

Top-level workspace also contains `_templates`, `README.md`, `OSRS_PLUGIN_CLEANUP_PLAN.md`, and historical review JSONL.

## Product lanes

### Who's Grinding Panel

Formerly `WhosGrindingClanPanel` / `whos-grinding-clan-panel-osrs`.

Immediate focus before repo cleanup:

- Add/keep config checkbox to show offline friends.
- Fix social source discovery using actual RuneLite API inspection, not guesses.
- Remove clan-first framing; the user wants this to be for everyone: **Who's Grinding Panel**.
- Add at-a-glance indicators/icons for what a player has been doing.
- Clicking a player should open/detail tracker information similar to account intelligence plugins.

### Account intelligence lane

Merge/absorb overlapping identity/profile plugins here:

- `SmartHiscoreLookup`
- `AccountLegacyCard`
- `NameChangeWatcher`
- detail information from Who's Grinding Panel where appropriate

User direction: AccountLegacyCard and SmartHiscoreLookup are effectively the same project; missing features from each should be merged.

### Keep as important standalone lanes

- `BossReadinessScore`: best-in-slot/current gear/readiness tab; user called it very useful.
- `IceBarrageTimer`: important for knowing when a target is barraged.
- `CompetitionOverlay`: keep; user has a bigger future idea for it.
- `PersonalProgressTimeline`: keep.

### Consolidation candidate lane

Likely merge into one coherent competitive/rivalry project/repo after analysis:

- `RivalRadar`
- `SkillNemesis`
- `SkillRaceCreator`
- `BossStreaks`
- `SkillStreaks`
- possibly boss race/rival lookup variants after review

## Execution order

1. Fix and verify Who's Grinding Panel code issues.
2. Build/test child repo with Java 11 Gradle flow.
3. Commit/push child repo.
4. Perform full analysis of active OSRS plugin repos.
5. Produce cleanup/consolidation plan.
6. Only after review, execute repo/submodule cleanup.
7. Push child repos first, then update/push `/opt/data/HeRmEz` parent so reclone + submodule update works.

## UI lessons from session

- RuneLite side panel width is tight; long tabs/dropdowns can trail off to the right.
- Fix by constraining dimensions and labels, not by assuming the layout is acceptable.
- Compact dropdowns and icon buttons must have fixed height/width; otherwise Swing layouts may stretch them and hide controls.
