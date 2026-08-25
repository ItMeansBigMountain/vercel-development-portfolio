# RuneLite Plugin Hub contributor PR workflow

Use this when the user wants one of their OSRS/RuneLite plugin repos submitted to RuneLite Plugin Hub, or says the plugins must be committed to the RuneLite/plugin-hub repo as a contributor.

## User-specific workspace assumptions

- Parent workspace: `/opt/data/HeRmEz/projects/osrs-plugins/`
- Each child directory, e.g. `/opt/data/HeRmEz/projects/osrs-plugins/AccountLegacyCard`, is intended to be a standalone Git repo/submodule for that one plugin.
- The parent `osrs-plugins` directory is a backup/portfolio container, not the repo that gets submitted to RuneLite.
- RuneLite plugins do **not** need Vercel or web deployment.

## Submission flow

1. In the child plugin repo, verify metadata points at the correlated GitHub repo:
   - `runelite-plugin.properties` should have `support=https://github.com/ItMeansBigMountain/<plugin-repo>`.
   - `plugins=` should reference the actual plugin main class.
2. Build/test the child plugin with Java 11:
   ```bash
   export JAVA_HOME=/opt/data/jdks/current-java11
   export PATH="$JAVA_HOME/bin:$PATH"
   ./gradlew clean test assemble --no-daemon --console=plain
   ```
3. Commit and push the child plugin repo first. Capture the full 40-character commit SHA:
   ```bash
   git add .
   git commit -m "fix: ..."   # if changes were needed
   git push origin main
   git rev-parse HEAD
   ```
4. In the user's `plugin-hub` fork, create/update a branch named for the plugin:
   ```bash
   cd /opt/data/HeRmEz/projects/plugin-hub
   git checkout -B <plugin-slug>
   ```
5. Add `plugins/<plugin-slug>` with exactly:
   ```text
   repository=https://github.com/ItMeansBigMountain/<plugin-repo>.git
   commit=<full-child-plugin-commit-sha>
   ```
6. Commit and push the plugin-hub fork branch:
   ```bash
   git add plugins/<plugin-slug>
   git commit -m "Add <plugin display name>"
   git push -u origin <plugin-slug> --force
   ```
7. Give the user the PR compare URL:
   ```text
   https://github.com/runelite/plugin-hub/compare/master...ItMeansBigMountain:plugin-hub:<plugin-slug>?expand=1
   ```
8. If the plugin is nested/submodule-tracked in `/opt/data/HeRmEz`, commit and push the parent pointer after the child repo and plugin-hub branch are pushed:
   ```bash
   cd /opt/data/HeRmEz
   git add projects/osrs-plugins/<PluginName> projects/plugin-hub .gitmodules
   git commit -m "chore: update OSRS plugin submission pointers"
   git push origin main
   ```

## Verification notes and pitfalls

- The local `plugin-hub/package ./gradlew :package:build` can fail from upstream packaging test/resource assumptions unrelated to the manifest change. Still run it when useful, but do not treat a local package test failure as definitive plugin rejection without inspecting whether the failure is from the new manifest or from missing upstream test resources.
- Always build the child plugin itself; this is the most important pre-PR check.
- Use the full commit SHA in Plugin Hub manifests, not a branch name or short SHA.
- Do not tell the user a plugin is ready to clone/pull until both `git push` in the child repo and, if relevant, parent HeRmEz pointer push have succeeded.
- If the user asks for the “hit URL” or clone URL, answer with the GitHub plugin repo URL first, then mention local backup path second.
