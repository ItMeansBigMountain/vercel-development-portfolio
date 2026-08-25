---
name: github-pr-workflow
description: "GitHub PR lifecycle: branch, commit, open, CI, merge."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Pull-Requests, CI/CD, Git, Automation, Merge]
    related_skills: [github-auth, github-code-review]
---

# GitHub Pull Request Workflow

Complete guide for managing the PR lifecycle. Each section shows the `gh` way first, then the `git` + `curl` fallback for machines without `gh`.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)
- Inside a git repository with a GitHub remote

### Quick Auth Detection

```bash
# Determine which method to use throughout this workflow
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  # Ensure we have a token for API/Git fallbacks. Prefer the user's Hermes token name.
  if [ -n "${GITHUB_ACCESS_TOKEN:-}" ]; then
    GITHUB_TOKEN="$GITHUB_ACCESS_TOKEN"
  elif [ -n "${GITHUB_TOKEN:-}" ]; then
    :
  elif [ -n "${GH_TOKEN:-}" ]; then
    GITHUB_TOKEN="$GH_TOKEN"
  elif [ -f ~/.hermes/.env ] && grep -q "^GITHUB_ACCESS_TOKEN=" ~/.hermes/.env; then
    GITHUB_TOKEN=$(grep "^GITHUB_ACCESS_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2- | tr -d '\n\r')
  elif [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
    GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2- | tr -d '\n\r')
  elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
    GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
  fi
fi
echo "Using: $AUTH"
```

### Extracting Owner/Repo from the Git Remote

Many `curl` commands need `owner/repo`. Extract it from the git remote:

```bash
# Works for both HTTPS and SSH remote URLs
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
echo "Owner: $OWNER, Repo: $REPO"
```

---

## 1. Branch Creation

This part is pure `git` — identical either way:

```bash
# Make sure you're up to date
git fetch origin
git checkout main && git pull origin main

# Create and switch to a new branch
git checkout -b feat/add-user-authentication
```

Branch naming conventions:
- `feat/description` — new features
- `fix/description` — bug fixes
- `refactor/description` — code restructuring
- `docs/description` — documentation
- `ci/description` — CI/CD changes

## 2. Making Commits

### Dirty working tree / unrelated local changes

When a repo already has unrelated uncommitted changes and the user asks to branch from `main`/`master` for a feature/update PR:

1. Inspect `git status --short --branch` and `git branch --list main master` first.
2. `git fetch origin`.
3. Prefer `git switch -c <feature-branch> origin/main` or `origin/master` so the new branch is explicitly based on the remote base. This carries the current working tree forward without committing unrelated work.
4. Stage only files that belong to the requested feature: `git add path1 path2 ...` — do **not** use `git add .` in a dirty repo.
5. Run targeted validation for the staged feature.
6. Commit and push the feature branch; leave unrelated pre-existing changes uncommitted and call that out in the summary.

Use the agent's file tools (`write_file`, `patch`) to make changes, then commit:

```bash
# Stage specific files
git add src/auth.py src/models/user.py tests/test_auth.py

# Commit with a conventional commit message
git commit -m "feat: add JWT-based user authentication

- Add login/register endpoints
- Add User model with password hashing
- Add auth middleware for protected routes
- Add unit tests for auth flow"
```

Commit message format (Conventional Commits):
```
type(scope): short description

Longer explanation if needed. Wrap at 72 characters.
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`, `perf`

## 3. Pushing and Creating a PR

### Push the Branch (same either way)

```bash
git push -u origin HEAD
```

### Create the PR

**With gh:**

```bash
gh pr create \
  --title "feat: add JWT-based user authentication" \
  --body "## Summary
- Adds login and register API endpoints
- JWT token generation and validation

## Test Plan
- [ ] Unit tests pass

Closes #42"
```

Options: `--draft`, `--reviewer user1,user2`, `--label "enhancement"`, `--base develop`

**With git + curl:**

```bash
BRANCH=$(git branch --show-current)

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d "{
    \"title\": \"feat: add JWT-based user authentication\",
    \"body\": \"## Summary\nAdds login and register API endpoints.\n\nCloses #42\",
    \"head\": \"$BRANCH\",
    \"base\": \"main\"
  }"
```

The response JSON includes the PR `number` — save it for later commands.

To create as a draft, add `"draft": true` to the JSON body.

### Review Every PR Feedback Surface

Before concluding that a PR has no comments or requested changes, inspect all three GitHub surfaces:

1. Issue comments: `GET /repos/{owner}/{repo}/issues/{pr}/comments` — normal PR conversation and many bot/maintainer requests.
2. Formal reviews: `GET /repos/{owner}/{repo}/pulls/{pr}/reviews` — approval/change-request state.
3. Inline review comments: `GET /repos/{owner}/{repo}/pulls/{pr}/comments` — line-specific feedback.

