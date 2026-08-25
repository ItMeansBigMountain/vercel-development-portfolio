# Development Plan

## Phase 0 — feasibility and host gate

- Pin a stable Postiz release and inspect AGPL obligations.
- Inventory required services and expected RAM/disk.
- Produce Hostinger hPanel/Docker deployment package; do not deploy inside Hermes.
- Verify HTTPS, persistent volumes, backups, and private administration.

## Phase 1 — local control-plane MVP

- Define canonical content and publication-ledger schemas.
- Implement a Postiz client behind an interface.
- Add dry-run provider that produces platform payload previews without publishing.
- Import existing YouTube lane metadata without changing current upload behavior.
- Unit-test idempotency, duplicate detection, account routing, and partial-platform failures.

## Phase 2 — first live connector

- Connect TikTok or Meta through official OAuth in Postiz.
- Publish one rights-safe test asset privately/draft where supported.
- Retrieve and verify post ID/account identity.
- Persist ledger result and Discord summary.

## Phase 3 — cross-post pilot

- Connect YouTube plus two non-YouTube platforms.
- Submit one canonical asset with platform-specific captions.
- Confirm partial success does not trigger premature cleanup.
- Add retry and dead-letter queues.

## Phase 4 — automation integration

- Route Viral Radar, faceless, and original content outputs into the shared intake contract.
- Keep lane-specific priorities, accounts, attribution, public/private policies, and approval gates.
- Add schedule windows and content calendar.
- Add token/provider health checks.

## Phase 5 — metrics and growth

- Collect platform-native metrics.
- Add verified performance-learning reports.
- Track follower conversion, retention/watch time, engagement, and posting reliability where APIs permit.

## Release gates

- No credentials in Git/logs/Discord.
- Public HTTPS dashboard reachable from phone/laptop.
- Exact destination identity verified for every account.
- Post ID/URL recorded before cleanup.
- Duplicate submission is idempotent.
- Partial failures preserve media and retry metadata.
- Existing YouTube automation remains reversible and operational during migration.
