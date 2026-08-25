# Repairing diverged backup branches with oversized generated artifacts

Use when an automated backup repository is both ahead/behind its remote and GitHub rejects a push because a generated file exceeded the 100 MB blob limit.

## Diagnose before merging

1. Check `git status --branch --short` and `git rev-list --left-right --count origin/main...main`.
2. Inspect GitHub authentication independently of branch state.
3. Read the remote rejection carefully: a non-fast-forward and a large-blob rejection are separate problems.
4. Find whether the oversized path is generated output that should be untracked rather than moved to LFS.

## Safe reconciliation pattern

When the primary checkout is dirty, avoid stashing or hard-resetting it blindly. Reconcile in a temporary clean clone:

1. Clone the remote using a noninteractive credential helper/askpass that reads a runtime token without writing it to disk.
2. Add the dirty repository as a local remote and fetch its branch.
3. Apply the net diff from local onto remote while explicitly excluding oversized generated artifacts. This avoids replaying rejected giant blobs from local history.
4. Add the generated artifact to `.gitignore` and remove it from the temporary clone's index with `git rm --cached --ignore-unmatch`.
5. Commit and push the clean net result.
6. Verify the pushed SHA with `git ls-remote`.
7. In the original checkout, authenticated-fetch the new remote head and use `git reset --mixed origin/main` only when preserving the working tree is intentional. This realigns branch history while leaving current uncommitted files intact.
8. Reapply the ignore line in the working tree if the mixed reset preserved an older local `.gitignore` copy.
9. Run the actual backup script end-to-end and verify local HEAD equals remote HEAD.

## Submodule conflict pitfall

A temporary clone made with `--no-recurse-submodules` cannot resolve a gitlink conflict using `git checkout --ours <submodule>` because no submodule commit is checked out. Capture the desired gitlink SHA before merge and resolve the index directly:

```bash
git update-index --add --cacheinfo 160000,<gitlink-sha>,path/to/submodule
```

Choose the gitlink deliberately after inspecting both trees; do not default to local or remote blindly.

## Backup authentication hardening

For scheduled HTTPS pushes, let the script create a temporary `GIT_ASKPASS` helper that prints `x-access-token` and the runtime `GITHUB_ACCESS_TOKEN`. The helper itself should contain no token and must be removed with an EXIT trap. Set `GIT_TERMINAL_PROMPT=0` so crons fail explicitly rather than hang.

## Verification

- `git rev-list --left-right --count origin/main...main` returns `0 0`.
- `git rev-parse HEAD` equals the SHA returned by authenticated `git ls-remote`.
- `git ls-files <generated-large-path>` returns nothing.
- `git check-ignore <generated-large-path>` prints the path.
- The real backup script completes and pushes successfully.
