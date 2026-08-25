# RuneLite plugin repo stabilization checklist

Use this when an `osrs-plugins` parent directory contains many plugin folders that need to be made clean, independent RuneLite plugin repositories without polluting the parent workspace backup.

## Target state

- The parent `osrs-plugins/` directory is **not** a Git repository unless the user explicitly asks for a monorepo.
- Each plugin child directory is its own independent Git repo on a normal branch such as `main`.
- The parent Git-backed workspace ignores plugin internals so nested repo contents are not accidentally tracked or backed up as ordinary files.
- Each plugin follows the `breach-check-osrs` Gradle/RuneLite structure.

## Stabilization workflow

1. Confirm the real workspace path first, usually `/opt/data/HeRmEz/projects/osrs-plugins`.
2. Inspect the parent for accidental monorepo artifacts:
   - parent `.git/`
   - parent `src/`
   - parent `settings.gradle`
   - boilerplate clones that accidentally contain copied plugin folders
3. Preserve before deleting. Move accidental parent Git metadata or large mistaken trees into `/opt/data/HeRmEz/projects/_backups/...` or create a Git bundle when the source is a repo.
4. Use `breach-check-osrs` as the template for shared Gradle files:
   - `build.gradle`
   - `settings.gradle` with the child plugin name as `rootProject.name`
   - `gradle/wrapper/*`
   - executable `gradlew`
   - `gradlew.bat`
   - `runelite-plugin.properties`
   - `src/test/resources/logback-test.xml`
5. For each actual plugin child directory:
   - skip `.git`, `_backups`, parent-control folders, and boilerplate-only folders unless the user wants them as plugins
   - create missing `src/main/java`, `src/test/java`, and test resources
   - initialize Git **inside that child directory only**
   - set or rename the primary branch to `main`
   - make an initial commit after tests pass
6. Add or update a parent-level ignore file so the main workspace repo does not track every nested repo file. Prefer ignoring plugin child contents while allowing parent docs/control files to be tracked.
7. Verify every plugin independently:
   - `git -C <plugin> status --short --branch`
   - `./gradlew test --no-daemon -q` from inside the plugin directory when feasible
8. Verify the parent workspace is clean and only contains intentional control files such as README or ignore rules.

## Parent ignore pattern example

Use a parent `.gitignore` pattern like this when `osrs-plugins/` lives inside a larger Git-backed workspace:

```gitignore
# Child directories are independent plugin repositories.
/*/

# Keep parent-level docs/control files trackable.
!/.gitignore
!/README.md
```

If the parent directory contains support folders that should remain tracked, add explicit `!/<folder>/` exceptions.

## Common pitfalls

- Do not clone `breach-check-osrs` and stop; the user wants all existing plugin folders standardized, not just a boilerplate checkout.
- Do not make the parent `osrs-plugins/` a monorepo by default. The user's preferred shape is independent repos per plugin.
- Do not use Git submodules unless the user explicitly asks; they add complexity and do not match the preferred workflow.
- Do not let the parent workspace backup capture nested plugin internals as ordinary files.
- Do not run bulk loops over every child without exclusions; boilerplate clones and backup folders can look like projects.
- When fixing compile errors during migration, keep changes scoped to the plugin that fails, then rerun that plugin's Gradle test before counting it as stabilized.
