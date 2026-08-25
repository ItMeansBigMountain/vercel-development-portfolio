# Nested repo submodules and backup-cache hygiene

Use this when a parent workspace repo contains child projects that are themselves Git repos and the user explicitly wants the child repos represented as submodules rather than bundle artifacts.

## Pattern

1. Inventory nested repos without traversing `.git` internals:

```bash
python3 - <<'PY'
from pathlib import Path
import subprocess
root = Path('/path/to/parent')
for gitdir in sorted(root.rglob('.git')):
    repo = gitdir.parent
    if repo == root:
        continue
    rel = repo.relative_to(root)
    remote = subprocess.run(['git','-C',str(repo),'remote','get-url','origin'], text=True, capture_output=True).stdout.strip()
    branch = subprocess.run(['git','-C',str(repo),'branch','--show-current'], text=True, capture_output=True).stdout.strip() or 'main'
    head = subprocess.run(['git','-C',str(repo),'rev-parse','--short','HEAD'], text=True, capture_output=True).stdout.strip()
    print(rel, branch, head, remote)
PY
```

2. Only convert repos with a real remote URL. If a nested repo has no remote, create/push it first or use the bundle pattern instead.

3. Register each child in `.gitmodules` and stage the gitlink:

```bash
git config -f .gitmodules submodule.projects/name.path projects/name
git config -f .gitmodules submodule.projects/name.url https://github.com/owner/name.git
git config -f .gitmodules submodule.projects/name.branch main
git add .gitmodules projects/name
```

4. Absorb child `.git` directories into the parent repo's submodule metadata when the child already exists as a full nested worktree:

```bash
git submodule absorbgitdirs projects/name
```

5. Verify:

```bash
git submodule init
git submodule status
git ls-files -s | awk '$1=="160000"{print}'
git config -f .gitmodules --get-regexp '^submodule\..*\.(path|url|branch)$'
```

## Backup repo cache hygiene

Automated workspace backups can accidentally stage huge runtime artifacts such as browser binaries, npm/pip caches, telemetry files, or SQLite state DBs. Before committing backup/submodule fixes:

```bash
# Remove already-tracked cache/runtime artifacts from the parent index only.
git rm -r --cached --ignore-unmatch \
  .hermes/.cache .hermes/.config .hermes/.npm .hermes/.local/share/pki .hermes/state.db

# Verify no staged additions exceed GitHub's 100MB hard limit.
python3 - <<'PY'
import os, subprocess
files = subprocess.run(['git','diff','--cached','--name-only','--diff-filter=AM'], text=True, capture_output=True).stdout.splitlines()
for f in files:
    try: size = os.path.getsize(f)
    except OSError: continue
    if size > 50_000_000:
        print(f, size)
PY
```

Add ignore rules for the parent backup repo:

```gitignore
/.hermes/.cache/
/.hermes/.config/
/.hermes/.npm/
/.hermes/.local/share/pki/
/.hermes/state.db
/.hermes/**/*.db
/.hermes/**/*.sqlite
/.hermes/**/*.sqlite3
```

If the backup script mirrors home/workspace content into `.hermes`, exclude cache/config/npm/pki and DB patterns in the sync step and exclude `.cache`, `.config`, `.npm`, DBs, locks, pids, and sockets from any sanitizer walk.

## Verification checklist

- `bash -n` any backup scripts touched.
- `git submodule status` lists each child at a commit.
- `git ls-files -s` shows child paths as mode `160000` gitlinks.
- `git diff --cached --check` is clean.
- No staged added/modified file is larger than 50MB.
- Push the parent repo and, if relevant, run the backup script once to confirm it no longer tries to embed child worktrees or large cache files.
