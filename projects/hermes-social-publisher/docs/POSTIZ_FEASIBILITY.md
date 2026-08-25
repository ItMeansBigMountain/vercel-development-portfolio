# Postiz Feasibility Record

Research date: 2026-08-25. Deployment target: Hostinger VPS, not the Hermes container.

## Recommendation

Adopt Postiz as the publishing engine and keep the Hermes control plane separate. Pin the server to `ghcr.io/gitroomhq/postiz-app:v2.23.0` and the optional CLI to npm `postiz@2.0.16`. Do not use `latest`. Release v2.23.0 is the current non-prerelease and specifically adds streamed media uploads, pending-post duplicate protection, and MCP reliability/security fixes.[1] The CLI package registry currently reports 2.0.16, Node >=18, and AGPL-3.0.[11]

The fit is strong but not sufficient by itself for Hermes safety. Postiz supplies connectors, scheduling, retries, analytics surfaces, a Public API, CLI, and MCP. Hermes must still own canonical content, exact destination identity, approvals, idempotency, cleanup gates, and a publication ledger. In particular, a Postiz post can have `releaseId="missing"`; that is not a verified platform ID and must block media cleanup.

## License boundary

Postiz and Postiz-Agent are AGPL-3.0. Running an unmodified upstream image is permitted. If Postiz itself is modified and network users interact with that modified version, AGPL section 13 requires offering those users the Corresponding Source.[2] Keep the independently communicating Hermes adapter in a separate repository/service, retain upstream legal notices, record the exact upstream tag, and publish any Postiz fork source and build/install scripts if a fork is exposed. This is engineering guidance, not legal advice.

## Services and operations

Postiz runs frontend, backend, and orchestrator in one application container. It requires PostgreSQL, Redis, Temporal, and storage; the Temporal bundle adds a second PostgreSQL and Elasticsearch.[4] The deployment package therefore runs seven always-on services: Caddy, Postiz, Postiz PostgreSQL, Redis, Temporal, Temporal PostgreSQL, and Elasticsearch. Temporal UI is an SSH-only optional debug profile.

Only TCP 80/443 and UDP 443 are public. Databases, Redis, Temporal gRPC, and Elasticsearch stay on Docker internal networks. Caddy terminates public TLS. The package disables Caddy's remote admin endpoint, does not set Postiz's production-dangerous `NOT_SECURED` or `DISABLE_SSRF_PROTECTION` flags, omits Stripe/billing variables, and mounts persistent named volumes.

Hostinger documents both its Docker VPS template and its hPanel Docker Compose Manager, so the package can be installed from the host without giving the Hermes container a Docker socket.[12][13]

## Resource plan

Upstream's supported floor is 2 vCPU, 2 GB RAM, and 20 GB disk; its recommended small-team target is 4 vCPU, 8 GB RAM, and 50 GB plus upload storage. Upstream warns that 2 GB has no headroom and recommends at least 4 GB once workflows/users increase.[3]

Use a Hostinger plan with at least 4 vCPU, 8 GB RAM, and 80 GB SSD for the first production pilot. Reserve:

- 1.0-1.5 GB RAM and 10 GB disk for Ubuntu, Docker, logs, and upgrades.
- 2.0-3.0 GB RAM for Postiz during video upload/publish bursts.
- 256 MB fixed Elasticsearch JVM heap plus native/page-cache overhead.
- 1.5-2.0 GB combined for Temporal, two PostgreSQL services, Redis, and Caddy.
- At least 30 GB free for images, volumes, backups, and local uploads; use R2 before sustained video volume.

This is a capacity budget, not a benchmark from the blocked Hermes container. Measure the real VPS after 24 hours and after a representative video publish with:

```bash
docker stats --no-stream --format '{{.Name}} {{.CPUPerc}} {{.MemUsage}}'
docker system df -v
df -h /
du -sh backups
```

