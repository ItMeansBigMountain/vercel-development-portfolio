# RuneLite Plugin Hub upstream PR validation

## Why standalone builds are insufficient

A plugin can pass its own `./gradlew clean test assemble` and still fail the official Plugin Hub packager. For `build=standard`, upstream compiles against RuneLite's bundled API/dependency surface rather than blindly honoring newer versions declared by the plugin project.

Treat the actual `runelite/plugin-hub` pull-request `build` check as the authoritative compatibility test.

## Submission sequence

1. Confirm the plugin is in a public standalone repository with a clean Java 11 build, tests, README, BSD-2-Clause license, and a 48x72 `icon.png` when an icon is included.
2. Ensure `runelite-plugin.properties` has complete metadata. For this portfolio, finalize candidates with explicit `version=<semver>` and `build=standard`.
3. Commit and push the plugin repository first. Record the full 40-character commit SHA.
4. Sync the user's `plugin-hub` fork to `runelite/plugin-hub` `master`.
5. Create a fresh branch from `upstream/master` for exactly one plugin.
6. Add exactly one marker file under `plugins/<unique-kebab-name>`:

   ```properties
   repository=https://github.com/<owner>/<repo>.git
   commit=<full-40-character-plugin-sha>
   ```

7. Open a non-draft PR to `runelite/plugin-hub:master`. One plugin marker per PR keeps review and CI isolated.
8. Monitor the upstream `build` check. If it fails, download the GitHub Actions log/annotations, patch the standalone plugin, rebuild, push a new plugin SHA, and update the marker in the existing PR branch.
9. Before pushing any marker refresh, query the live PR and use its authoritative `head.repo.full_name` and `head.ref`; do not rely on a remembered local/remote branch name from an earlier submission. Push the current marker commit explicitly to `HEAD:<head.ref>`, then read the PR back and verify that `head.sha` advanced and the changed-file list is still exactly the intended one marker. A similarly named stale branch may exist and may reject non-fast-forward pushes; that is not evidence that the active PR branch is wrong.
10. Read Plugin Hub bot comments and reviews. Do not interpret every red policy check as an actionable code failure.

## Bundled Gson compatibility pitfall

The official packager may expose an older RuneLite-bundled Gson than a standalone build resolves. Static calls such as:

```java
JsonParser.parseString(json)
```

can therefore compile locally but fail upstream with `cannot find symbol`.

Use the backward-compatible form when targeting the Plugin Hub dependency surface:

```java
new JsonParser().parse(json)
```

After changing it, rerun the standalone Java 11 build, push the plugin commit, and update the marker SHA. Never update only the marker without pushing and verifying the referenced plugin commit.

## Check interpretation

- `.github/workflows/build.yml / build` or check name `build` with conclusion `success`: Plugin Hub packaging passed.
- `RuneLite Plugin Hub Checks` with title **Requires maintainer review**: expected human-review gate for a new plugin, not an automated code defect. Confirm the bot summary says a maintainer will request additional changes if needed.
- `Changes are needed`, compiler errors, annotations, or maintainer review comments: actionable; inspect and fix before reporting the PR as ready.
- `upload` is normally skipped for pull requests and is not a failure.

## Final verification

Read each PR back from the upstream API and verify:

- `state=open`
- `draft=false`
- upstream `build=success`
- marker points to the latest pushed standalone-plugin SHA
- no `CHANGES_REQUESTED` review and no unresolved actionable maintainer comment

Report the upstream PR URL and clearly distinguish “packager green, awaiting maintainer review” from “approved/merged.” Move a project from `pr-review-pending` to `completed` only after official approval/merge.
