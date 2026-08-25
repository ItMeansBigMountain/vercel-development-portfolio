#!/usr/bin/env sh
set -eu
umask 077

DEST=${1:-./backups/$(date -u +%Y%m%dT%H%M%SZ)}
mkdir -p "$DEST"

docker compose exec -T postiz-postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=custom' > "$DEST/postiz.pgdump"
docker compose exec -T temporal-postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=custom' > "$DEST/temporal.pgdump"
for volume in hermes-social-publisher-postiz-config hermes-social-publisher-postiz-uploads; do
  docker run --rm -v "$volume:/source:ro" -v "$DEST:/backup" alpine:3.22 \
    tar -C /source -czf "/backup/$volume.tgz" .
done
cp docker-compose.yml Caddyfile "$DEST/"
sha256sum "$DEST"/* > "$DEST/SHA256SUMS"
printf 'Backup written to %s\n' "$DEST"
