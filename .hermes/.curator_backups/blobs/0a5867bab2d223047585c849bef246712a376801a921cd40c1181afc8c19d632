# OSRS plugin lifecycle buckets and RuneLite Plugin Hub PR flow

Session lesson from cleaning the user's OSRS plugin workspace and preparing Who's Grinding Panel for review.

## Workspace lifecycle directories

Under `/opt/data/HeRmEz/projects/osrs-plugins`, keep class-level lifecycle buckets alongside `_templates`:

```text
_templates/
completed/
in-progress/
pr-review-pending/
```

Use them as follows:

- `in-progress/` — active OSRS/RuneLite plugin projects still being built, consolidated, tested, or polished.
- `pr-review-pending/` — plugins deemed locally complete where the remaining work is official RuneLite Plugin Hub submission/review.
- `completed/` — plugins only after the RuneLite Plugin Hub PR is approved/merged and the plugin is shareable through the official RuneLite Plugin Hub.

When moving plugin repos, use `git mv` from the HeRmEz parent so `.gitmodules` paths and submodule gitlinks are updated together. Verify with:

```bash
git -C /opt/data/HeRmEz submodule status -- projects/osrs-plugins/<bucket>/<Plugin>
git -C /opt/data/HeRmEz config -f .gitmodules --get-regexp '^submodule\..*\.path$' | grep osrs-plugins
```

After a child plugin commit, update and push the parent submodule pointer too.

### Publishing a lifecycle move from a dirty or divergent parent

A merged plugin's local worktree may need moving even when the HeRmEz parent contains unrelated changes or has diverged from remote. Do not stash, reset, merge, or broadly stage that workspace.

1. In the active parent worktree, use `git mv` for the lifecycle path, update only that submodule's `.gitmodules` path, and explicitly replace the gitlink with the accepted child SHA using `git update-index --add --cacheinfo 160000,<sha>,<new-path>`.
2. Verify the child builds from the new path and that `git ls-files -s <new-path>` stores the accepted SHA.
3. Commit only `.gitmodules`, the old path, and the new path locally; never use `git add .`.
4. Publish independently from a clean clone of remote `main`: apply the same `.gitmodules` edit, remove the old gitlink, add the new exact gitlink, and confirm the staged file set contains exactly those three paths.
5. Configure commit identity locally in the disposable clone when needed; do not alter global Git configuration.
6. Push the clean fast-forward and verify both the remote parent head and stored completed-path gitlink.

A `git mv` of a submodule can stage the old parent gitlink even when the moved child worktree is on a newer commit. Always read the staged `160000` SHA and replace it explicitly before committing.

## RuneLite Plugin Hub PR checklist

Authoritative sources checked: `runelite/plugin-hub` README and RuneLite Developer Guide.

Before moving a plugin to `pr-review-pending/`, verify:

1. Plugin repo is public on GitHub.
2. Java 11-compatible Gradle build passes.
3. `runelite-plugin.properties` is complete:
   - `displayName`
   - `author`
   - `description`
   - `tags`
   - `plugins=<fully.qualified.PluginClass>`
   - optional `version=`
   - `build=standard`
4. README explains features and any third-party data/API behavior.
5. A plugin-specific `icon.png` at repo root is max 48x72 px. Before publishing:
   - Compare its SHA-256 against every active, pending-review, completed, and template RuneLite plugin icon; no two plugins may reuse the same image.
   - Ensure its subject and silhouette clearly represent that plugin rather than a generic or copied icon.
   - If the plugin has a RuneLite sidebar/navigation icon, align it with the same approved visual identity.
   - Generate and visually inspect both an enlarged preview and the actual-size asset, then obtain user approval before applying it.
6. Latest intended commit is pushed; record the full 40-character hash.

Plugin Hub submission flow:

1. Fork/clone `runelite/plugin-hub`.
2. Add a manifest file under `plugins/`.
3. Manifest content:

```properties
repository=https://github.com/<owner>/<plugin-repo>.git
commit=<40-character commit hash>
```

4. Run Plugin Hub checks/tooling if available.
5. Commit manifest on a branch and open a PR against `runelite/plugin-hub`.
6. Respond to CI/reviewer feedback by updating the plugin repo commit and manifest commit as needed.
7. Only after the PR is merged/shareable through official Plugin Hub, move the plugin folder to `completed/` and update `.gitmodules`.

## Who's Grinding Panel finalization notes

- Current Windows run command for this repo is `gradlew.bat run --no-daemon --console=plain` from the plugin directory.
- The verified local validation command remains `./gradlew clean test assemble --no-daemon --console=plain` with Java 11.
- For gained card lines, do not render redundant trailing type labels: use `+485,257 xp`, `+16 kc`, `+34 score`, not `+485,257 xp (XP)`, `+16 kc (KC)`, or `+34 score (Score)`.
