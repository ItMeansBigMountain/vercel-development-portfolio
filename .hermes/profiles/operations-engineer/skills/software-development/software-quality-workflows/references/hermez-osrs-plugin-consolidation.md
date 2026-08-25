# HeRmEz OSRS plugin consolidation workflow

Use this reference when working on the user's RuneLite/OSRS plugin portfolio under `/opt/data/HeRmEz/projects/osrs-plugins`.

## Canonical repo strategy

Active default OSRS submodules should stay narrow and canonical:

- `WhosGrindingClanPanel` / product name `Who's Grinding Panel`: friends/friends-chat social activity, compact row icons, click-to-detail tracker scaffolding. Avoid clan-first UI unless explicitly revived.
- `SmartHiscoreLookup`: canonical account/player intelligence. Absorb AccountLegacyCard and NameChangeWatcher concepts here.
- `RivalRadar`: canonical rival/race/streak/nemesis hub. Absorb SkillNemesis, SkillRaceCreator, BossRaceCreator, BossKCRivalLookup, BossStreaks, and SkillStreaks concepts here.
- Keep standalone unless user changes direction: `BossReadinessScore`, `IceBarrageTimer`, `PersonalProgressTimeline`, `CompetitionOverlay`.
- `_templates/osrs-plugins-boilerplate` is a template, not an active product plugin.

## Required workflow

1. Work in the child repo first.
2. Use TDD for new behavior: write a failing JVM test, watch it fail, implement minimal code, then rerun tests.
3. Build/test the child repo with Java 11:
   ```bash
   export JAVA_HOME=/opt/data/jdks/current-java11
   export PATH="$JAVA_HOME/bin:$PATH"
   ./gradlew test --no-daemon --console=plain
   ./gradlew assemble --no-daemon --console=plain
   ```
4. Commit and push the child repo before touching the parent pointer.
5. In `/opt/data/HeRmEz`, stage only exact OSRS paths/submodule pointers. Do not stage unrelated automation/video/trading dirt.
6. Commit and push the parent repo. Verify local and remote SHAs match.
7. Report pull commands for the user:
   ```bat
   cd C:\Users\faree\Desktop\HeRmEz
   git pull origin main
   git submodule sync --recursive
   git submodule update --init --recursive
   ```

## Auth and push pattern

Use `GITHUB_ACCESS_TOKEN` for authenticated GitHub operations. `gh` may be absent; do not conclude GitHub auth is unavailable until the token-backed API/git fallback has been tried.

For shell pushes, prefer a local variable or Python wrapper that constructs the token URL without printing the token. Beware malformed quoting around `${GITHUB_ACCESS_TOKEN}` in heredocs or Python snippets; verify with `git ls-remote` after push.

## Common pitfalls

- A parent `git status` may show lots of unrelated dirty files. Stage exact OSRS paths only.
- Child submodule commits must be pushed before parent pointer updates, otherwise the user's fresh clone cannot resolve the submodule commit.
- Keep RuneLite side panels within default sidebar width; avoid wide tabs/dropdowns and explicitly set preferred/maximum sizes for Swing controls.
- Do not add cross-plugin runtime dependencies just to share small UI/detail patterns. Copy or reimplement small models until a shared library is intentionally designed.
- Treat recursive submodule errors from non-OSRS paths, such as `projects/viral-clip-radar`, as a separate parent hygiene task unless the user asks to fix it now.
