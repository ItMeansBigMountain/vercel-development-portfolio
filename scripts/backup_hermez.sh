#!/usr/bin/env bash
set -euo pipefail

# Ensure git uses the hermes user's persisted credential store in this container.
export HOME="/opt/data"

REPO="/opt/data/HeRmEz"
SRC="/opt/data"
BACKUP_DIR="$REPO/.hermes"
PROJECTS_DIR="$REPO/projects"
BACKUP_BRANCH="${HERMES_BACKUP_BRANCH:-workspace-backup}"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Serialize runs. Snapshot staging uses an alternate Git index, so active
# development branches and their staging areas are never changed.
LOCK_FILE="${HERMES_BACKUP_LOCK_FILE:-/opt/data/.hermes-backup.lock}"
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "ERROR: another HeRmEz backup is already running" >&2
  exit 1
fi

# Use the runtime GitHub token non-interactively when available. The helper
# contains no credential; it prints the token from the process environment and
# is removed on exit.
ASKPASS_HELPER=""
if [ -n "${GITHUB_ACCESS_TOKEN:-}" ]; then
  ASKPASS_HELPER="$(mktemp)"
  printf '%s\n' '#!/usr/bin/env bash' > "$ASKPASS_HELPER"
  printf '%s\n' 'case "$1" in' >> "$ASKPASS_HELPER"
  printf '%s\n' '  *Username*) printf "%s\\n" "x-access-token" ;;' >> "$ASKPASS_HELPER"
  printf '%s\n' '  *Password*) printf "%s\\n" "$GITHUB_ACCESS_TOKEN" ;;' >> "$ASKPASS_HELPER"
  printf '%s\n' '  *) exit 1 ;;' >> "$ASKPASS_HELPER"
  printf '%s\n' 'esac' >> "$ASKPASS_HELPER"
  chmod 700 "$ASKPASS_HELPER"
  export GIT_ASKPASS="$ASKPASS_HELPER"
  export GIT_TERMINAL_PROMPT=0
  trap 'rm -f "$ASKPASS_HELPER"' EXIT
fi

if [ ! -d "$REPO/.git" ]; then
  echo "ERROR: $REPO is not a git repository" >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR" "$PROJECTS_DIR"

git -C "$REPO" fetch origin --prune >/dev/null 2>&1 || true

# Sanitize Hermes home into the repo. This intentionally excludes secrets,
# credentials, runtime locks/pids, nested git metadata, and the repo itself to
# avoid recursive backups. Prefer rsync when available; otherwise use a Python
# fallback so the cron job works on minimal containers.
if [ "${HERMES_BACKUP_SKIP_SYNC:-0}" = "1" ]; then
  echo "INFO: sanitized Hermes-home sync skipped for verification"
