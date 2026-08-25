# OSRS plugin submodule merge workflow

Use when the user decides two RuneLite/OSRS plugin repos under `projects/osrs-plugins/` should become one plugin/repo, especially inside the HeRmEz parent workspace where each plugin is a Git submodule.

## Decision pattern

Prefer merging into the plugin whose UX should remain visible to RuneLite/plugin-hub users. Treat the other repo as an internal model/view/source package unless there is a clear reason for separate plugin-hub submissions.

Example from session: `ClanGrindHeatmap` became internal heatmap model/config inside `WhosGrindingClanPanel`, because "who is grinding" and "when the clan grinds" are one clan activity panel experience.

## Safe sequence

1. Inspect both child repos before editing:

```bash
for d in WhosGrindingClanPanel ClanGrindHeatmap; do
  git -C projects/osrs-plugins/$d status --short
  git -C projects/osrs-plugins/$d log --oneline -5
  find projects/osrs-plugins/$d -maxdepth 4 -type f \
    \( -name '*.java' -o -name 'build.gradle' -o -name 'settings.gradle' -o -name 'README.md' -o -name 'plugin.json' -o -name 'runelite-plugin.properties' \) | sort
done
```

2. Merge functionality into the target child repo, preserving package naming under the target plugin package. Do not keep two plugin descriptors/classes registered unless the intent is genuinely two plugins.

3. Update target metadata together:

- `README.md`
- `plugin.json`
- `runelite-plugin.properties`
- config names/ranges
- tests for moved pure-Java helpers

4. Verify the child repo with Java 11:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon
```

5. Commit and push the target child repo first:

```bash
git -C projects/osrs-plugins/WhosGrindingClanPanel add .
git -C projects/osrs-plugins/WhosGrindingClanPanel commit -m "Merge clan grind heatmap into clan panel"
git -C projects/osrs-plugins/WhosGrindingClanPanel push origin main
```

6. Only after the child push succeeds, update the parent HeRmEz repo to point at the new child commit and remove the obsolete submodule:

```bash
git submodule deinit -f projects/osrs-plugins/ClanGrindHeatmap || true
git rm -f projects/osrs-plugins/ClanGrindHeatmap
rm -rf .git/modules/projects/osrs-plugins/ClanGrindHeatmap
git add .gitmodules projects/osrs-plugins/WhosGrindingClanPanel
git commit -m "Merge clan heatmap into clan panel submodule"
git push origin main
```

## Windows pull/update command for the user

After both pushes are on GitHub, tell the user to run from the HeRmEz root:

```powershell
cd C:\Users\faree\Desktop\HeRmEz
git pull
git submodule sync --recursive
git submodule update --init --recursive projects/osrs-plugins/WhosGrindingClanPanel
rmdir /s /q projects\osrs-plugins\ClanGrindHeatmap
```

If the user just cloned the parent repo and submodule folders look empty, explain that the OSRS plugins are submodules; use:

```powershell
git submodule update --init --recursive projects/osrs-plugins/WhosGrindingClanPanel
```

## Pitfalls

- Do not tell the user `git pull` alone will populate submodule contents. It updates parent gitlinks, not child worktrees.
- Do not remove the old submodule from the parent before the target child repo commit has been pushed; otherwise other machines may point at a child commit that only exists locally.
- Do not preserve the old plugin as a second registered RuneLite plugin unless the user wants two plugin-hub submissions.
- Keep old repo deletion/archive as a parent/submodule decision, not just local folder deletion.
- If push credentials are missing on the agent host, report that the local commits exist and give the user the exact push/pull sequence; do not claim the HeRmEz GitHub repo has the update.
