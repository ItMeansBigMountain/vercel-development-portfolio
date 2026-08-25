# HeRmEz OSRS Submodule Sync Pattern

Use this when working on `/opt/data/HeRmEz/projects/osrs-plugins/*` child repos that are tracked as submodules by the parent `/opt/data/HeRmEz` control repo.

## Durable lessons

- HeRmEz is the parent control repo; OSRS plugins are child repos/submodules.
- Authenticated GitHub operations in Hermes should prefer `GITHUB_ACCESS_TOKEN` when `gh` is unavailable.
- Push child repo commits first, verify remote/local SHA, then update the parent submodule pointer and push HeRmEz.
- Parent HeRmEz often has unrelated dirty/untracked automation/video/trading files. Stage exact paths only; never broad `git add .` from the parent.
- Full `git submodule status --recursive` can be noisy if unrelated nested repos have mapping issues. For OSRS delivery verification, query the relevant OSRS submodule paths explicitly.

## Child repo push pattern

```bash
cd /opt/data/HeRmEz/projects/osrs-plugins/WhosGrindingClanPanel
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon --console=plain

git add README.md plugin.json runelite-plugin.properties src/main/java src/test/java
git diff --cached --check
git commit -m "feat: focus whos grinding panel on friends activity"
python3 - <<'PY'
import os, subprocess
remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
url = remote.replace('https://github.com/', 'https://x-access-token:' + os.environ['GITHUB_ACCESS_TOKEN'] + '@github.com/')
subprocess.check_call(['git', 'push', url, 'main'])
remote_sha = subprocess.check_output(['git', 'ls-remote', url, 'refs/heads/main'], text=True).split()[0]
local_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
print('child_remote=' + remote_sha)
print('child_local=' + local_sha)
raise SystemExit(0 if remote_sha == local_sha else 1)
PY
```

The Python URL construction avoids brittle shell quoting while still keeping the token out of normal logs when commands are summarized/redacted.

## Parent pointer update pattern

```bash
cd /opt/data/HeRmEz
git diff --submodule=log -- projects/osrs-plugins/WhosGrindingClanPanel
git add projects/osrs-plugins/WhosGrindingClanPanel
git diff --cached --stat
git commit -m "chore: update whos grinding panel submodule"
python3 - <<'PY'
import os, subprocess
remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
url = remote.replace('https://github.com/', 'https://x-access-token:' + os.environ['GITHUB_ACCESS_TOKEN'] + '@github.com/')
subprocess.check_call(['git', 'push', url, 'main'])
remote_sha = subprocess.check_output(['git', 'ls-remote', url, 'refs/heads/main'], text=True).split()[0]
local_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
print('parent_remote=' + remote_sha)
print('parent_local=' + local_sha)
raise SystemExit(0 if remote_sha == local_sha else 1)
PY
# If authenticated push succeeded but local tracking is stale, update it after verifying SHA.
git update-ref refs/remotes/origin/main HEAD
```

## Safe authentication and clean-parent fallback

Do not assume the generic token variable name. Detect **names only** without printing values, then prefer `GITHUB_ACCESS_TOKEN` in this workspace. For HTTPS Git commands, use a temporary `GIT_ASKPASS` helper that reads the token from the environment; scope `GIT_ASKPASS` and `GIT_TERMINAL_PROMPT=0` to each Git command. Never globally export an ephemeral helper path in a persistent agent shell.

If the parent workspace is dirty or its local `main` diverges from `origin/main`, do not reset, stash, merge, or commit through it merely to publish a gitlink. First fetch authenticated `origin/main` and compare ancestry. A clean clone is valid, but a very large parent checkout may time out. The efficient fallback is a temporary worktree based directly on the fetched remote tip:

```bash
cd /opt/data/HeRmEz
tmp=$(mktemp -d)
git fetch origin main
git worktree add --detach "$tmp" origin/main
cd "$tmp"
git update-index --add --cacheinfo 160000,<verified-child-sha>,<submodule-path>
git diff --cached --check
git diff --cached --name-only
git diff --cached --submodule=short
git commit -m "chore: update plugin submodule"
git push origin HEAD:main
cd /opt/data/HeRmEz
git worktree remove --force "$tmp"
```

Requirements:

- The child commit must already be pushed and remotely verified.
- The temporary worktree must start from current authenticated `origin/main` so the push is a fast-forward.
- Use `git update-index --cacheinfo 160000,...` to avoid checking out the child submodule.
- Confirm the staged diff contains exactly the intended gitlink.
- After push, verify child `main`, parent `main`, and GitHub's stored submodule `sha`; all child values must match.
- Cleanup the worktree/helper with traps where practical, but do not let cleanup hide a failed push.

## Windows handoff

For this user, provide Windows `cmd` handoff commands as one-liners only; do not use multi-line continuations.

```bat
cd C:\Users\faree\Desktop\HeRmEz && git pull origin main && git submodule sync --recursive && git submodule update --init --recursive
```

Then run an individual plugin, for example:

```bat
cd C:\Users\faree\Desktop\HeRmEz\projects\osrs-plugins\WhosGrindingClanPanel && git switch main && git pull origin main && gradlew.bat run --no-daemon
```

If full recursive update fails with a missing `.gitmodules` mapping, use `references/stale-submodule-gitlinks.md` from the parent repo before telling the user to retry.
