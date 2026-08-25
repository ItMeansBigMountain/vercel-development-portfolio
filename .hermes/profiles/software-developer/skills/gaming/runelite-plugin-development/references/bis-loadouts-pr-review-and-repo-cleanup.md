# BIS Loadouts PR-review move and OSRS repo cleanup lessons

Use this when finalizing BIS Loadouts or doing OSRS plugin lifecycle/GitHub cleanup.

## BIS Loadouts canonical state

- Display/project name: `BIS Loadouts`.
- Child repo: `ItMeansBigMountain/bis-loadouts-osrs`.
- Java package: `com.itmeansbigmountain.bisloadouts`.
- Main class: `BisLoadoutsPlugin`.
- Config group: `bisloadouts`.
- Current HeRmEz lifecycle path: `/opt/data/HeRmEz/projects/osrs-plugins/pr-review-pending/BisLoadouts`.

## PR-ready documentation pattern

Before moving an OSRS plugin from `in-progress/` to `pr-review-pending/`:

1. Rewrite `README.md` around the current product name and actual behavior, not stale prototype language.
2. Include: features, configuration, privacy/network usage, local development commands, manual RuneLite test checklist, Plugin Hub readiness notes, and future scope limits.
3. Add `docs/plugin-hub-pr-readiness.md` with repo metadata, required local checks, manual UI smoke test, public API/privacy notes, and intentional scope limits.
4. Update developer cheatsheets to the lifecycle path that the user will actually pull locally.
5. Run Java 11 validation from the child repo:
   ```bash
   export JAVA_HOME=/opt/data/jdks/current-java11
   export PATH="$JAVA_HOME/bin:$PATH"
   ./gradlew clean test assemble --no-daemon --console=plain
   ```
6. Commit and push the child repo, verify local/remote SHA, then move the submodule path in the HeRmEz parent with `git mv`, update `.gitmodules`, stage exact paths, commit, and push.

## Windows handoff after lifecycle move

After a plugin moves buckets, tell the user to pull the parent and update the new path-scoped submodule:

```powershell
cd C:\Users\faree\Desktop\HeRmEz
git pull origin main
git submodule sync --recursive
git submodule update --init --recursive .\projects\osrs-plugins\pr-review-pending\BisLoadouts
```

If the old lifecycle folder remains locally, remove it only after the pull succeeds:

```powershell
Remove-Item -Recurse -Force .\projects\osrs-plugins\in-progress\BisLoadouts
```

## GitHub repo cleanup pattern

When the user asks to delete unused OSRS plugin repos:

1. List all GitHub repos that look OSRS/RuneLite/plugin-related.
2. Compare against the active local HeRmEz lifecycle directories and `.gitmodules` mappings.
3. Present explicit keep/delete candidate lists.
4. Ask for final confirmation before destructive deletion.
5. Delete by exact repo names only.
6. Verify each deleted repo returns 404/gone.
7. Re-scan remaining OSRS/plugin repos and update the OSRS cleanup plan.

Do not archive/delete `plugin-hub`, active lifecycle repos, or `_templates/osrs-plugins-boilerplate` unless the user explicitly asks for those exact repos.
