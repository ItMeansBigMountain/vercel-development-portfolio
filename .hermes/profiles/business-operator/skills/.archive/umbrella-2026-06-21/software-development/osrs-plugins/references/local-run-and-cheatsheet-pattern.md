# Local RuneLite plugin run + developer cheatsheet pattern

Use this when the user is testing one of the OSRS plugin repos locally or asks how to make every plugin easier to run.

## Fast local run instructions

From an individual plugin repo, not the parent container:

```bash
./gradlew run --no-daemon
```

If Gradle or RuneLite fails because of Java version, set Java 11 explicitly first.

macOS:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH="$JAVA_HOME/bin:$PATH"
java -version
./gradlew run --no-daemon
```

Windows PowerShell:

```powershell
$env:JAVA_HOME="C:\Program Files\Eclipse Adoptium\jdk-11*"
$env:Path="$env:JAVA_HOME\bin;$env:Path"
java -version
.\gradlew.bat run --no-daemon
```

Linux:

```bash
export JAVA_HOME=/path/to/jdk-11
export PATH="$JAVA_HOME/bin:$PATH"
java -version
./gradlew run --no-daemon
```

Expected flow: Gradle launches RuneLite with the plugin injected from the local project. In RuneLite, open the plugin panel and search for the plugin display name. For BossReadinessScore specifically, the historical test entrypoint was `com.itmeansbigmountain.bossreadinessscore.BossReadinessScorePluginTest`.

## Verification commands before telling the user it works

Run from the plugin repo:

```bash
./gradlew test --no-daemon
./gradlew assemble --no-daemon
```

If the user only needs interactive testing and time is short, at minimum verify Java 11 and the `run` task starts.

## Batch developer cheatsheet pattern

When preparing many plugin repos for local testing, add a small `DEVELOPER_CHEATSHEET.md` to each active child plugin repository. Include:

- Java 11 requirement and quick version check.
- `./gradlew test --no-daemon`, `./gradlew assemble --no-daemon`, and `./gradlew run --no-daemon`.
- Windows PowerShell equivalents.
- RuneLite manual test flow: launch, open plugin panel, search plugin name, enable, test core UI/API behavior.
- Common fixes: wrong Java version, wrapper permission, plugin not visible, dependency/download stalls.
- Git/submodule note: child repo changes must be committed and pushed inside the child repo; the parent HeRmEz repo then records updated submodule pointers.

Do not add this to boilerplate/template repos unless the user asks; it is for active testable plugin projects.

## Parent/submodule hygiene

For the user's `/opt/data/HeRmEz/projects/osrs-plugins` workspace, the parent `HeRmEz` repo should point submodules at public absolute GitHub URLs, e.g. `https://github.com/ItMeansBigMountain/<PluginName>.git`, not relative paths that resolve under `HeRmEz.git/projects/...`. Remove dead gitlinks for nonexistent plugin repos rather than leaving broken submodules.
