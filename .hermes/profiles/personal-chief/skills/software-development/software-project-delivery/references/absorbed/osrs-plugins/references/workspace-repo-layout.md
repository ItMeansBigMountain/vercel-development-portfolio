# User workspace RuneLite plugin repo layout

Use this when the user asks to organize, split, standardize, or publish their OSRS/RuneLite plugin projects.

## Canonical local paths

- Main Git-backed workspace: `/opt/data/HeRmEz`
- OSRS plugin parent directory: `/opt/data/HeRmEz/projects/osrs-plugins`
- Boilerplate/reference repo URL: `https://github.com/ItMeansBigMountain/breach-check-osrs.git`
- A cloned copy may exist at `/opt/data/HeRmEz/breach-check-osrs`; verify before assuming.

The user may reference host/container-style paths such as `/docker/hermes-agent-xbit/data/HeRmEz/projects` or `hermes-agent-xbit/data/HeRmEz/projects`. In this Hermes runtime, the corresponding accessible path is normally `/opt/data/HeRmEz/projects`.

## Required workflow for "make each project its own repo"

1. Inspect `/opt/data/HeRmEz/projects/osrs-plugins` first; do not create or initialize repos in the wrong current directory.
2. Treat `osrs-plugins` as a parent folder containing multiple plugin projects, not as one monorepo unless the user explicitly asks.
3. Ignore parent-control or non-project directories such as `.git`, shared `src`, or existing boilerplate directories unless the user says they are standalone plugins.
4. Clone or inspect `breach-check-osrs` and use its full RuneLite Gradle layout as the standard:
   - `build.gradle`
   - `settings.gradle` with the plugin-specific root name
   - `gradle/wrapper/*`
   - `gradlew`, `gradlew.bat`
   - `runelite-plugin.properties`
   - `icon.png` if appropriate
   - `src/main/java/...`
   - `src/test/java/...`
   - `src/test/resources/logback-test.xml`
5. For each plugin directory, create/repair structure, then initialize Git inside that project directory only.
6. Verify with `git -C <plugin> status --short --branch` and, when feasible, a local Gradle build/test before pushing.

## Submodule repair workflow

When `/opt/data/HeRmEz/projects/osrs-plugins` is meant to be usable from another machine, verify the parent repo's `.gitmodules` instead of trusting local nested repo remotes. The parent must reference each child plugin's real GitHub URL, not relative paths such as `./projects/osrs-plugins/AccountLegacyCard`; those resolve from the parent remote into broken URLs like `https://github.com/ItMeansBigMountain/HeRmEz.git/projects/osrs-plugins/AccountLegacyCard`.

Recommended repair sequence:

1. Inventory child repos with `.git`, their `origin` URLs, current branches, and heads.
2. Rewrite `.gitmodules` entries for real plugin repos to their actual GitHub remotes and include `branch = main`.
3. Remove stale gitlinks for empty/non-repo placeholders before syncing, e.g. directories with no `.git`, no Gradle files, and no source.
4. If `projects/plugin-hub` is a gitlink, ensure `.gitmodules` has `https://github.com/ItMeansBigMountain/plugin-hub.git` and its branch is `master` unless the repo changes.
5. Run `git submodule sync --recursive`, remove stale submodule sections from `.git/config`, and verify no `HeRmEz.git/projects` URLs remain.
6. Verify with `git submodule status --recursive`, `git ls-files -s | awk '$1==160000 {print $2, $4}'`, and `git ls-remote --heads` for every `.gitmodules` URL before committing.

## Pitfalls from prior session

- Do not stop after cloning the boilerplate into the session cwd; the actual plugin projects live under `/opt/data/HeRmEz/projects/osrs-plugins`.
- Do not run a blind loop over every child directory without excluding `.git`, shared `src`, or boilerplate folders.
- Do not copy from `/opt/data/HeRmEz/projects/breach-check-osrs` unless verified; the clone may be under `/opt/data/HeRmEz/breach-check-osrs` or absent and need re-cloning.
- If the user says a previous answer was wrong, immediately inspect the corrected path and continue; do not ask whether to execute an obvious filesystem search/inspection step.
- Do not present clone/submodule commands from memory; inspect actual child remotes and `.gitmodules` first because the user tests these plugins locally one by one.
- When repairing OSRS plugin submodules in the parent HeRmEz repo, verify both `.gitmodules` and `.git/config`. Relative URLs such as `./projects/osrs-plugins/<Plugin>` can resolve against the parent GitHub remote into broken URLs like `https://github.com/ItMeansBigMountain/HeRmEz.git/projects/osrs-plugins/<Plugin>`. Replace them with the actual child repo URLs (for example `https://github.com/ItMeansBigMountain/account-legacy-card-osrs.git`) and run `git submodule sync --recursive`.
- Check the root index for stale gitlinks with `git ls-files -s | awk '$1==160000 {print $2, $4}'`. A gitlink without a matching `.gitmodules` entry (observed with `projects/plugin-hub`) breaks `git submodule status --recursive`; either restore the mapping or remove the stale gitlink deliberately.
- Empty placeholder directories under `projects/osrs-plugins` may still appear in `.gitmodules`; confirm a child has `.git`, `build.gradle`, `settings.gradle`, `gradlew`, `runelite-plugin.properties`, and `src/` before listing it as a testable plugin repo.