elif command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude='/HeRmEz/***' \
    --exclude='/.env' \
    --exclude='/.env.*' \
    --include='/.env.*.template' \
    --exclude='/.git-credentials' \
    --exclude='/.gitconfig' \
    --exclude='/.cache/***' \
    --exclude='/.config/***' \
    --exclude='/.npm/***' \
    --exclude='/.gradle/***' \
    --exclude='/.local/***' \
    --exclude='/.expo/***' \
    --exclude='/jdks/***' \
    --exclude='/.nuget/***' \
    --exclude='/.dotnet/***' \
    --exclude='/home/***' \
    --exclude='/kanban/workspaces/***' \
    --exclude='/kanban/logs/***' \
    --exclude='/sandboxes/***' \
    --exclude='/image_cache/***' \
    --exclude='/images/***' \
    --exclude='/tmp/***' \
    --exclude='/bin/***' \
    --exclude='/cache/***' \
    --exclude='/lsp/***' \
    --exclude='/logs/***' \
    --exclude='/sessions/***' \
    --exclude='/audio_cache/***' \
    --exclude='/state-snapshots/***' \
    --exclude='/backups/***' \
    --exclude='/ibmcloud-cli/***' \
    --exclude='/hermes-agent/***' \
    --exclude='/credentials/***' \
    --exclude='/secrets/***' \
    --exclude='/.curator_backups/***' \
    --exclude='/models_dev_cache.json' \
    --exclude='/processes.json' \
    --exclude='/gateway_state.json' \
    --exclude='/gateway_voice_mode.json' \
    --exclude='/context_length_cache.yaml' \
    --exclude='/provider_models_cache.json' \
    --exclude='/ollama_cloud_models_cache.json' \
    --exclude='/kanban.db*' \
    --exclude='/kanban*.bak' \
    --exclude='/kanban*.sql' \
    --exclude='/*oauth_pending*.json' \
    --exclude='**/*oauth_pending*.json' \
    --exclude='/*.bak*' \
    --exclude='/.hermes/state.db' \
    --exclude='/.hermes/.agent-browser/***' \
    --exclude='/.hermes/profiles/*/state.db*' \
    --exclude='**/*.db' \
    --exclude='**/*.sqlite' \
    --exclude='**/*.sqlite3' \
    --exclude='/auth.json' \
    --exclude='/auth.lock' \
    --exclude='**/*secret*' \
    --exclude='**/*token*' \
    --exclude='**/*credential*' \
    --exclude='**/oauth*.json' \
    --exclude='**/keyring*' \
    --exclude='**/*.pem' \
    --exclude='**/*.key' \
    --exclude='**/*.p12' \
    --exclude='**/*.pfx' \
    --exclude='**/id_rsa*' \
    --exclude='**/id_ed25519*' \
    --exclude='*.lock' \
    --exclude='*.pid' \
    --exclude='*.sock' \
    --exclude='**/.tick.lock' \
    --exclude='**/__pycache__/***' \
    --exclude='**/.pytest_cache/***' \
    --exclude='**/.mypy_cache/***' \
    --exclude='**/.ruff_cache/***' \
    --exclude='**/.venv/***' \
    --exclude='**/venv/***' \
    --exclude='**/*.egg-info/***' \
    --exclude='**/node_modules/***' \
    --exclude='**/dist/***' \
    --exclude='**/build/***' \
    --exclude='**/.next/***' \
    --exclude='**/.nuxt/***' \
    --exclude='**/.expo/***' \
    --exclude='**/.terraform/***' \
    --exclude='**/.terragrunt-cache/***' \
    --exclude='**/.vercel/***' \
    --exclude='**/.angular/***' \
    --exclude='**/.turbo/***' \
    --exclude='**/.parcel-cache/***' \
    --exclude='**/bin/***' \
    --exclude='**/obj/***' \
    --exclude='**/test-results/***' \
    --exclude='**/*.tsbuildinfo' \
    --exclude='**/.git/***' \
    "$SRC/" "$BACKUP_DIR/"
else
  python3 - <<'PY'
import fnmatch
import os
import shutil
from pathlib import Path

src = Path('/opt/data')
dst = Path('/opt/data/HeRmEz/.hermes')

exclude_exact = {
    '.env', '.git-credentials', '.gitconfig', 'auth.json', 'auth.lock',
    'processes.json', 'gateway_state.json', 'gateway_voice_mode.json',
    'context_length_cache.yaml', 'provider_models_cache.json',
    'ollama_cloud_models_cache.json',
}
exclude_dir_names = {
    '.git', '.cache', '.config', '.npm', '.gradle', '.local', '.expo', '.nuget', '.dotnet',
    'jdks', 'tmp', 'bin', 'cache', 'lsp', 'logs', 'sessions', 'audio_cache',
    'state-snapshots', 'backups', 'ibmcloud-cli', 'hermes-agent', 'credentials', 'secrets',
    'home', 'sandboxes', 'image_cache', 'images', 'workspaces', '__pycache__',
    '.pytest_cache', '.mypy_cache', '.ruff_cache', '.venv', 'venv', 'node_modules',
    'dist', 'build', 'web_dist', '.next', '.nuxt', '.terraform', '.terragrunt-cache',
    '.vercel', '.angular', '.turbo', '.parcel-cache', 'obj', 'test-results',
    '.curator_backups',
}
exclude_file_globs = [
    '.env.*', 'models_dev_cache.json', '*secret*', '*token*', '*credential*', 'oauth*.json', 'keyring*',
    '*.pem', '*.key', '*.p12', '*.pfx', 'id_rsa*', 'id_ed25519*',
    '*.db', '*.sqlite', '*.sqlite3', '*.db-*', '*.lock', '*.pid', '*.sock', '.tick.lock',
]
include_names = {'.env.discord.template'}

