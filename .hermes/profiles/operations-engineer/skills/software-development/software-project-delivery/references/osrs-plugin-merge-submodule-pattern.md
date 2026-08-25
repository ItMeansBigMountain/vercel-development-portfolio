# OSRS/RuneLite plugin merge + submodule pattern

Use when two OSRS/RuneLite plugin repos under a parent portfolio seem like one product and the user asks whether to merge them.

## Decision pattern

1. Inspect both child repos first:
   - `git -C <repo> status --short`
   - `git -C <repo> log --oneline -5`
   - `find <repo> -maxdepth 4 -type f \( -name '*.java' -o -name 'build.gradle' -o -name 'settings.gradle' -o -name 'README.md' -o -name 'plugin.json' -o -name 'runelite-plugin.properties' \)`
2. In the parent repo, check whether the plugin folders are submodules:
   - `git ls-files -s projects/osrs-plugins/<PluginA> projects/osrs-plugins/<PluginB>`
   - Mode `160000` means submodule/gitlink.
   - `git submodule status --recursive` and `.gitmodules` reveal each child remote.
3. Prefer one canonical plugin repo when the UX is a single side panel/overlay and the second repo is really a model/view inside it.
4. Preserve the old child repo untouched until the merged target builds and the user approves archival/removal. Do not delete submodules as part of the code merge unless explicitly asked.

## Safe merge shape

- Pick the repo whose plugin identity should survive as the target (display name, package, plugin-hub submission path).
- Copy reusable code from the source repo into the target package rather than keeping two plugin descriptors.
- Merge config options into the target config with positions/ranges.
- Update `plugin.json`, `runelite-plugin.properties`, and `README.md` to describe the merged product and mention the folded source repo.
- Add tests for the copied pure-Java helpers in the target package.
- Keep one `PluginDescriptor` / `plugins=` entry unless deliberately shipping multiple plugins from one repo.

## Verification

Use Java 11 for RuneLite compatibility:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon
```

Report the real Gradle result. If it passes, report the changed target repo and that the old submodule remains untouched/archival until the next explicit step.

## Parent repo/submodule follow-up

After target child repo changes are committed/pushed, the parent repo will show the child submodule as modified (`m path/to/submodule`). Commit the updated submodule pointer in the parent only after the child push succeeds.

If deprecating/removing the source plugin submodule later:

1. Confirm with the user.
2. Add archival/deprecation note in the source repo or parent tracker.
3. Remove from `.gitmodules`, remove the gitlink, and clean `.git/modules/...` only after confirming no useful unmerged changes remain.
4. Update plugin-hub direction to point only at the merged target plugin.

## Pitfalls

- A normal `git pull` of the parent repo does not populate submodule contents. Users need `git submodule update --init --recursive` or clone with `--recurse-submodules`.
- Do not call the parent repo fully updated until child submodule commits are pushed and the parent gitlink points at the desired commit.
- Do not preserve two plugin descriptors just because two repos existed; Plugin Hub usually wants the product identity to be clear and narrow.
- Avoid copying build outputs (`build/`, `.gradle/`) or generated files between plugin repos.