An empty `/pulls/{pr}/comments` response does **not** mean the PR has no feedback. Also inspect check runs for machine-generated actionable titles/details. When fixing feedback on an immutable-SHA manifest workflow, push the child change first, update the existing PR branch to the new full SHA, reply with the fix and SHA, and wait for checks again.

### RuneLite Plugin Hub submissions

For `runelite/plugin-hub`, load and follow `references/runelite-plugin-hub.md`. Two independent constraints matter:

- **One plugin per PR:** the live PR diff must contain exactly one `plugins/<plugin-id>` marker.
- **One open PR per author:** two correctly isolated PRs may still be disallowed simultaneously. Never combine plugins to work around this; prioritize one, defer the other, and preserve its child SHA/branch for later.

If reopening a closed submission returns HTTP 422 after a maintainer requests fresh artifacts, do not loop on reopening. Start a replacement branch from current upstream `master`, carry forward resolved review feedback, and verify the replacement PR's live files before reporting success.

## 4. Monitoring CI Status

### Check CI Status

**With gh:**

```bash
# One-shot check
gh pr checks

# Watch until all checks finish (polls every 10s)
gh pr checks --watch
```

**With git + curl:**

```bash
# Get the latest commit SHA on the current branch
SHA=$(git rev-parse HEAD)

# Query the combined status
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Overall: {data['state']}\")
for s in data.get('statuses', []):
    print(f\"  {s['context']}: {s['state']} - {s.get('description', '')}\")"

# Also check GitHub Actions check runs (separate endpoint)
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for cr in data.get('check_runs', []):
    print(f\"  {cr['name']}: {cr['status']} / {cr['conclusion'] or 'pending'}\")"
```

### Poll Until Complete (git + curl)

```bash
# Simple polling loop — check every 30 seconds, up to 10 minutes
SHA=$(git rev-parse HEAD)
for i in $(seq 1 20); do
  STATUS=$(curl -s \
    -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['state'])")
  echo "Check $i: $STATUS"
  if [ "$STATUS" = "success" ] || [ "$STATUS" = "failure" ] || [ "$STATUS" = "error" ]; then
    break
  fi
  sleep 30
done
```

## 5. Auto-Fixing CI Failures

When CI fails, diagnose and fix. This loop works with either auth method.

### Step 1: Get Failure Details

**With gh:**

```bash
# List recent workflow runs on this branch
gh run list --branch $(git branch --show-current) --limit 5

# View failed logs
gh run view <RUN_ID> --log-failed
```

**With git + curl:**

```bash
BRANCH=$(git branch --show-current)

# List workflow runs on this branch
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?branch=$BRANCH&per_page=5" \
  | python3 -c "
import sys, json
runs = json.load(sys.stdin)['workflow_runs']
for r in runs:
    print(f\"Run {r['id']}: {r['name']} - {r['conclusion'] or r['status']}\")"

# Get failed job logs (download as zip, extract, read)
RUN_ID=<run_id>
curl -s -L \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs \
  -o /tmp/ci-logs.zip
cd /tmp && unzip -o ci-logs.zip -d ci-logs && cat ci-logs/*.txt
```

### Step 2: Fix and Push

After identifying the issue, use file tools (`patch`, `write_file`) to fix it:

```bash
git add <fixed_files>
git commit -m "fix: resolve CI failure in <check_name>"
git push
```

### Step 3: Verify

Re-check CI status using the commands from Section 4 above.

### Auto-Fix Loop Pattern

When asked to auto-fix CI, follow this loop:

1. Check CI status → identify failures
2. Read failure logs → understand the error
3. Use `read_file` + `patch`/`write_file` → fix the code
4. `git add . && git commit -m "fix: ..." && git push`
5. Wait for CI → re-check status
6. Repeat if still failing (up to 3 attempts, then ask the user)

## 6. Merging

**With gh:**

```bash
# Squash merge + delete branch (cleanest for feature branches)
gh pr merge --squash --delete-branch

# Enable auto-merge (merges when all checks pass)
gh pr merge --auto --squash --delete-branch
```

**With git + curl:**

```bash
PR_NUMBER=<number>

# Merge the PR via API (squash)
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \
  -d "{
    \"merge_method\": \"squash\",
    \"commit_title\": \"feat: add user authentication (#$PR_NUMBER)\"
  }"

# Delete the remote branch after merge
BRANCH=$(git branch --show-current)
git push origin --delete $BRANCH

# Switch back to main locally
git checkout main && git pull origin main
git branch -d $BRANCH
```

Merge methods: `"merge"` (merge commit), `"squash"`, `"rebase"`

### Enable Auto-Merge (curl)