dst.mkdir(parents=True, exist_ok=True)

for root, dirs, files in os.walk(src):
    rootp = Path(root)
    rel = rootp.relative_to(src)
    if rel.parts and rel.parts[0] == 'HeRmEz':
        dirs[:] = []
        continue
    dirs[:] = [d for d in dirs if d not in exclude_dir_names]
    target_dir = dst / rel
    target_dir.mkdir(parents=True, exist_ok=True)
    for name in files:
        if name in include_names:
            pass
        elif name in exclude_exact or any(fnmatch.fnmatch(name, pat) for pat in exclude_file_globs):
            continue
        source = rootp / name
        target = target_dir / name
        try:
            if source.is_symlink():
                linkto = os.readlink(source)
                if target.exists() or target.is_symlink():
                    target.unlink()
                os.symlink(linkto, target)
            else:
                shutil.copy2(source, target)
        except (FileNotFoundError, PermissionError):
            # File changed/disappeared or unreadable during backup; skip it.
            continue
PY
fi

# rsync exclusions do not remove a directory copied by an older script. This
# directory contains full machine archives and must never be nested in Git.
rm -rf -- "$BACKUP_DIR/backups"

# Config is useful recovery state, but dashboard credentials must never enter
# Git. Blank credential-bearing fields in the sanitized copy only; the live
# runtime reads its password hash/signing key from the protected .env file.
/opt/hermes/.venv/bin/python - <<'PY'
from pathlib import Path
import yaml
p = Path('/opt/data/HeRmEz/.hermes/config.yaml')
if p.exists():
    data = yaml.safe_load(p.read_text(encoding='utf-8')) or {}
    basic = (data.setdefault('dashboard', {}).setdefault('basic_auth', {}))
    for key in ('password', 'password_hash', 'secret'):
        basic[key] = ''
    p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding='utf-8')
PY

cat > "$BACKUP_DIR/BACKUP_MANIFEST.md" <<EOF
# Hermes home backup manifest

Last backup: $STAMP
Source: /opt/data
Destination: /opt/data/HeRmEz/.hermes

This is a sanitized snapshot. Excluded intentionally:

- /opt/data/HeRmEz itself, to avoid recursive backups
- .env, .git-credentials, .gitconfig
- auth.json and auth.lock
- OAuth/keyring files
- files whose names contain secret, token, or credential
- private key material (*.pem, *.key, *.p12, *.pfx, id_rsa*, id_ed25519*)
- runtime locks, pids, sockets, common cache/build directories, session logs, local SDKs/CLIs, and generated installs
- downloaded package stores/SDKs (.nuget, .dotnet, node_modules, virtualenvs)
- Kanban scratch workspaces, sandboxes, generated media, and provider/deployment caches
- runtime databases, journals, corruption snapshots, and OAuth pending callback state
- nested .git directories

Future project folders should live under /opt/data/HeRmEz/projects.
EOF

mkdir -p "$REPO/scripts"
cp -p "$0" "$REPO/scripts/backup_hermez.sh"
cp -p "/opt/data/scripts/verify_hermez_backup_stage.py" "$REPO/scripts/verify_hermez_backup_stage.py"

if ! git -C "$REPO" config user.email >/dev/null; then
  git -C "$REPO" config user.email 'hermes-agent@local'
