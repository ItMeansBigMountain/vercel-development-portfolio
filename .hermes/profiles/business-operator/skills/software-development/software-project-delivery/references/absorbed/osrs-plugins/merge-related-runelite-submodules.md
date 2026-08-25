# Merging related RuneLite plugin repos under the HeRmEz OSRS portfolio

Use when the user decides two OSRS/RuneLite plugin ideas should become one product/repo, especially when both live as Git submodules under `projects/osrs-plugins/`.

## Recommended shape

- Pick one child repo as the canonical plugin repo. Prefer the repo whose UX/product concept should remain visible in RuneLite/plugin-hub.
- Move the other plugin's reusable code into the canonical package as a model/helper/view, not as a second plugin descriptor, unless the user explicitly wants two plugin entries.
- Update the canonical repo metadata in all three places:
  - `@PluginDescriptor`
  - `plugin.json`
  - `runelite-plugin.properties`
- Update README with a short "merged repo decision" section so future agents do not resurrect the archived repo by accident.

## Safe command sequence

1. In the child canonical repo, implement the merge.
2. Run Java 11 verification:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon
```

3. Commit and push the child repo first:

```bash
git add .
git commit -m "Merge <old plugin> into <canonical plugin>"
git push origin main
```

4. In the parent `HeRmEz` repo, remove the obsolete submodule and stage the canonical submodule pointer:

```bash
cd /opt/data/HeRmEz
git submodule deinit -f projects/osrs-plugins/<ObsoletePlugin> || true
git rm -f projects/osrs-plugins/<ObsoletePlugin>
rm -rf .git/modules/projects/osrs-plugins/<ObsoletePlugin>
git add .gitmodules projects/osrs-plugins/<CanonicalPlugin>
git commit -m "Merge <old plugin> into <canonical plugin> submodule"
git push origin main
```

If the parent worktree has unrelated dirty files or remote advanced, use a clean worktree to cherry-pick the parent submodule-pointer commit instead of rebasing over unrelated runtime changes:

```bash
git fetch origin main
git worktree add /tmp/hermez-push-worktree origin/main
cd /tmp/hermez-push-worktree
git cherry-pick <parent-merge-commit>
git push origin HEAD:main
cd /opt/data/HeRmEz
git worktree remove /tmp/hermez-push-worktree --force
```

## Windows user pull commands

After both child and parent are pushed, tell the user to run from `C:\Users\faree\Desktop\HeRmEz`:

```powershell
git pull
git submodule sync --recursive
git submodule update --init --recursive projects/osrs-plugins/<CanonicalPlugin>
```

If the obsolete folder remains locally:

```powershell
rmdir /s /q projects\osrs-plugins\<ObsoletePlugin>
```

Then run the plugin locally:

```powershell
cd C:\Users\faree\Desktop\HeRmEz\projects\osrs-plugins\<CanonicalPlugin>
git pull
.\gradlew.bat clean test assemble --no-daemon
.\gradlew.bat run --no-daemon
```

## Pitfalls

- Do not only edit `.gitmodules`; use `git rm` so the parent records deletion of the `160000` gitlink.
- Do not push the parent before pushing the child commit; the parent pointer may reference an unreachable child commit for the user.
- If GitHub credentials fail inside the normal session, try the configured user home for credential-store setups, e.g. `HOME=/opt/data git push ...`, before declaring a blocker.
- Avoid deleting the old child GitHub repo immediately. Removing the parent submodule is enough to give the user one active repo while preserving old history remotely.
