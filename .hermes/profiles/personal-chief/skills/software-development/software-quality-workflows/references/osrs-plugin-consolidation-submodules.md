# OSRS RuneLite consolidation and submodule workflow notes

Use these notes when the user is consolidating many standalone RuneLite/OSRS external plugins inside the HeRmEz parent workspace.

## Workflow that worked

1. **Inventory before changing code**
   - For each candidate plugin repo, collect README, `runelite-plugin.properties`, `plugin.json`, main Java source count, test count, and signals such as `HiscoreClient`, `@Subscribe`, `OverlayManager`, `ConfigManager`, `StatChanged`, boss/KC parsers, race/streak/nemesis models.
   - Classify repos as canonical, source-to-absorb, standalone keep, or archive/remove-from-parent.

2. **Document consolidation targets first**
   - Patch canonical child repo READMEs with explicit roadmaps before large code moves.
   - Keep one canonical repo per product family:
     - Account/player intelligence: SmartHiscoreLookup absorbs AccountLegacyCard and NameChangeWatcher concepts.
     - Rival/race/streak/nemesis: RivalRadar absorbs SkillNemesis, SkillRaceCreator, BossRaceCreator, BossKCRivalLookup, BossStreaks, and SkillStreaks concepts.
     - Keep high-value standalone plugins focused: BossReadinessScore, IceBarrageTimer, PersonalProgressTimeline, CompetitionOverlay.

3. **Use TDD for first absorbed modules**
   - Write JVM tests before code for client-free models/services.
   - Good first slices: `PlayerIntelCard`, `NameChangeObservation`, name-normalization, parsers/analyzers/streak trackers.
   - Keep RuneLite client APIs at the edge so core logic is testable without launching a client.

4. **Verify and push child repo before parent**
   - Run Java 11 Gradle checks in the child repo:
     ```bash
     export JAVA_HOME=/opt/data/jdks/current-java11
     export PATH="$JAVA_HOME/bin:$PATH"
     ./gradlew test --no-daemon --console=plain
     ./gradlew assemble --no-daemon --console=plain
     ```
   - Commit/push the child repo using `GITHUB_ACCESS_TOKEN` if `gh` is absent.
   - Verify child local SHA equals `git ls-remote` remote SHA.

5. **Update parent HeRmEz exactly**
   - In `/opt/data/HeRmEz`, stage only the intended submodule pointer paths and docs, e.g.:
     ```bash
     git add projects/osrs-plugins/SmartHiscoreLookup projects/osrs-plugins/OSRS_PLUGIN_CLEANUP_PLAN.md
     git diff --cached --stat
     git diff --cached --check
     ```
   - Commit/push parent after child push is verified.
   - Verify parent local SHA equals remote SHA, then update local `origin/main` if necessary.

## UX/product pitfalls captured

- Default RuneLite sidebar/overlay width is a hard constraint. Avoid wide tabs and oversized dropdowns; use compact dropdowns/icon buttons with explicit preferred/maximum sizing.
- Avoid cross-plugin runtime dependencies during consolidation. Copy or reimplement small UI/model patterns until a shared library is clearly justified.
- Rename product-facing text away from obsolete source repo names when the product direction changes, but remote repo rename can wait.
- For WhosGrindingPanel specifically, remove broken Clan Chat UI/source until a reliable RuneLite API path is confirmed; keep Friends List and Friends Chat working first.
