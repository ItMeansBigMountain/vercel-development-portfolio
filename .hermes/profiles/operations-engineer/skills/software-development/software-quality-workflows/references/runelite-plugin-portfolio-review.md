# RuneLite / OSRS external plugin portfolio review pattern

Use this when reviewing a directory of many standalone RuneLite external plugin repos, especially OSRS Plugin Hub candidates.

## Evidence to collect

1. Locate the plugin root(s) and repo inventory/tracker if present.
2. For each plugin repo, collect:
   - `git branch --show-current`, `git remote get-url origin`, `git status --short`
   - presence of `README.md`, `build.gradle`, `settings.gradle`, `runelite-plugin.properties`
   - Java source counts under `src/main` and `src/test`, excluding `.git`, `.gradle`, `.gradle-user-home`, `build`, and `target`
   - Plugin Hub metadata from `runelite-plugin.properties`: `displayName`, `author`, `support`, `description`, `tags`, `plugins`
   - feature signals from Java: `@Subscribe`, `OverlayManager`, `HiscoreClient`, `ConfigManager`, `OkHttpClient`/`HttpUrl`, parser/formatter classes
   - maturity signals: TODO/FIXME/placeholder/scaffold/future language in source + README
3. Run real verification per plugin: `./gradlew test --no-daemon --console=plain`.
   - Use a timeout per repo and summarize pass/fail plus actionable warning patterns.
   - Common non-blocking warnings: Gradle deprecation warnings, unchecked test launcher operations, deprecated RuneLite API use.

## Review framing

Rank plugins by product readiness, not just build success:

- **Flagship candidates**: differentiated player-facing loop, non-trivial implementation, tests, clear docs.
- **Quick wins**: focused utility, low external API risk, clean tests, easy screenshots/demo.
- **Thin/scaffold MVPs**: compile and have metadata, but mostly reminders/placeholders/config shells.
- **Consolidation candidates**: multiple small plugins in the same product family.

OSRS plugin families that commonly consolidate well:

- Rival/hiscore: rival radar, boss KC lookup, smart hiscore lookup.
- Clan activity: clan grind heatmap, who-is-grinding panel, group progress board.
- Race/competition: boss race creator, skill race creator, competition overlay.

## Recommended output shape

1. Start with verification summary: count of plugins tested, command used, pass/fail count, repo cleanliness.
2. Give an executive ranking: strongest, thin/scaffold, biggest issue.
3. Include a compact table: plugin, main Java files, tests, build status, notes.
4. Review each plugin with: status, strengths, risks/gaps, recommendation, next work.
5. End with portfolio-level issues and a recommended build order.

## Pitfalls

- Do not treat passing Gradle tests as Plugin Hub readiness; RuneLite plugins also need manual client smoke tests.
- Do not let names/descriptions overpromise; call out `Creator`, `Panel`, or `Overlay` names that are mostly shells.
- Ignore generated/build/cache Java counts; `.gradle-user-home` and `build/generated` can wildly inflate source counts.
- Check README/product promise against code signals, especially local-only claims vs network/API imports.
- Prefer polishing 2-3 publishable plugins before trying to advance a large flat portfolio of thin repos.
