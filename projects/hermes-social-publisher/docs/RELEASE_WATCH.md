# Postiz Release Watch

## 2026-08-31 baseline — Postiz v2.23.0

Upstream release: https://github.com/gitroomhq/postiz-app/releases/tag/v2.23.0
Published: 2026-08-04
Release commit shown by GitHub: `1e4c8dd`

### Verified changes

- Provider media is streamed instead of fully buffered. X uses 1 MB ranged chunks and LinkedIn uses 2 MB ranges, reducing worker peak memory for large video uploads.
- Pending-post workflow v1.0.6 resolves interrupted in-flight posts before publishing to reduce duplicate publication.
- Webhook and media-path fetches use a safe request dispatcher for SSRF protection; streamed upload paths and Reddit S3 response parsing were hardened.
- MCP Streamable HTTP is stateless. OAuth discovery metadata no longer breaks connectors that put their key in the URL.
- Pinterest video pins now select and upload the MP4 rather than the first media item.
- Login, password-reset, and impersonation email lookups are case-insensitive. Coupon controls for impersonated users do not affect the Hermes publishing scope.

### Security advisories checked

- `GHSA-4hgh-5rhf-4qpm` (critical): unauthenticated `/uploads` encoded path traversal could expose process secrets and enable administrator session forgery. GitHub marks versions `<2.22.1` affected and `2.22.1` patched.
- `GHSA-5m7p-wphr-xjp7` (moderate): forged or replayed lifetime-deal codes. GitHub marks versions `<2.21.10` affected and `2.21.10` patched.
- The deployment package's v2.23.0 pin is above both published patched-version floors. This is version-range evidence only, not a live deployment or exploit test.
- Older advisory `GHSA-f7jj-p389-4w45` (SSRF through DNS rebinding) and `GHSA-jxg2-2cmf-h66m` (password hash in JWT) currently show no patched version in GitHub's advisory API. Do not claim v2.23.0 resolves either without new upstream evidence; keep network egress controls, private administration, and secret rotation/incident procedures.

### API, CLI, MCP, connector, and migration impact

- No release-note evidence of a breaking Postiz Public API or CLI contract change.
- MCP clients must support stateless Streamable HTTP and should re-run discovery/authentication tests for key-in-URL configurations; credentials must remain outside logs and Git.
- Hermes must not replace its own idempotency ledger with Postiz's pending-post workflow. Correlate one Hermes attempt ID with Postiz's pending/final state and require a native post ID/URL before cleanup.
- Re-run large-video tests for X and LinkedIn and a real MP4 selection test for Pinterest before enabling those connectors. Pinterest's official flow requires registering an upload, sending the actual video file to the returned upload URL, then creating the Pin.
- LinkedIn's official Marketing API notice says version `202508` was sunset on 2026-08-17 and identifies `202608` as current. Confirm the Postiz connector's effective LinkedIn version/header before production; the Postiz release notes do not state it.
- Upstream notes do not identify a database schema migration or manual migration command. Treat pending-post workflow v1.0.6 as a state/queue compatibility change: back up first, stage upgrade, inspect migrations/logs, test interrupted publish recovery, and do not roll back application-only if an incompatible migration ran.
- No production upgrade was performed by this watch.

### 2026-08-31 release-gate result

- **NOT READY for production.** Exact v2.23.0 source commit `1e4c8dd5c4f70c4d0abd01e23cc42d5b533d1ab9` contains effective LinkedIn headers `202601` and stale `202306`; the executable gate rejects the latter because it is below the official `202508` sunset floor.
- Fixture-backed adapter, MCP, X 1 MiB range, LinkedIn 2 MiB range, and Pinterest MP4-selection contracts pass. The adapter persists the Postiz pending ID and reconciles interrupted retries without a second create call; unknown outcomes are never automatically resubmitted.
- Live connector probes remain blocked until a staged v2.23.0 service and dedicated test credentials exist. No credentials were read and no social post was created.
- Exact evidence, backup/migration/rollback procedure, unresolved-advisory posture, and test output: [`POSTIZ_V2_23_RELEASE_GATE.md`](POSTIZ_V2_23_RELEASE_GATE.md).

### Sources

- https://github.com/gitroomhq/postiz-app/releases/tag/v2.23.0
- https://github.com/gitroomhq/postiz-app/security/advisories/GHSA-4hgh-5rhf-4qpm
- https://github.com/gitroomhq/postiz-app/security/advisories/GHSA-5m7p-wphr-xjp7
- https://github.com/gitroomhq/postiz-app/pull/1717
- https://github.com/gitroomhq/postiz-app/pull/1781
- https://github.com/gitroomhq/postiz-app/pull/1796
- https://github.com/gitroomhq/postiz-app/pull/1786
- https://github.com/gitroomhq/postiz-app/pull/1813
- https://github.com/gitroomhq/postiz-app/pull/1835
- https://github.com/gitroomhq/postiz-app/pull/1802
- https://developers.pinterest.com/docs/work-with-organic-content-and-users/create-boards-and-pins
- https://learn.microsoft.com/en-us/linkedin/marketing/integrations/recent-changes?view=li-lms-2026-08
- https://learn.microsoft.com/en-us/linkedin/marketing/versioning?view=li-lms-2026-08
