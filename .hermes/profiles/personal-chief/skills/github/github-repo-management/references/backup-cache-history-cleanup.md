# Backup cache history cleanup

Use this when a workspace backup push is rejected by GitHub even after generated/cache paths have been added to `.gitignore` and removed from the index with `git rm --cached`.

## Trigger

GitHub rejects a push with messages like:

- `File ... is larger than GitHub's recommended maximum file size of 50.00 MB`
- `File ... exceeds GitHub's file size limit of 100.00 MB`
- The offending paths are generated backup/runtime paths such as `.hermes/jdks`, `.hermes/.gradle`, `.hermes/sessions`, `.hermes/hermes-agent`, local SDKs, caches, logs, build outputs, or package installs.

## Pattern

If the large blobs are in **local commits that have not been pushed yet**, a normal cleanup commit is not enough: GitHub sees every blob in the push range. Rewrite the unpublished range to remove the generated paths from all ahead commits, then push.

1. Confirm the rejected large paths are not user source/data that should be preserved in Git.
2. Commit or stage the ignore/index cleanup first, so the desired end-state is known.
3. Preserve a local recovery branch before rewriting:

```bash
git branch backup/pre-ignore-cleanup-$(date +%Y%m%d%H%M%S) HEAD
```

4. Rewrite only the unpublished range (`origin/main..main`) with an index filter:

```bash
export FILTER_BRANCH_SQUELCH_WARNING=1
git filter-branch --force --index-filter '
  git rm -r --cached --ignore-unmatch \
    .hermes/.gradle .hermes/.local .hermes/.expo .hermes/jdks .hermes/tmp \
    .hermes/bin .hermes/cache .hermes/lsp .hermes/logs .hermes/sessions \
    .hermes/audio_cache .hermes/state-snapshots .hermes/ibmcloud-cli \
    .hermes/hermes-agent .hermes/credentials .hermes/secrets \
    .hermes/models_dev_cache.json >/dev/null 2>&1 || true
' --prune-empty origin/main..main
```

Adjust the path list to the specific generated/cache directories discovered in the rejection.

5. Verify there are no oversized blobs in the push range:

```bash
python3 - <<'PY'
import subprocess
objs = subprocess.check_output(['git', 'rev-list', '--objects', 'origin/main..HEAD']).decode('utf-8', 'ignore').splitlines()
large = []
for line in objs:
    oid = line.split()[0]
    path = ' '.join(line.split()[1:]) if ' ' in line else ''
    try:
        size = int(subprocess.check_output(['git', 'cat-file', '-s', oid]).decode())
    except Exception:
        continue
    if size > 50 * 1024 * 1024:
        large.append((size, path, oid))
for size, path, oid in sorted(large, reverse=True):
    print(f'{size/1024/1024:.1f} MiB {oid} {path}')
print('large_count', len(large))
PY
```

6. Push and verify the remote ref:

```bash
git push origin main
git ls-remote --heads origin main
```

7. Run the backup script once manually and verify it pushes cleanly. This confirms the ignore rules and the backup script's own rsync/Python excludes agree.

## Pitfalls

- Do not rewrite public/shared history casually. This pattern is for commits ahead of `origin/main` that were rejected and never landed remotely.
- Do not add Git LFS by default for generated caches/SDKs. The right fix is usually to stop tracking them.
- A final cleanup commit that deletes large files can still be rejected if an earlier unpublished commit in the same push introduced them.
- Keep the backup branch until the remote push and a manual backup run both succeed.