Scale when sustained RAM exceeds 70%, disk exceeds 70%, swap is used during publishing, or free disk is below two complete backups plus 10 GB. The shipped Elasticsearch heap is 256 MB, matching upstream's Compose baseline.

## API, CLI, and MCP

- Public API: integration discovery, connection checks, provider schemas/tools, create/list/update/delete posts, upload, missing-release reconciliation, and platform/post analytics.[8]
- CLI: JSON-output wrapper around the Public API, supporting OAuth2 device flow or `POSTIZ_API_KEY`; for self-hosting set `POSTIZ_API_URL=https://<domain>`.[9]
- MCP: 11 tools for integration/group discovery, schemas, dynamic provider tools, scheduling/listing/settings updates, and optional image/video generation. Use Bearer authentication at `/mcp`; never put the key in the URL because URLs leak into logs/history.[10]
- MCP does not currently read or reply to comments.[10]

For Hermes, use a narrow Postiz API key in a secret file/environment, list integrations before every publish, compare returned account metadata to the expected account record, create one platform variant at a time, and persist Postiz IDs plus verified native IDs/URLs.

## Platform coverage and setup

Postiz documents 34 platform types. The target set—X, LinkedIn, Reddit, Instagram, Facebook, Threads, YouTube, TikTok, Pinterest, Discord, and Bluesky—is present.[6] Coverage means the connector exists, not that this deployment is authorized or that every account can publish.

Self-hosted OAuth providers require developer apps and exact callbacks shaped as `https://<domain>/integrations/social/{provider}`. Facebook Business Instagram shares Meta credentials with Facebook; LinkedIn Page shares LinkedIn credentials. Bluesky uses per-user service URL, handle, and app password and needs no instance-level developer app.[7]

Operational gates:

- Meta: create/review the needed Facebook, Instagram, and Threads products/scopes; verify Page/professional-account identity.
- Google/YouTube: create a separate Postiz OAuth client and test privately before any migration. Existing YouTube automation remains untouched.
- TikTok: distinguish `DIRECT_POST` from inbox `UPLOAD`; inbox upload is not publication and cannot satisfy cleanup.
- X: confirm current write entitlement and costs before considering it enabled.
- Reddit: app approval plus subreddit-specific rules/flair checks.
- Pinterest, LinkedIn, Discord: create apps and use the callback identifier from Postiz.
- Bluesky: store app passwords only inside Postiz; never in Git or Hermes prompts.

## Risks and acceptance gates

- `DISABLE_REGISTRATION=true` allows only a single signup but also disables OIDC. Bootstrap the operator over HTTPS, then set it true and recreate the Postiz container.[5]
- Provider tiles can appear even when keys are absent; a visible tile is not capability proof.[7]
- Public HTTPS is mandatory because OAuth callbacks and browser API URLs must be externally reachable.[3]
- Local uploads are durable only if both Postiz database and upload volumes are backed up together.
- Temporal state is operational state; back up its PostgreSQL database too.
- No source media is deleted until every requested platform has an independently verified post ID/URL. `missing`, queue acceptance, draft creation, inbox upload, or HTTP 2xx alone do not pass.

## Sources

[1] https://api.github.com/repos/gitroomhq/postiz-app/releases/latest
[2] https://raw.githubusercontent.com/gitroomhq/postiz-app/v2.23.0/LICENSE
[3] https://docs.postiz.com/self-host/installation/system-requirements.md
[4] https://docs.postiz.com/self-host/architecture.md
[5] https://docs.postiz.com/self-host/configuration/reference.md
[6] https://docs.postiz.com/general/platforms/overview.md
[7] https://docs.postiz.com/self-host/providers/overview.md
[8] https://docs.postiz.com/public-api/introduction.md
[9] https://docs.postiz.com/cli/introduction.md
[10] https://docs.postiz.com/mcp/introduction.md
[11] https://registry.npmjs.org/postiz/latest
[12] https://www.hostinger.com/tutorials/what-is-docker-compose
[13] https://www.hostinger.com/tutorials/how-to-install-docker-on-ubuntu
