# Hermes Social Publisher

A self-hosted, agent-operated content distribution system for creating once, adapting per platform, and publishing across YouTube, TikTok, Instagram/Facebook Reels, Threads, LinkedIn, X, Reddit, Pinterest, Bluesky, and future networks.

## Decision

Use **Postiz as the upstream cross-posting engine** instead of rebuilding every OAuth connector and scheduler from scratch. Build a thin Hermes-owned control plane around its API/CLI/MCP surfaces for content intake, per-platform adaptation, approvals, publication ledgers, credential health, metrics feedback, and Discord reporting.

Postiz is AGPL-3.0, self-hostable, uses official platform OAuth flows, supports broad network coverage, and is designed for automation. Self-hosting is software-free but still consumes infrastructure.

## Constraints

- The Hermes container has no Docker socket. Postiz must be deployed from the Hostinger host/hPanel or another Docker-capable public host.
- The current `/opt/data` filesystem is about 89% used; do not install Postiz's PostgreSQL/Redis/Temporal stack inside this container.
- Social account secrets and refresh tokens must remain outside Git under `/opt/data/secrets/social/` or the Postiz host's protected secret store.
- Every publish must verify destination account and return a platform post ID/URL before local cleanup.
- The existing YouTube pipelines remain operational during migration.

## Source of truth

- `PRODUCT_DIRECTION.md` — scope and architecture
- `DEVELOPMENT_PLAN.md` — delivery phases and verification gates
- `docs/CREDENTIAL_MODEL.md` — token and account safety
- `docs/PLATFORM_MATRIX.md` — platform readiness and blockers
- `docs/POSTIZ_FEASIBILITY.md` — pinned upstream, license, surfaces, coverage, and capacity record
- `deploy/hostinger/` — validated, version-pinned Hostinger Compose deployment/backup/rollback package
