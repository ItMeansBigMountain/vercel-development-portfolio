# OSRS plugin portfolio review pattern

Use when the user asks to review their RuneLite/OSRS plugin set under `/opt/data/HeRmEz/projects/osrs-plugins`.

## Inventory

Treat `/opt/data/HeRmEz/projects/osrs-plugins` as a container. Child directories with `build.gradle` are individual plugin repos. Exclude `osrs-plugins-boilerplate` from product health summaries unless the user asks about scaffolding.

Useful quick inventory:

```bash
python3 - <<'PY'
from pathlib import Path
root=Path('/opt/data/HeRmEz/projects/osrs-plugins')
for d in sorted(p for p in root.iterdir() if p.is_dir() and (p/'build.gradle').exists()):
    print(d.name)
PY
```

## Build health check

Run each child sequentially, not in parallel, to avoid Gradle lock contention. Use Java 11:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
for d in /opt/data/HeRmEz/projects/osrs-plugins/*; do
  [ -f "$d/build.gradle" ] || continue
  [ "$(basename "$d")" = "osrs-plugins-boilerplate" ] && continue
  (cd "$d" && chmod +x gradlew && ./gradlew clean test assemble --no-daemon --console=plain)
done
```

For a durable report, write JSONL per plugin with: plugin name, return code, build seconds, git dirty count, remote URL, jar path, and log path.

## Product review lens

After technical build health, summarize product maturity, not just compile status:

- Which plugins are already serious side-panel/API products?
- Which are thin MVP/reminder/link wrappers?
- Which repos are superseded by broader product direction?
- Which plugins should be consolidated before publication?

Current user product direction says RivalRadar should absorb/supersede BossKCRivalLookup, BossRaceCreator, SkillNemesis, and SkillRaceCreator unless explicitly revived. BossReadinessScore, AccountLegacyCard/SmartHiscoreLookup, RivalRadar, and clan activity panels are the high-value areas.

## Reporting style

The user prefers concise Discord reports: no giant tables. Give build pass/fail counts, report path, strongest repos, weakest/thinnest repos, and the next concrete product fix.
