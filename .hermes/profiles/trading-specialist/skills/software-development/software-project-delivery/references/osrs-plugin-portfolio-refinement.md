# OSRS / RuneLite Plugin Portfolio Refinement Notes

## Active workspace vs archived/template repos

For this user's OSRS plugin workspace, keep the top-level `projects/osrs-plugins/` directory focused on active plugins and a small number of planning files. Thin or overlapping plugin repos should be removed from the parent HeRmEz submodule list after their product direction is captured in canonical repos.

Current desired active plugin set after cleanup:

- `BossReadinessScore`
- `CompetitionOverlay`
- `IceBarrageTimer`
- `PersonalProgressTimeline`
- `RivalRadar`
- `SmartHiscoreLookup`
- `WhosGrindingClanPanel` / product name `Who's Grinding Panel`

Keep planning/history files such as:

- `README.md`
- `OSRS_PLUGIN_CLEANUP_PLAN.md`
- prior review JSONL/log artifacts when useful

Removed-from-parent submodules can still exist as remote repos/history; they should not clutter a fresh HeRmEz clone unless intentionally re-added.

## Boilerplate handling

`osrs-plugins-boilerplate` is useful, but it should not appear as a top-level active plugin folder in `projects/osrs-plugins/`. Prefer one of these patterns:

1. Keep it remote-only and link to it from `README.md` / cleanup docs.
2. If a local copy is needed, re-add it under a template path such as:
   - `projects/osrs-plugins/_templates/osrs-plugins-boilerplate`

Do not leave it beside active plugin projects, because the user reads that directory as the active portfolio.

## Canonical consolidation targets

### SmartHiscoreLookup / Account Intel

Absorb features from:

- `AccountLegacyCard`
- `NameChangeWatcher`

Target functionality:

- local account snapshot/card
- player lookup/detail panel
- official hiscore links
- previous/current display-name detection from RuneLite `Nameable#getPrevName()`
- tracker enrichment from official hiscores / Wise Old Man / TempleOSRS where appropriate

### RivalRadar / Race-Streak-Rival family

Absorb features from:

- `SkillNemesis`
- `SkillRaceCreator`
- `BossRaceCreator`
- `BossKCRivalLookup`
- `BossStreaks`
- `SkillStreaks`

Target functionality:

- rival comparisons
- skill/boss races
- skill/boss streaks
- nemesis/weakness analysis
- competition-ready progress views

## Standalone plugin policy

The user does not want end users to install multiple RuneLite plugins just to unlock a detail view. Similar code standards and copied/adapted helper patterns are acceptable, but avoid plugin-to-plugin runtime dependencies unless the user explicitly approves a shared library strategy.

## Parent submodule cleanup workflow

When removing consolidated/obsolete OSRS plugin folders from HeRmEz:

```bash
git submodule deinit -f projects/osrs-plugins/OldPlugin || true
git rm -f projects/osrs-plugins/OldPlugin
# repeat for each removed submodule
git add .gitmodules projects/osrs-plugins/OSRS_PLUGIN_CLEANUP_PLAN.md
git commit -m "chore: prune consolidated osrs plugin submodules"
git push origin main
```

After pushing, verify:

```bash
grep -n "projects/osrs-plugins" .gitmodules
git submodule status --recursive | grep 'projects/osrs-plugins'
find projects/osrs-plugins -maxdepth 1 -mindepth 1 -printf '%f\n' | sort
git status --short --branch
```

## Windows clone cleanup note

After pulling parent submodule deletions, stale submodule directories may still appear locally on Windows. Tell the user to run:

```bat
git pull origin main
git submodule sync --recursive
git submodule update --init --recursive
```

If old directories still linger, remove them manually with `rmdir /s /q <FolderName>` from `projects\osrs-plugins`. This is local cleanup of removed submodule worktrees, not a sign the parent repo still tracks them.

## RuneLite panel UI lessons from this session

- Default RuneLite side panels are narrow; screenshots showing controls trailing right should trigger a layout simplification immediately.
- Wide top tabs can overflow; a constrained `JComboBox` plus small icon button may be safer.
- Under Swing `BoxLayout`, set explicit preferred/maximum sizes for selector rows, combo boxes, and refresh buttons, otherwise components can stretch vertically or horizontally.
- Keep refresh buttons visible: compact icon text such as `↻`, fixed width/height, and a tooltip.

## Social API working notes

For social/player discovery, inspect the local `runelite-api` jar with `javap` when docs/examples are unclear. Verified candidate APIs from this session included:

```java
Client#getFriendContainer()
Client#getFriendsChatManager()
Client#getClanChannel()
Client#getGuestClanChannel()
Client#getClanSettings()
Client#getGuestClanSettings()
```

Useful event classes included:

```java
ClanChannelChanged
ClanMemberJoined
ClanMemberLeft
FriendsChatChanged
FriendsChatMemberJoined
FriendsChatMemberLeft
RemovedFriend
```

Record only working examples and verified API signatures in project-local notes such as `PROJECT_NOTES.md` so future sessions do not re-research old context externally.