fi
if ! git -C "$REPO" config user.name >/dev/null; then
  git -C "$REPO" config user.name 'Hermes Agent'
fi

cd "$REPO"

# Build the snapshot in an alternate index. This avoids committing unrelated
# staged work and makes the backup independent of the checked-out branch.
ALT_INDEX="$(mktemp)"
rm -f "$ALT_INDEX"
trap 'rm -f "$ASKPASS_HELPER" "$ALT_INDEX"' EXIT
export GIT_INDEX_FILE="$ALT_INDEX"
git read-tree HEAD

# Active workers may create/remove generated files while staging. Retry the
# alternate index only; the developer's real index remains untouched.
add_ok=0
for attempt in 1 2 3 4 5; do
  # Add tracked paths explicitly; nested repos that aren't registered submodules
  # are skipped to avoid "does not have a commit checked out" failures.
  if git add -A -- .gitignore .gitmodules README.md KANBAN.md .hermes \
      scripts/backup_hermez.sh scripts/verify_hermez_backup_stage.py; then
    # Stage projects/* content while ignoring nested .git directories and
    # archive/backup directories containing large files or nested repos.
    # Note: symlinks in _ops mean we skip the whole _ops directory.
    if git add -A -- 'projects/*' ':!projects/**/.git/**' ':!projects/_ops/**' ':!projects/dayz-survival-unity/**' ':!projects/game-dev/**' ':!projects/_archive/**' ':!projects/_backups/**' ':!projects/mcp-unity/**' ':!projects/rts-js-chatrooms/**'; then
      add_ok=1
      break
    fi
  fi
  sleep "$attempt"
done
if [ "$add_ok" -ne 1 ]; then
  echo "ERROR: backup staging remained unstable after 5 attempts" >&2
  exit 1
fi

/opt/hermes/.venv/bin/python "$REPO/scripts/verify_hermez_backup_stage.py"
TREE_SHA="$(git write-tree)"

REMOTE_PARENT="$(git rev-parse --verify "refs/remotes/origin/$BACKUP_BRANCH" 2>/dev/null || true)"
if [ -n "$REMOTE_PARENT" ] && [ "$(git rev-parse "$REMOTE_PARENT^{tree}")" = "$TREE_SHA" ]; then
  echo "✅ **HeRmEz backup current**"
  echo "• Branch: $BACKUP_BRANCH"
  echo "• Commit: ${REMOTE_PARENT:0:12}"
  exit 0
fi

COMMIT_MSG="chore: automated HeRmEz backup $STAMP"
if [ -n "$REMOTE_PARENT" ]; then
  SNAPSHOT_SHA="$(printf '%s\n' "$COMMIT_MSG" | git commit-tree "$TREE_SHA" -p "$REMOTE_PARENT")"
else
  SNAPSHOT_SHA="$(printf '%s\n' "$COMMIT_MSG" | git commit-tree "$TREE_SHA" -p HEAD)"
fi

if [ "${HERMES_BACKUP_DRY_RUN:-0}" = "1" ]; then
  echo "✅ **HeRmEz backup dry run passed**"
  echo "• Branch: $BACKUP_BRANCH"
  echo "• Candidate: ${SNAPSHOT_SHA:0:12}"
  exit 0
fi

git push origin "$SNAPSHOT_SHA:refs/heads/$BACKUP_BRANCH" >/dev/null

REMOTE_SHA="$(git ls-remote --heads origin "$BACKUP_BRANCH" | cut -f1)"
if [ "$SNAPSHOT_SHA" != "$REMOTE_SHA" ]; then
  echo "ERROR: pushed backup but remote SHA mismatch" >&2
  echo "local=$SNAPSHOT_SHA" >&2
  echo "remote=$REMOTE_SHA" >&2
  exit 1
fi

echo "✅ **HeRmEz backup pushed**"
echo "• Branch: $BACKUP_BRANCH"
echo "• Commit: ${SNAPSHOT_SHA:0:12}"
