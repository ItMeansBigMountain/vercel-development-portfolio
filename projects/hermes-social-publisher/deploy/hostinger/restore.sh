#!/usr/bin/env sh
set -eu

BACKUP=${1:?usage: CONFIRM_RESTORE=yes ./restore.sh BACKUP_DIRECTORY}
if [ "${CONFIRM_RESTORE:-}" != yes ]; then
  printf 'Refusing destructive restore. Re-run with CONFIRM_RESTORE=yes.\n' >&2
  exit 1
fi
(cd "$BACKUP" && sha256sum -c SHA256SUMS)
docker compose up -d postiz-postgres temporal-postgres
cat "$BACKUP/postiz.pgdump" | docker compose exec -T postiz-postgres sh -c 'dropdb -U "$POSTGRES_USER" --if-exists "$POSTGRES_DB" && createdb -U "$POSTGRES_USER" "$POSTGRES_DB" && pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists'
cat "$BACKUP/temporal.pgdump" | docker compose exec -T temporal-postgres sh -c 'dropdb -U "$POSTGRES_USER" --if-exists "$POSTGRES_DB" && createdb -U "$POSTGRES_USER" "$POSTGRES_DB" && pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists'
for volume in hermes-social-publisher-postiz-config hermes-social-publisher-postiz-uploads; do
  docker run --rm -v "$volume:/target" -v "$BACKUP:/backup:ro" alpine:3.22 \
    sh -c "rm -rf /target/* /target/.[!.]* /target/..?* 2>/dev/null || true; tar -C /target -xzf /backup/$volume.tgz"
done
docker compose up -d
printf 'Restore submitted. Verify with docker compose ps and the HTTPS smoke checks.\n'
