# External API Reach-Out Guides for RuneLite Projects

Use this when creating or reviewing README documentation for a RuneLite plugin or companion service that communicates over the network.

## Source-first inventory

Inspect runtime source before writing documentation:

1. Search HTTP client classes, URL/host constants, request builders, browser-open helpers, and config-provided URLs.
2. Exclude Gradle/Maven repositories and test-only URLs from runtime API lists.
3. Separate:
   - outbound HTTP API calls;
   - browser-only links opened by the user;
   - local RuneLite client APIs that make no third-party request;
   - inbound routes exposed by a companion backend service.
4. Verify methods and dynamic path/query parameters from request construction, not assumptions.
5. Check fallback/cache/error branches, authentication headers/capabilities, uploads, and telemetry.

## Required README section

Every maintained API-driven project README should include `## External APIs` or `## API reach-out guide` and cover:

- service and host;
- relevant route(s) and HTTP method(s);
- purpose and data received;
- player/account/device data transmitted;
- authentication or explicit lack of authentication;
- cache, retry, offline, and fallback behavior;
- privacy, storage, upload, and telemetry boundaries;
- whether a listed URL is only opened in a browser.

Never publish secrets, bearer values, tokens, installation credentials, or private endpoint overrides.

For a local-only plugin, state explicitly that it makes no external API calls and identify local RuneLite APIs only when useful.

## Concise template

```markdown
## External APIs

The plugin makes these runtime network requests:

- **Service name** — `METHOD https://host/path/{parameter}`
  - Purpose: ...
  - Sends: ...
  - Receives: ...
  - Authentication: none / server-issued session / OAuth (never include credentials).
  - Failure behavior: cached data / local fallback / visible unavailable state.

Browser-only links: ...

The plugin does/does not use a custom backend, upload data, or send telemetry.
```

## Plugin Hub publication sequence

If the plugin is already submitted with an immutable marker:

1. Commit and push the README in the child plugin repository.
2. Run the Java 11 clean test/assemble suite when source changed; for docs-only changes, at minimum inspect the exact diff.
3. Update only that plugin's marker to the new full child SHA.
4. Verify the Plugin Hub PR still changes exactly one marker file.
5. Recheck official Plugin Hub checks and all review surfaces.

## Publication and repository-topology preflight

Before committing or publishing a portfolio-wide documentation pass:

1. Resolve each project's real Git root, current branch, origin URL, and dirty state. A directory name is not proof that its configured remote still represents that project.
2. Fetch the remote branch before committing/pushing. If remote history has been repurposed for another plugin, do not rebase or push the old project's README into it.
3. Query the account's actual repositories when an origin returns “Repository not found”; do not invent a renamed destination or create a repository without explicit scope.
4. Commit valid documentation locally when no remote exists, but label it local-only.
5. For submodules, push and remotely verify the child commit first. Update the parent gitlink only when that exact child SHA is reachable from the child remote; never publish a dangling pointer to a local-only commit.
6. If the parent workspace is dirty or diverged, create an isolated worktree from fetched `origin/main`, apply only the policy/docs and verified gitlinks there, validate, push as a fast-forward, and read back the remote parent/child SHAs.
7. When a README audit exposes a source contradiction (for example, a public class/file-name mismatch that makes a documented client uncompilable), apply the smallest safe source correction and run the relevant build before describing the client as usable.

## Scope control

Apply this standard to maintained/active projects. Do not mass-edit archived tutorials, vendored projects, generated files, or legacy snapshots merely because broad text search finds an HTTP URL. Determine the actual project boundary and runtime ownership first.
