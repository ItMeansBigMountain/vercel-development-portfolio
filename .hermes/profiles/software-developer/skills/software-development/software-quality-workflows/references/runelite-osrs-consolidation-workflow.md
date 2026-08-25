# RuneLite / OSRS plugin consolidation workflow

Use this reference when the user is consolidating multiple standalone RuneLite plugin repos inside the HeRmEz workspace.

## Sequence that worked

1. **Start from product decisions**
   - Identify canonical repos and retired/source repos.
   - Capture explicit keep/merge/standalone decisions in `projects/osrs-plugins/OSRS_PLUGIN_CLEANUP_PLAN.md`.
   - For this user's current OSRS direction:
     - `WhosGrindingPanel` stays standalone and should avoid cross-plugin runtime deps.
     - `SmartHiscoreLookup` is canonical for account/player intel; absorb AccountLegacyCard and NameChangeWatcher concepts.
     - `RivalRadar` is canonical for rivals/races/streaks/nemesis; absorb skill/boss race and streak concepts.
     - Keep `BossReadinessScore`, `IceBarrageTimer`, `PersonalProgressTimeline`, and `CompetitionOverlay` standalone.

2. **Document consolidation targets before large code moves**
   - Update the canonical child repo README with source repos/features to absorb.
   - Add a concrete target backlog and acceptance checks.
   - Update the parent OSRS cleanup plan with implementation order.

3. **Implement one feature slice at a time using TDD**
   - Write client-free JVM tests first for parser/model/service logic.
   - Verify RED failure.
   - Add minimal production code.
   - Run targeted tests, then `./gradlew test assemble --no-daemon --console=plain`.

4. **Push child repos before parent pointers**
   - In the child repo: commit, push with `GITHUB_ACCESS_TOKEN`, verify remote SHA equals local SHA.
   - In `/opt/data/HeRmEz`: stage only the submodule path plus intentional OSRS docs; never broad-add the dirty control repo.
   - Commit/push parent, verify remote SHA equals local SHA.

## Useful implementation slices

### SmartHiscoreLookup account-intel merge

- First slice: `PlayerIntelCard` model + `NameChangeObservationService` with offline tests.
- Second slice: plugin login behavior builds a local account card from RuneLite `Player#getCombatLevel()` and `Client#getTotalLevel()` and emits a compact summary plus hiscore URL.
- Later slice: scan friends/friends-chat previous names using RuneLite `Nameable#getPrevName`, record unique `previous -> current` pairs, and optionally summarize them in chat or a compact panel.

### WhosGrindingPanel stabilization

- Remove broken/unreliable clan source from the visible UI until it is proven.
- Keep `Friends List` and `Friends Chat` sources.
- `showOfflineFriends()` gates offline friends from `client.getFriendContainer()`.
- Sidebar width is a hard requirement: compact dropdown/icon controls, no wide tabs, and explicit preferred/max sizing for Swing controls.

### RivalRadar consolidation

- Start with local non-network modules: skill nemesis analyzer, skill streak tracker, boss KC parser/streak tracker.
- Add race setup/progress models next.
- Add hiscore/Wise Old Man comparisons last, backgrounded and cached.

## Verification checklist

- Child repo `git status --short` is clean after push.
- Child remote SHA equals local `HEAD`.
- Parent stages exact OSRS paths only.
- Parent remote SHA equals local `HEAD`.
- User pull instructions include:
  ```bat
  git pull origin main
  git submodule sync --recursive
  git submodule update --init --recursive
  ```

## Pitfalls

- Do not treat passing Gradle tests as Plugin Hub readiness; still need manual RuneLite smoke tests and screenshots/GIFs later.
- Do not introduce cross-plugin runtime dependencies for small shared UX patterns; duplicate/adapt a small model or pattern until a shared library is clearly justified.
- Do not stage unrelated dirty HeRmEz files from automation/video/trading work while updating OSRS submodules.
- Avoid session-specific remote renames during consolidation; product display names can change before GitHub repo names are renamed deliberately.