```bash
# Auto-merge requires the repo to have it enabled in settings.
# This uses the GraphQL API since REST doesn't support auto-merge.
PR_NODE_ID=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['node_id'])")

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/graphql \
  -d "{\"query\": \"mutation { enablePullRequestAutoMerge(input: {pullRequestId: \\\"$PR_NODE_ID\\\", mergeMethod: SQUASH}) { clientMutationId } }\"}"
```

## 7. Complete Workflow Example

```bash
# 1. Start from clean main
git checkout main && git pull origin main

# 2. Branch
git checkout -b fix/login-redirect-bug

# 3. (Agent makes code changes with file tools)

# 4. Commit
git add src/auth/login.py tests/test_login.py
git commit -m "fix: correct redirect URL after login

Preserves the ?next= parameter instead of always redirecting to /dashboard."

# 5. Push
git push -u origin HEAD

# 6. Create PR (picks gh or curl based on what's available)
# ... (see Section 3)

# 7. Monitor CI (see Section 4)

# 8. Merge when green (see Section 6)
```

## 8. Backing Up Nested Repositories Without a Remote

When a project lives as a nested git repo inside the user's main workspace and has no configured remote, do not assume `git push` from inside the nested repo will work. Back it up with a git bundle, then commit that bundle in the parent workspace if the user asked to back up the whole workspace.

```bash
# inside nested repo
PROJECT=$(basename "$PWD")
BACKUP_DIR=/opt/data/HeRmEz/projects/_backups/$PROJECT
mkdir -p "$BACKUP_DIR"
git bundle create "$BACKUP_DIR/$PROJECT.bundle" --all
git bundle verify "$BACKUP_DIR/$PROJECT.bundle"
cat > "$BACKUP_DIR/README.md" <<EOF
# $PROJECT backup

Restore:

\`\`\`bash
git clone $BACKUP_DIR/$PROJECT.bundle $PROJECT-restored
\`\`\`
EOF

# parent workspace
cd /opt/data/HeRmEz
git add "projects/_backups/$PROJECT/$PROJECT.bundle" "projects/_backups/$PROJECT/README.md"
git commit -m "chore: back up $PROJECT repo"
git push origin main
```

Before bundling media-heavy projects, commit only code/manifests/metadata in the nested repo and keep generated media ignored. If local artifact cleanup is requested, verify the bundle first, then remove disposable ignored media directories.

### Publishing exact submodule pointers from a clean clone

When the parent workspace is dirty, publish only reviewed gitlinks from an isolated clone:

1. Clone the parent to a fresh path.
2. **Run every subsequent `git update-index`, commit, and push with that clone as the actual working directory.** Creating a clone inside a shell command does not change the shell's current directory.
3. Set each exact gitlink with `git update-index --cacheinfo 160000,<full-child-sha>,<path>`.
4. Inspect `git diff --cached --submodule=short`, commit, and push.
5. Read back with `git ls-files -s <paths>` and verify the remote parent SHA.

Pitfall: if a clone succeeds but the following commit output mentions unrelated dirty files from the original workspace, stop—the command is still running in the original directory. Do not report the pointer as published until the clean clone itself has pushed it.

Pitfall on persistent-shell agents: do not globally `export GIT_ASKPASS` to an ephemeral helper that is deleted on shell exit/trap; the exported path can persist into later terminal calls and break authenticated reads. Scope it to each Git command (`GIT_ASKPASS="$helper" GIT_TERMINAL_PROMPT=0 git ...`) or explicitly `unset GIT_ASKPASS GIT_TERMINAL_PROMPT` before deleting the helper. Verify remote heads after cleanup.

Fallback for very large parent repositories: if a fresh clone times out, do not commit from a dirty or divergent current checkout. Authenticated-fetch `origin/main`, verify ancestry, then create a temporary detached worktree from the fetched remote tip (`git worktree add --detach <tmp> origin/main`). Make and inspect the single gitlink commit there, push `HEAD:main` as a fast-forward, remove the worktree, and remotely read back both the parent head and gitlink SHA.

## Useful PR Commands Reference

| Action | gh | git + curl |
|--------|-----|-----------|
| List my PRs | `gh pr list --author @me` | `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$OWNER/$REPO/pulls?state=open"` |
| View PR diff | `gh pr diff` | `git diff main...HEAD` (local) or `curl -H "Accept: application/vnd.github.diff" ...` |
| Add comment | `gh pr comment N --body "..."` | `curl -X POST .../issues/N/comments -d '{"body":"..."}'` |
| Request review | `gh pr edit N --add-reviewer user` | `curl -X POST .../pulls/N/requested_reviewers -d '{"reviewers":["user"]}'` |
| Close PR | `gh pr close N` | `curl -X PATCH .../pulls/N -d '{"state":"closed"}'` |
| Check out someone's PR | `gh pr checkout N` | `git fetch origin pull/N/head:pr-N && git checkout pr-N` |
