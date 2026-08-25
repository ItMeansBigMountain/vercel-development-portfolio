# Who's Grinding Panel: WOM selected-period grinding summaries

Session learning from implementing the detail-card `Grinding` field.

## Product correction

For this plugin, `Grinding` should mean: **what the selected player has been doing during the configured gains period**, not where the plugin discovered them socially.

Do not use source-only text such as `Friends chat • world 486` as the final Grinding value in the selected-player detail card. Social discovery/source data can remain in list rows or filters, but the detail card should focus on tracker/profile data.

## Wise Old Man gained endpoint

Use Wise Old Man's gained API for the selected player and configured period:

```text
https://api.wiseoldman.net/v2/players/{urlEncodedName}/gained?period={day|week|month|year}
```

Period mapping from `GainsPeriod`:

- Day -> `day`
- 7 days -> `week`
- 30 days -> `month`
- 365 days -> `year`

The response contains:

```text
data.skills.<metric>.experience.gained
 data.bosses.<metric>.kills.gained
 data.activities.<metric>.score.gained
```

Summarize **all positive gains** into line-by-line compact sidebar rows, not just a top-N subset. The user specifically corrected that they want to see every stat found with `+` gains so tracking can be audited.

```text
Ranged: +420,000 xp
Slayer: +180,000 xp
Zulrah: +43 kc
Clue Scrolls Hard: +3 score
```

Do not duplicate the gain type by appending `(XP)`, `(KC)`, or `(Score)` after values; the value suffix already says `xp`, `kc`, or `score`, and the section/icon provides the category.

Skip `skills.overall` when listing grinding items; it hides what the player actually trained.

## UX / implementation pattern

- Fetch selected/clicked players asynchronously; avoid blocking the RuneLite sidebar.
- Before reading gained data, call WOM's player create/update endpoint:
  ```text
  POST /v2/players/{urlEncodedName}
  ```
  Then call the gained endpoint. This makes newly discovered social usernames trackable before summaries are read.
- Cache by normalized player name + period.
- Show a loading line while fetching and a graceful fallback such as `Could not load Wise Old Man gains. Use the WOM link below.`
- Add a config toggle/warning when external lookup is enabled because the selected player name is sent to Wise Old Man.
- Keep WOM/TempleOSRS/official hiscore URLs in the card; remove a separate `Sources` line from the selected-player card unless the user asks for it again.
- If later implementing "load everyone on the server / social list" behavior, do it as a throttled queue with explicit pacing and dedupe, not as an eager bulk POST loop every scan. This protects WOM, keeps Plugin Hub review safer, and avoids UI/network spikes.

## Official hiscores fallback

The official hiscores fallback exists to compute period gains by cutting the difference between current official totals and a local baseline snapshot from the configured plugin lookback period.

Current stable fallback in this repo uses the official lite CSV endpoint:

```text
https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={urlEncodedName}
```

Do **not** casually swap this path to the JSON endpoint in a final/passive cleanup if WOM or player finding regresses. If researching JSON (`index_lite.json`) for newer metrics such as Sailing/new bosses, do it as a deliberate branch/tested change: verify WOM lookup still works for known players like `oyama`, verify fallback parsing against live official hiscores, and keep WOM as the primary source.

The baseline/lookback period is selected in plugin settings (`GainsPeriod.days()`: Day/7/30/365). For period gains, save a current local snapshot and compare it only against a local baseline snapshot at or before the configured lookback. Do not compare against a too-recent baseline and present it as a full 7/30/365-day gain; show the baseline-needed message instead.

Fallback lessons from live checks: TempleOSRS (`player_gains.php`) and Crystal Math Labs (`api.php?type=track`) may return “user not found” for names that official hiscores and WOM can read (tested with `tzaku`/`z7yn`). Keep them as optional middle fallbacks only after live validation. Official hiscores is the reliable last-resort source for saving a local baseline/current total, but it cannot produce immediate historical gains without an old-enough local snapshot.

