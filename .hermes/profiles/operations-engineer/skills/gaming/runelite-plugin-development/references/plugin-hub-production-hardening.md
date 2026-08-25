# Plugin Hub production-hardening pass

Use this after a Plugin Hub PR is open and before calling the plugin production-ready.

## Review every feedback surface

For the upstream `runelite/plugin-hub` PR, inspect all of:

1. `GET /repos/runelite/plugin-hub/issues/{pr}/comments` — maintainer and bot conversation.
2. `GET /repos/runelite/plugin-hub/pulls/{pr}/reviews` — formal reviews.
3. `GET /repos/runelite/plugin-hub/commits/{head_sha}/check-runs` — packager and Plugin Hub checks.

Do not rely on `/pulls/{pr}/comments`; that endpoint is for inline review comments and can be empty while actionable issue comments exist.

Interpretation:

- `build: success` proves the official packager accepted the pinned plugin revision.
- `RuneLite Plugin Hub Checks: failure` with title `Requires maintainer review.` is the expected human-review gate.
- A maintainer comment or `Changes are needed` is actionable and must be fixed.

## Production-option scan

Before updating the marker, scan source, configuration, metadata, tests, and README for user-accessible development surfaces:

- developer/development/debug/mock/test modes;
- pretend-role or authority simulation;
- experimental endpoints or service URL overrides;
- enum values labeled development-only;
- hidden config that still remains selectable through migration or serialization.

Remove the option and its behavior, docs, and tests—not just its label. Normal internal `log.debug(...)` calls are logging, not user-accessible developer options.

For RuneLite review, also search for prohibited implementation patterns named by maintainers. One observed example is `Thread.currentThread().interrupt()`: when maintainers disallow thread interruption, remove every call, rebuild, and reply with the exact replacement plugin SHA.

## Update the existing PR safely

1. Make the plugin change on its canonical branch.
2. Run a clean Java 11 `test assemble` build.
3. Push and capture the full 40-character plugin SHA.
4. Update only `commit=` in the existing `plugins/<name>` marker on the current PR branch.
5. Push the same branch; do not open a replacement PR.
6. Reply to actionable maintainer comments with a concise description and exact plugin SHA.
7. Poll until the official `build` check succeeds and the Plugin Hub check reaches either maintainer review or an actionable result.

## Parent workspace pointer integrity

After child and marker pushes, update parent gitlinks using SHAs obtained from `git rev-parse`, never by expanding a short hash manually. Verify with:

```text
git ls-files -s <plugin-path> <plugin-hub-path>
```

Each `160000` SHA must equal the verified child or marker-branch commit. If unrelated parent history blocks publishing, use a clean checkout of remote `main`, update only the intended gitlinks, commit, push, and verify remote `main`.
