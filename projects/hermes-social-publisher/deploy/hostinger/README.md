# Hostinger Postiz Deployment

This package is for a Docker-capable Hostinger VPS. Do not run it inside the Hermes container.

## Pinned stack

- Postiz `v2.23.0`
- PostgreSQL `17-alpine` for Postiz
- Redis `7.2-alpine`
- Temporal `1.28.1`
- Temporal UI `2.34.0` (optional SSH-only debug profile)
- Temporal PostgreSQL `16-alpine`
- Elasticsearch `7.17.27`
- Caddy `2.10.2-alpine`

Tags are deliberately pinned. Before production, record resolved image digests with `docker compose images --digests` or `docker image inspect`; use the same architecture when rolling back.

## Prerequisites

- Hostinger VPS: Ubuntu 24.04, 4 vCPU, 8 GB RAM, 80 GB SSD recommended.
- A DNS A/AAAA record such as `social.example.com` pointing to the VPS.
- Ports 80/tcp, 443/tcp, and 443/udp allowed; SSH restricted to trusted IPs/keys.
- Docker Engine and Compose plugin. Hostinger hPanel can install its Docker VPS template and provides Docker Compose Manager for multi-container applications.[1][2]
- A non-root deployment user with access to Docker. Treat Docker group membership as root-equivalent.

Do not expose Docker daemon ports 2375/2376 or the internal Postiz/Temporal/database ports.

## Host-side deployment

```bash
sudo install -d -m 0750 -o "$USER" -g "$USER" /opt/hermes-social-publisher
cd /opt/hermes-social-publisher
# Copy this deploy/hostinger directory here using scp, rsync, or hPanel.
./generate-secrets.sh
nano .env
chmod 600 .env
docker compose --env-file .env config --quiet
docker compose --env-file .env pull
docker compose --env-file .env up -d
docker compose --env-file .env ps
```

Set `POSTIZ_DOMAIN`, `ACME_EMAIL`, and only provider credentials that are ready. Never paste the generated `.env` into chat, logs, Git, or hPanel notes.

Verify:

```bash
curl -fsSIL "https://$(grep '^POSTIZ_DOMAIN=' .env | cut -d= -f2-)"
docker compose --env-file .env logs --since=10m postiz caddy temporal
```

Open the HTTPS URL from a phone/laptop. Create the first operator, generate a Public API key under Settings → Developers, verify it through `POSTIZ_API_KEY=... ./smoke-test.sh social.example.com`, then change `DISABLE_REGISTRATION=true` and run:

```bash
docker compose --env-file .env up -d --force-recreate postiz
```

Because Postiz disables OIDC when registration is disabled, do not enable OIDC and this single-user registration lock simultaneously.

## hPanel path

In Hostinger, use VPS → Manage. Install/select the Docker template under OS & Panel → Operating System only on a new/rebuildable VPS because changing the OS is destructive. For an existing Docker VPS, use the Docker Compose Manager or SSH; upload the package, keep `.env` private, and deploy the Compose project. Hostinger documents Compose Manager as its hPanel dashboard for containerized multi-service applications.[1]

## Provider onboarding

For each OAuth provider, register this callback, replacing `{provider}` with Postiz's API identifier:

```text
https://social.example.com/integrations/social/{provider}
```

Start with Bluesky as a harmless infrastructure probe because it needs no host-level developer app. Then pilot one official OAuth provider with a private/draft post. A connected tile is not proof: capture integration ID, returned account name/ID, granted scopes, expiration, and a harmless identity/capability response.

Do not migrate YouTube credentials or disable its current automation. Use a new Postiz Google OAuth client and a private test until rollback is proven.

## Backup

Run before every upgrade and daily once live:

```bash
./backup.sh /srv/backups/postiz/$(date -u +%Y%m%dT%H%M%SZ)
```

Copy backups off-VPS. The script stores custom-format dumps for both PostgreSQL databases, Postiz config/uploads, deployment files, and checksums. It intentionally does not copy `.env`; back that up separately in an encrypted secrets manager.

Verify restore quarterly on a disposable VPS. `restore.sh` is destructive and requires `CONFIRM_RESTORE=yes`.

## Upgrade

```bash
cd /opt/hermes-social-publisher
./backup.sh /srv/backups/postiz/pre-upgrade-$(date -u +%Y%m%dT%H%M%SZ)
cp docker-compose.yml docker-compose.pre-upgrade.yml
# Edit only the Postiz image tag after reading release and migration notes.
docker compose --env-file .env config --quiet
docker compose --env-file .env pull postiz
docker compose --env-file .env up -d postiz
docker compose --env-file .env ps
```

Run HTTPS, API, draft, scheduled workflow, and one private platform test. Never use unattended `latest` upgrades.

## Rollback

Application-only rollback when no incompatible migration ran:

```bash
cp docker-compose.pre-upgrade.yml docker-compose.yml
docker compose --env-file .env pull postiz
docker compose --env-file .env up -d --force-recreate postiz
```

Full data rollback after a migration or data corruption:

```bash
docker compose --env-file .env down
CONFIRM_RESTORE=yes ./restore.sh /srv/backups/postiz/PRE_UPGRADE_BACKUP
docker compose --env-file .env ps
```

Never add `--volumes` to `docker compose down`. Keep the current image and backup until post URLs, schedules, OAuth refresh, and analytics have passed.

## Monitoring and incident checks

```bash
docker compose --env-file .env ps
docker compose --env-file .env logs --since=30m postiz temporal caddy
docker stats --no-stream
docker system df -v
df -h /
```

Alert on container restart loops, Postiz/Temporal errors, certificate failure, >70% sustained memory, >70% disk, or failed nightly backup. Do not prune volumes automatically.

## Sources

[1] https://www.hostinger.com/tutorials/what-is-docker-compose
[2] https://www.hostinger.com/tutorials/how-to-install-docker-on-ubuntu