## Search/rescan and panel-control UX lessons

- The logged-in profile row should be an editable search field, autofilled with the current RuneLite username but rewritable in-place; pressing Enter/search loads that player's grinding card even if they are not visible in social sources.
- Put the manual refresh/rescan affordance next to the current-user row rather than beside the source dropdown, but keep it in its own small button box with a visible gap from the current-user card. The user visually associates refresh with the current profile/header area while still expecting it not to be visually merged into the same player row.
- Rescan must feel like it refreshes real data, not merely updates a status message. Clear stale gained-summary cache on refresh and reload WOM/current fallback data for the selected/search player.
- User-facing, frequently-toggled filters belong in the panel when they affect immediate list/card behavior. For Who's Grinding, move `Gains period` / lookback and `Show offline friends` out of visible RuneLite settings into compact panel controls: source dropdown on one row, lookback dropdown underneath, and a same-height checkbox button beside it. Keep the underlying config keys persisted but mark them hidden in the settings interface.
- When panel controls write RuneLite config, inject `ConfigManager`, use `setConfiguration(CONFIG_GROUP, key, value)`, clear gain-summary cache when period/data display changes, and rescan social sources when offline-friend visibility changes. When toggling `Show offline friends` off, immediately prune cached offline friend rows before/without a full rescan; otherwise previously loaded offline friends remain visible even though new scans omit them.
- If the user says they cannot find players they previously could find, first restore the known-good WOM flow before extending fallback parsing.

## Dual-source tracking model

User goal for this plugin: players should find friends, clan chat, and friends-chat members and see what they have been doing over the selected day/week/month/year period without manual tracker setup. Treat social discovery and gain-data lookup as separate concerns.

Display WOM and official hiscores as two separate sections when requested, not as a hidden replacement pipeline:

```text
WOM gains:
...
Official Hiscores tracked:
...
```

Official hiscores should be tracked automatically for every inspected player that official hiscores can find. Compute official gains by saving local snapshots and diffing current totals against a baseline. For the configured period, prefer a strict old-enough baseline; if none exists but an older local snapshot exists, show best-available gains labeled clearly as partial (e.g. `Partial since first local snapshot`). If no prior snapshot exists, save the baseline and show a clear automatic-tracking message, not instructions for the user to go do something manually.

Do not tell the user/player to manually open WOM as the main recovery path. If WOM `POST /players/{username}` is blocked or WOM lacks gains, continue seamlessly with fallback tracking and explain only what the plugin is doing automatically.

When comparing tracker APIs and official hiscores, expose a config choice rather than assuming a single merged display is correct. Current preferred options are:

```text
Tracker APIs (WOM)
Official Hiscores delta
Both (development)
```

Use `Both (development)` for side-by-side debugging only; default user-facing behavior should favor tracker APIs unless the user selects official deltas. Include the selected data source in cache keys so switching config does not show stale summaries.

Rescan must clear the gained-summary cache before rescanning social sources. Otherwise tiny post-baseline official-hiscores changes (e.g. a few XP after relogging) can appear missing because the UI is rendering cached data rather than refetching official hiscores.

Official hiscores fallback deltas are not WOM-style weekly/monthly/yearly period trackers. They show the difference between the current plugin scan and the last saved plugin scan (after Jagex public hiscores reflects the new total). The UI should label this clearly as a fallback/local-scan delta and visually separate it from tracker APIs with a divider line. Mention fallback candidates in the card/source note: TempleOSRS, Crystal Math Labs, and official OSRS hiscores. For small gains, mention hiscores update latency as a likely cause before changing parsing logic.

