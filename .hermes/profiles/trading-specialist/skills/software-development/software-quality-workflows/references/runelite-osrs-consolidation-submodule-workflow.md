# RuneLite OSRS plugin consolidation + submodule workflow

Use this when consolidating many small RuneLite/OSRS plugin repos into a smaller canonical set inside a parent workspace repo such as HeRmEz.

## Durable workflow

1. **Choose canonical targets before moving code**
   - Account/player intel features belong in the account-intel canonical repo (for example `SmartHiscoreLookup`).
   - Rival/race/streak/nemesis features belong in the rival/competition canonical repo (for example `RivalRadar`).
   - Keep genuinely standalone products separate: boss readiness/gear, PvP timers, personal progress timelines, and large future overlays.

2. **Absorb one feature family at a time with TDD**
   - Write a failing JVM test in the canonical repo first.
   - Port the smallest pure-Java model/service from the retired repo.
   - Keep it RuneLite-free when possible so tests do not require launching a client.
   - Only after the pure model is green should RuneLite event/config wiring be added.

3. **Keep cross-plugin dependencies out**
   - Do not make standalone plugins depend on each other at runtime.
   - Copy or mirror small UX/model patterns across repos until a shared library is clearly justified.
   - For UI patterns, preserve RuneLite default sidebar width: compact controls, explicit preferred/maximum sizes, and no wide tabs/rows that trail off-screen.

4. **Verify child repo first**
   - Use Java 11 for RuneLite plugin builds.
   - Run at minimum:
     ```bash
     export JAVA_HOME=/opt/data/jdks/current-java11
     export PATH="$JAVA_HOME/bin:$PATH"
     ./gradlew test --no-daemon --console=plain
     ./gradlew assemble --no-daemon --console=plain
     ```
   - Commit and push the child repo before touching the parent submodule pointer.

5. **Update parent workspace second**
   - In the parent repo, stage only exact OSRS paths/submodule pointers. Do not sweep unrelated dirty files.
   - Inspect the submodule diff:
     ```bash
     git diff --submodule=log -- projects/osrs-plugins/<PluginName>
     ```
   - Commit only the changed pointer and any OSRS cleanup docs.
   - Push parent and verify remote/local SHA match.

## Authenticated GitHub push pattern

When `gh` is unavailable, use `GITHUB_ACCESS_TOKEN`. Avoid logging the token. A robust pattern is to construct the authenticated URL inside a short script and pass it directly to `git push`/`git ls-remote`:

```python
import os, subprocess
remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
url = 'https://x-access-token:' + os.environ['GITHUB_ACCESS_TOKEN'] + '@github.com/' + remote.split('github.com/', 1)[1]
subprocess.check_call(['git', 'push', url, 'main'])
remote_sha = subprocess.check_output(['git', 'ls-remote', url, 'refs/heads/main'], text=True).split()[0]
local_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert remote_sha == local_sha
```

## Common consolidation sequence

- `SmartHiscoreLookup` absorbs:
  - account card/local account summary models
  - hiscore link helpers
  - previous/current name observation from friends/friends-chat data
- `RivalRadar` absorbs:
  - skill nemesis analyzer
  - skill streak tracker
  - boss streak parser/tracker
  - skill/boss race target models
  - optional background-safe hiscore/Wise Old Man comparisons

## Pitfalls

- Do not begin by wiring RuneLite events; start with testable pure-Java models/services.
- Do not stage unrelated parent workspace dirt while updating submodule pointers.
- Do not claim a parent clone is ready until child commits are pushed and the parent pointer is pushed.
- Do not preserve broken product labels from retired repos when the product direction changed; update README, `plugin.json`, `runelite-plugin.properties`, and `@PluginDescriptor` together.
- Avoid shell snippets that expose or badly quote `GITHUB_ACCESS_TOKEN`; use Python subprocess or carefully quoted bash and verify without printing credentials.
