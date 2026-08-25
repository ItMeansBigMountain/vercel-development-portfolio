# Consolidating related workspace projects into a child repo submodule

Use this when the user asks to make a new GitHub repo from several existing workspace codebases and place that repo back under `/opt/data/HeRmEz/projects` as a submodule.

## Recommended sequence

1. Inspect the target directories first. The user may phrase this as "ls/check your internal files"; do a real file inventory before and after copy.
2. Create a clean child repo directory under `/opt/data/HeRmEz/projects/<repo-name>`.
3. Preserve any pre-existing files at that child path under a `legacy-existing/` folder instead of deleting them silently.
4. Copy the requested codebases into named subfolders.
5. Exclude by default:
   - `.git/`, `.env*`, secrets, tokens, credentials.
   - generated media/source folders: `videos/`, `EXPORTS/`, `SOURCES/`, `TMP/`, upload queues.
   - analytics/log/upload ledgers if they contain runtime/account data.
   - caches/deps: `__pycache__/`, `.pytest_cache/`, `node_modules/`, `.venv/`.
   - media binaries: `*.mp4`, `*.mp3`, `*.wav`, `*.mov`, `*.webm`, common image formats.
6. Add a README explaining included subfolders and excluded runtime artifacts.
7. Search/verify before commit:
   - no media files slipped in.
   - no `*token*` / credential files slipped in.
   - no large files over the repo policy threshold.
   - top-level/internal files look correct.
8. Initialize/commit/push the child repo. Verify local SHA equals remote SHA using token-backed `git ls-remote` if normal auth is not configured.
9. In the parent HeRmEz repo:
   - `git rm -r --cached <path>` if the path was previously tracked as normal files.
   - ensure `.gitmodules` has the child path and remote URL.
   - `git add .gitmodules <path>` so the path is staged as a `160000` gitlink.
   - run `git submodule absorbgitdirs <path>` when converting an existing nested worktree.
   - verify with `git submodule status <path>` and `git ls-files -s <path>`.
10. Commit/push only the parent submodule pointer and `.gitmodules` change, not unrelated dirty workspace files.

## Pitfalls

- Do not just copy folders and commit them inside the parent repo when the user asked for a submodule.
- Do not delete pre-existing child-path files; preserve them under `legacy-existing/` unless the user explicitly says to discard.
- Do not report success until both child and parent remote SHAs are verified.
- If `rsync` is missing, use Python `shutil.copytree(..., ignore=...)`; do not stop at the missing binary.