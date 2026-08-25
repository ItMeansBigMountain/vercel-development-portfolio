# OSRS consolidation implementation notes

Session-derived notes for continuing the user's RuneLite plugin portfolio consolidation.

## Confirmed sequence

1. Fix and push the focused child plugin repo first.
2. Run Java 11 Gradle verification in the child repo:
   ```bash
   export JAVA_HOME=/opt/data/jdks/current-java11
   export PATH="$JAVA_HOME/bin:$PATH"
   ./gradlew test --no-daemon --console=plain
   ./gradlew assemble --no-daemon --console=plain
   ```
3. Commit and push the child repo, then verify local and remote SHAs match.
4. Only then update the `/opt/data/HeRmEz` parent submodule pointer and push parent.
5. Stage exact OSRS paths only; leave unrelated parent dirt alone.

## TDD pattern that worked

For consolidation modules, add a pure Java service/model first, with JVM tests that do not require launching RuneLite. Watch the test fail on missing classes/methods, then implement the minimal code.

Implemented successfully this way:

- `SmartHiscoreLookup`
  - `PlayerIntelCard`
  - `NameChangeObservation`
  - `NameChangeObservationService`
  - login-time local account intel card
  - friends/friends-chat name-change scanning using RuneLite `Nameable#getPrevName`
- `RivalRadar`
  - `SkillNemesisAnalyzer` / `SkillNemesisAnalysis`
  - `SkillStreakTracker` / `SkillStreakUpdate`

Next compatible module: `BossStreakTracker` as a pure parser/tracker before wiring RuneLite events.

## RuneLite API checks used

Use `javap` against cached RuneLite jars before wiring social APIs:

```bash
API=$(find /opt/data/.gradle/caches/modules-2/files-2.1/net.runelite/runelite-api -type f -name 'runelite-api-*.jar' | sort | tail -1)
javap -classpath "$API" net.runelite.api.Nameable
javap -classpath "$API" net.runelite.api.FriendContainer
javap -classpath "$API" net.runelite.api.FriendsChatManager
```

Observed useful signatures:

- `Nameable#getName()`
- `Nameable#getPrevName()`
- `Client#getFriendContainer()`
- `Client#getFriendsChatManager()`
- `Client#getTotalLevel()`
- `Player#getCombatLevel()`

## Authenticated push pitfall

Avoid hand-building token URLs inside nested single-quoted shell/Python snippets; it caused repeated quoting syntax errors. Prefer a simple Python snippet with double quotes/f-string, or a shell parameter expansion without nested quoting.

Safe Python shape:

```python
import os, subprocess
remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
token = os.environ['GITHUB_ACCESS_TOKEN']
url = f"https://x-access-token:{token}@github.com/" + remote.split('github.com/', 1)[1]
subprocess.check_call(['git', 'push', url, 'main'])
remote_sha = subprocess.check_output(['git', 'ls-remote', url, 'refs/heads/main'], text=True).split()[0]
local_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert remote_sha == local_sha
```
