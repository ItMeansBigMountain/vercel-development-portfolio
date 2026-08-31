# Postiz v2.23.0 Release Gate Evidence

Date: 2026-08-31
Pinned upstream: `ghcr.io/gitroomhq/postiz-app:v2.23.0`
Upstream source commit inspected: `1e4c8dd5c4f70c4d0abd01e23cc42d5b533d1ab9`

## Decision

**NOT READY for production.** No upgrade or publication was performed.

The fixture-backed control-plane contracts pass, but source inspection found an effective `LinkedIn-Version: 202306` request in `linkedin.provider.ts` in addition to `202601`. The release gate rejects every LinkedIn version at or below the official `202508` sunset floor. Production use remains blocked until upstream removes or updates the stale request and the same gate passes against the exact candidate image/source.

Live X, LinkedIn, Pinterest, and MCP probes are also blocked by the absence of a staged v2.23.0 service and connector credentials. Credentials are not required for the fixture tests and were not read or logged.

## Verified control-plane behavior

- One Hermes attempt ID is stored in the Hermes ledger with the returned Postiz pending ID; no unsupported field is added to the upstream request contract.
- An interrupted retry reconciles the stored Postiz ID instead of invoking `create_post` again.
- A submitting attempt with no Postiz ID becomes `outcome_unknown`; automatic resubmission is prohibited because a native post may already exist.
- Terminal success requires both a native platform post ID and URL. Pending state cannot authorize media cleanup.
- MCP contract fixtures require two independent HTTP 200 initialize responses with no session ID.
- Key-in-URL discovery fixtures require HTTP 404 at the root and non-OAuth MCP protected-resource paths. Evidence replaces every query value with `[REDACTED]`.
- X fixture: exact sequential 1 MiB `Range` reads, including the final partial chunk.
- LinkedIn fixture: exact sequential 2 MiB `Range` reads, including the final partial chunk.
- Pinterest fixture: selects the `.mp4` item even when a cover image appears first.

## Exact verification

```text
PYTHONPATH=src python3 -m unittest discover -s tests -v
Ran 15 tests in 0.135s
OK
```

```text
python3 -m compileall -q src tests
exit 0
```

Exact v2.23.0 LinkedIn source probe:

```text
{'ready': False, 'evidence': ('Linkedin-Version 202306', 'Linkedin-Version 202601'), 'blockers': ('sunset LinkedIn versions found: 202306',)}
```

Relevant upstream source evidence:

- `linkedin.provider.ts`: ranged video chunk size `1024 * 1024 * 2`; most REST upload calls use `202601`, but a post request still uses `202306`.
- `x.provider.ts`: `X_UPLOAD_CHUNK_SIZE = 1024 * 1024`.
- `pinterest.provider.ts`: finds the MP4 and streams `findMp4.path`.
- `start.mcp.ts`: OAuth discovery is scoped to `/mcp-oauth`; root/other paths return 404.
- `post.workflow.v1.0.6.ts`: irreversible mutation activities use `maximumAttempts: 1`.

## Required staged probes

Run only after a non-production v2.23.0 instance and dedicated test accounts exist:

1. Submit one rights-safe private/draft test asset where supported and capture the Hermes attempt ID, Postiz pending ID, final native ID, and URL.
2. Interrupt the worker after pending persistence, restart it, and prove the native account contains exactly one post.
3. Record sanitized MCP initialize statuses and discovery statuses; never record the connector key or full keyed URL.
4. Serve a generated video from a range-capable staging origin. Capture only byte ranges/statuses: X must request 1 MiB ranges; LinkedIn must request 2 MiB ranges.
5. Send Pinterest a fixture whose cover image is first and MP4 second; verify the uploaded object is the MP4 and capture the final Pin ID/URL.
6. Capture outbound LinkedIn request path and `Linkedin-Version` value. Every request must use a currently supported version.

## Backup, migration, and rollback gate

Before staging or production candidate startup:

1. Stop new schedules and drain or snapshot active Postiz/Temporal workflow IDs.
2. Run `deploy/hostinger/backup.sh` and verify the PostgreSQL dump, Redis archive, uploads archive, and manifest/checksums are readable.
3. Pull the candidate image without changing the running service.
4. Inspect image startup/entrypoint and ORM migration files; record every migration and whether it is backward compatible.
5. Restore the backup into an isolated staging stack, start v2.23.0, and retain startup/migration logs.
6. Run this release gate and all staged probes.
7. Roll back only if no incompatible migration ran. If schema changed incompatibly, restore database, Redis, uploads, and workflow state together; application-image-only rollback is prohibited.
8. Keep the existing YouTube automation unchanged until the migration is proven reversible.

## Unresolved advisories

- Published patched floors for `GHSA-4hgh-5rhf-4qpm` and `GHSA-5m7p-wphr-xjp7` are below v2.23.0.
- `GHSA-f7jj-p389-4w45` and `GHSA-jxg2-2cmf-h66m` still have no published patched version in the recorded advisory evidence. Do not represent them as fixed. Retain restricted egress, private administration, least-privilege credentials, and rotation/incident procedures.

## Files

- `src/hermes_social_publisher/release_gate.py`
- `tests/test_postiz_release_gate.py`
- `docs/RELEASE_WATCH.md`
- `docs/PLATFORM_MATRIX.md`
