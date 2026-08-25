# OSRS/RuneLite plugin consolidation and parent submodule update

Use when the user decides two RuneLite plugin ideas should become one plugin/repo inside the HeRmEz portfolio, especially under `projects/osrs-plugins/`.

## Target shape

- Keep the **product** as one RuneLite external plugin repo when the ideas are really one user workflow (for example a clan activity panel plus a clan activity heatmap).
- Fold secondary concepts into the main plugin as models/views/config sections, not a second Plugin Hub submission.
- Keep the old repo untouched until the merged target builds and tests.

## Recommended sequence

1. Inspect both child repos:

```bash
for d in PrimaryPlugin SecondaryPlugin; do
  git -C "$d" status --short
  git -C "$d" log --oneline -5
  find "$d" -maxdepth 4 -type f \( -name '*.java' -o -name 'README.md' -o -name 'build.gradle' -o -name 'plugin.json' -o -name 'runelite-plugin.properties' \) | sort
 done
```

2. Choose the primary repo based on the broader product UX/name. For clan features, prefer the side-panel repo as the primary and fold heatmap/stat helpers into it.

3. Move/copy reusable Java code into the primary package namespace rather than preserving a second plugin package. Add tests for the copied model/helper behavior.

4. Update the primary plugin metadata and README:
   - One display name / `PluginDescriptor`.
   - Broaden tags/descriptions to cover the merged concept.
   - Document that the secondary repo is folded into the primary repo.
   - Note future external API work (Wise Old Man / TempleOSRS) as background/cached, not game-thread blocking.

5. If the user wants local RuneLite testing, add a visible panel scaffold early:
   - `ClientToolbar` + `NavigationButton` in the plugin startup/shutdown.
   - A `PluginPanel` subclass with placeholder/sample rows and data-status copy.
   - Keep live clan/WOM/Temple calls unwired until background/caching is designed.

6. Verify the child repo before touching the parent:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon
```

7. Commit and push the primary child repo first.

8. In the parent `HeRmEz` repo, remove the obsolete secondary submodule and stage the updated primary submodule pointer:

```bash
git submodule deinit -f projects/osrs-plugins/SecondaryPlugin || true
git rm -f projects/osrs-plugins/SecondaryPlugin
rm -rf .git/modules/projects/osrs-plugins/SecondaryPlugin
git add .gitmodules projects/osrs-plugins/PrimaryPlugin
git commit -m "Merge secondary plugin into primary plugin submodule"
git push origin main
```

## Windows/local handoff commands

After child and parent pushes, tell the user to update local HeRmEz from the parent root:

```powershell
cd C:\Users\faree\Desktop\HeRmEz
git pull
git submodule sync --recursive
git submodule update --init --recursive projects/osrs-plugins/PrimaryPlugin
```

If the old directory remains locally after the parent removes the submodule:

```powershell
rmdir /s /q projects\osrs-plugins\SecondaryPlugin
```

Then run locally:

```powershell
cd C:\Users\faree\Desktop\HeRmEz\projects\osrs-plugins\PrimaryPlugin
.\gradlew.bat clean test assemble --no-daemon
.\gradlew.bat run --no-daemon
```

## Pitfalls

- Do not only commit parent `.gitmodules` changes; submodule users need the child repo commit pushed first.
- Do not delete/archive the old child repo until the merged child builds.
- Do not leave two Plugin Hub submissions if the product direction is one UI/workflow.
- A normal `git pull` does not populate or update child repo contents; users need `git submodule update --init --recursive` from the parent checkout.
- Avoid capturing local credential/push failures as durable constraints; just provide the child-first/parent-second push sequence and handoff commands.