Official `index_lite.ws` row order must stay aligned with RuneLite `net.runelite.client.hiscore.HiscoreSkill` for the pinned client version. In RuneLite 1.12.32 / current OSRS hiscores, the skill block includes `Sailing` after Construction; activities do **not** include the old Deadman/BH Legacy rows; and boss rows include newer entries such as Brutus, Maggot King, Shellbane Gryphon, Royal Titans, Yama, and Zulrah at the current final row. If rows are stale, later rows shift and create false deltas like fake Araxxor/Lunar Chests KC while hiding real Fishing XP. Version local snapshot serialization when row order changes and ignore old snapshots so users get a clean new baseline rather than comparing mismatched schemas.

- When the user asks for a console command “only errors”, return just the command, no explanation; for this Gradle/RuneLite repo use `./gradlew.bat run --no-daemon --console=plain --quiet 1>NUL` on Windows to suppress stdout while leaving stderr visible.

## WOM not-found / zero-gains handling

WOM has multiple “no useful stats” states that must not be collapsed into the same generic message:

1. `GET /players/{name}` or `/gained` returns 404: player is not tracked/found on WOM.
2. `/gained?period=day|week|month|year` returns 200 with `startsAt:null`, `endsAt:null`, and all gains zero: player exists, but WOM has no usable gain snapshots for that period.
3. `/gained` returns 200 with `startsAt == endsAt` and all gains zero: WOM has only one relevant snapshot or no change across snapshots.
4. `/gained` returns positive gains: render the gains normally.

Docs say `POST /v2/players/{username}` should “track or update” a player and return `PlayerDetails`, so the intended sequence is GET gains → POST update if missing/stale → retry GET gains. In practice, live probes from non-browser/server contexts returned Cloudflare 403 for POST while GET still worked. Do not describe this as a permanent WOM limitation; implement it as a handled runtime outcome. Important UX correction from the user: do **not** tell players to manually open/update WOM as the main recovery path. Keep the experience automatic and seamless: continue to official hiscores tracking, save a local baseline, label partial data when necessary, and only explain what the plugin is doing automatically.

For known examples from the session: `tzaku` and `z7yn` existed on WOM but had no positive day gains; `tzaku` week gains had null start/end and zeros, while `z7yn` week had equal start/end and zeros. These are not player-not-found cases.

## Git merge/pull recovery lesson

When the user pulls plugin changes on Windows and creates a conflict/merge commit, do not assume their conflict resolution preserved the intended behavior. Pull/fetch their pushed merge commit, search for conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) and stale UI text/suffixes, inspect the touched Java files and docs, then run `./gradlew clean test assemble --no-daemon --console=plain` before pushing cleanup. Also update the parent HeRmEz submodule pointer after the plugin repo is corrected.

## Final README / Plugin Hub documentation pass

For final-phase RuneLite plugin polish, update the README as a user-facing product page, not just a developer note. Include screenshots under `docs/screenshots/` and embed them with relative Markdown paths. The README should clearly answer:

- What the plugin does in one paragraph.
- What social sources it scans.
- What panel controls do: source dropdown, lookback dropdown, offline checkbox, refresh button.
- What a clicked/expanded player card shows.
- That **all** positive tracked changes are shown, grouped into Skills/Bosses/Activities.
- How WOM tracker periods differ from fallback official-hiscores scan deltas.
- What fallback APIs are checked/planned.
- Build/test and manual RuneLite verification steps.

When screenshots from the live client are unavailable or visually stale, create clear representative sidebar-width PNGs that match the current UI state and labels, then replace them with live RuneLite screenshots before Plugin Hub submission if possible. Do not show real usernames/RSNs in README, Plugin Hub screenshots, public docs, or generated representative screenshots; use synthetic names (`SampleYou`, `Skill Panda`) or blur/anonymize every username before committing. After the user manually edits README/docs, pull first and preserve their edits before further changes. Always verify generated screenshot files open and have sane dimensions, then run `./gradlew clean test assemble --no-daemon --console=plain` before committing docs/assets.

## Tests to add

- Unit-test the gained JSON parser with skills, bosses, and activities.
- Verify names are URL encoded consistently with the links.
- Verify zero-gain periods produce a concise no-gains message.
