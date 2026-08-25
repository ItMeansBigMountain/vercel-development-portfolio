# Bulk publishing RuneLite plugin child repos

Use this reference when `/opt/data/HeRmEz/projects/osrs-plugins` already contains many buildable child plugin directories and the user asks to complete/push each plugin to its own GitHub repository.

## Safe sequence

1. Inventory only real plugin child directories under `/opt/data/HeRmEz/projects/osrs-plugins`.
   - Include directories with `build.gradle`, `gradlew`, `settings.gradle`, `src/`, and an inner `.git/` when present.
   - Exclude parent/control/template directories by exact name or path, especially `.git`, `_backups`, `breach-check-osrs`, and `osrs-plugins-boilerplate`, unless the user explicitly asks to publish the template too.
2. Process one child at a time:
   - `chmod +x gradlew`
   - `./gradlew clean test --no-daemon`
   - inspect `git status --short --branch`
   - stage only source/docs/metadata files (`README.md`, `build.gradle`, `plugin.json`, `runelite-plugin.properties`, `src/`) rather than caches/build outputs
   - commit any remaining completion work with a conventional message
3. Create the GitHub repository using the available token. In this environment the token may be named `GITHUB_ACCESS_TOKEN`, not only `GITHUB_TOKEN`/`GH_TOKEN`.
4. Push with a temporary token-bearing HTTPS remote, then immediately sanitize the local remote URL:
   - add/push: `https://x-access-token:<token>@github.com/<owner>/<repo>.git`
   - sanitize: `git remote set-url origin https://github.com/<owner>/<repo>.git`
5. Verify each repository before moving on:
   - `git ls-remote origin refs/heads/main`
   - `git status --short --branch` should show `## main...origin/main`

## Repository naming

Use a predictable lowercase kebab-case name derived from the child directory plus `-osrs`, e.g. `AchievementGapFinder` -> `achievement-gap-finder-osrs`.

For acronym-heavy names, inspect the generated name before creating the repo. A naive CamelCase splitter can turn `BossKCRivalLookup` into `boss-k-c-rival-lookup-osrs`; this is acceptable only if the user has not specified a naming convention, but future runs should prefer a smarter acronym-aware slug such as `boss-kc-rival-lookup-osrs` when creating new repos.

## Pitfalls

- Do not let a broad loop publish the boilerplate/template directory accidentally. Exact-name excludes must be checked before the generic `build.gradle`/`gradlew` inclusion test.
- Do not leave token-bearing Git remotes in local config after pushing.
- Do not count a plugin complete until its local Gradle test has passed and `ls-remote` confirms `main` exists on GitHub.
- Avoid `git add .` in plugin folders because `.gradle/`, `build/`, and generated artifacts may exist locally.
