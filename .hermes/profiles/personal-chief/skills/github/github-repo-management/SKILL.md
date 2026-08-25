---
name: github-repo-management
description: "Clone/create/fork repos; manage remotes, releases."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Repositories, Git, Releases, Secrets, Configuration]
    related_skills: [github-auth, github-pr-workflow, github-issues]
---

# GitHub Repository Management

Create, clone, fork, configure, and manage GitHub repositories. Each section shows `gh` first, then the `git` + `curl` fallback.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)

### Setup

For this user's Hermes/HeRmEz workspace, prefer `GITHUB_ACCESS_TOKEN` for authenticated GitHub API and push operations. Do not claim GitHub access is unavailable just because `gh` is missing; try the token-backed curl/git fallback first.

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  # Prefer the user's durable Hermes GitHub token name before generic gh/GitHub names.
  if [ -n "${GITHUB_ACCESS_TOKEN:-}" ]; then
    GITHUB_TOKEN="$GITHUB_ACCESS_TOKEN"
  elif [ -n "${GITHUB_TOKEN:-}" ]; then
    GITHUB_TOKEN="$GITHUB_TOKEN"
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

# Get your GitHub username (needed for several operations). Do not claim GitHub access is unavailable just because gh is missing;
# use the token-backed curl/API fallback first, especially GITHUB_ACCESS_TOKEN in Hermes sessions.
if [ "$AUTH" = "gh" ]; then
  GH_USER=$(gh api user --jq '.login')
else
  GH_USER=$(curl -fsS -H "Authorization: Bearer $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")
fi
```

If you're inside a repo already:

```bash
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

---

## 1. Cloning Repositories

Cloning is pure `git` — works identically either way:

```bash
# Clone via HTTPS (works with credential helper or token-embedded URL)
git clone https://github.com/owner/repo-name.git

# Clone into a specific directory
git clone https://github.com/owner/repo-name.git ./my-local-dir

# Shallow clone (faster for large repos)
git clone --depth 1 https://github.com/owner/repo-name.git

# Clone a specific branch
git clone --branch develop https://github.com/owner/repo-name.git

# Clone via SSH (if SSH is configured)
git clone git@github.com:owner/repo-name.git
```

**With gh (shorthand):**

```bash
gh repo clone owner/repo-name
gh repo clone owner/repo-name -- --depth 1
```

## 2. Creating Repositories

**With gh:**

```bash
# Create a public repo and clone it
gh repo create my-new-project --public --clone

# Private, with description and license
gh repo create my-new-project --private --description "A useful tool" --license MIT --clone

# Under an organization
gh repo create my-org/my-new-project --public --clone

# From existing local directory
# Preflight: from the intended child directory, verify `git rev-parse --show-toplevel`
# resolves to that child—not a surrounding portfolio repository. Scaffolders may inherit
# the parent Git root. Initialize the child repo before staging if it is meant to stand alone.
cd /path/to/existing/project
gh repo create my-project --source . --public --push
```

**With git + curl:**

```bash
# Create the remote repo via API
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{
    "name": "my-new-project",
    "description": "A useful tool",
    "private": false,
    "auto_init": true,
    "license_template": "mit"
  }'

# Clone it
git clone https://github.com/$GH_USER/my-new-project.git
cd my-new-project

# -- OR -- push an existing local directory to the new repo
cd /path/to/existing/project
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/$GH_USER/my-new-project.git
git push -u origin main
```

To create under an organization:

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/orgs/my-org/repos \
  -d '{"name": "my-new-project", "private": false}'
```

### From a Template

**With gh:**

```bash
gh repo create my-new-app --template owner/template-repo --public --clone
```

**With curl:**

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/template-repo/generate \
  -d '{"owner": "'"$GH_USER"'", "name": "my-new-app", "private": false}'
```

## 3. Forking Repositories

**With gh:**

```bash
gh repo fork owner/repo-name --clone
```

**With git + curl:**

```bash
# Create the fork via API
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo-name/forks

# Wait a moment for GitHub to create it, then clone
sleep 3
git clone https://github.com/$GH_USER/repo-name.git
cd repo-name

# Add the original repo as "upstream" remote
git remote add upstream https://github.com/owner/repo-name.git
```

### Keeping a Fork in Sync

```bash
# Pure git — works everywhere
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

**With gh (shortcut):**

```bash
gh repo sync $GH_USER/repo-name
```

## 4. Repository Information

**With gh:**

```bash
gh repo view owner/repo-name
gh repo list --limit 20
gh search repos "machine learning" --language python --sort stars
```

**With curl:**

```bash
# View repo details
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO \
  | python3 -c "
import sys, json
r = json.load(sys.stdin)
print(f\"Name: {r['full_name']}\")
print(f\"Description: {r['description']}\")
print(f\"Stars: {r['stargazers_count']}  Forks: {r['forks_count']}\")
print(f\"Default branch: {r['default_branch']}\")
print(f\"Language: {r['language']}\")"

# List your repos
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/user/repos?per_page=20&sort=updated" \
  | python3 -c "
import sys, json
for r in json.load(sys.stdin):
    vis = 'private' if r['private'] else 'public'
    print(f\"  {r['full_name']:40}  {vis:8}  {r.get('language', ''):10}  ★{r['stargazers_count']}\")"

# Search repos
curl -s \
  "https://api.github.com/search/repositories?q=machine+learning+language:python&sort=stars&per_page=10" \
  | python3 -c "
import sys, json
for r in json.load(sys.stdin)['items']:
    print(f\"  {r['full_name']:40}  ★{r['stargazers_count']:6}  {r['description'][:60] if r['description'] else ''}\")"
```

## 5. Repository Cleanup / Deletion

Use this when the user asks to clean up unused GitHub repositories. Deletion is irreversible, so do not delete from an inferred list without explicit confirmation of the exact repos.

Recommended sequence:

1. Inventory candidate repos with the GitHub API/gh, including `full_name`, URL, description, `archived`, `private`, and `updated_at`.
2. Correlate against the active local workspace (directories, `.gitmodules`, remotes) before classifying repos as unused.
3. Present two explicit lists: **keep** and **delete/archive candidates**.
4. Ask for confirmation before destructive deletion; archiving is safer if the user is uncertain.
5. If the user explicitly names the exact repository/project and says to delete or scrap it, that is final confirmation; verify the local remote and GitHub `full_name` match before acting rather than asking again.
6. For deletion with curl/API, call `DELETE /repos/{owner}/{repo}` and expect HTTP `204`.
7. Verify each deleted repo by `GET /repos/{owner}/{repo}` returning `404`, then re-list related repos to prove only the active set remains.
8. When the deleted repo is a parent-workspace submodule, clean both sides: `git submodule deinit -f`, `git rm -f`, remove stale `.git/modules/...`, verify `.gitmodules` and the parent index no longer contain it, and publish the narrow parent change without staging unrelated work.
9. Scan active planning/status documents and dedicated generated logs for stale references. Update or remove current-state references, but preserve clearly dated historical audits/error reports as history unless the user explicitly requests history rewriting.
10. Update any workspace cleanup docs/tracking files and commit/push those docs separately from unrelated dirty work.

Pitfalls:

- Do not delete repositories solely because they are not currently cloned; confirm they are not active templates, plugin-hub repos, or canonical remotes used by a renamed local submodule.
- When a repo was just renamed, keep the renamed repo and treat the old name as gone/redirected; update local submodule URLs before classifying anything as unused.
- Avoid broad `git add .` in a large workspace after cleanup; stage only the docs/submodule paths relevant to the repo cleanup.

## 6. Repository Renames and Hosted-App Continuity

When the user wants the same project under a new repository name, prefer a GitHub rename over creating a duplicate repository. This preserves commit history, issues, stars, redirects, and deployment linkage.

1. Verify the intended destination name does not already exist and the source repository is the expected remote.
2. Require a clean local tree and verify local `HEAD` equals the current remote default-branch SHA.
3. Rename through `gh repo rename NEW_NAME` or `PATCH /repos/{owner}/{old}` with `{ "name": "NEW_NAME" }`.
4. Update the local `origin` to the new canonical URL even though GitHub provides redirects.
5. Verify the new repository URL, default branch, visibility, and remote SHA; do not treat the redirect alone as final verification.
6. For connected hosting platforms, rename/relink the hosted project separately. Repository renames do not guarantee project aliases, primary domains, deployment-protection rules, or environment settings migrate as intended.
7. Preserve the old public deployment alias when useful for compatibility, but establish and verify a new canonical alias.
8. If an authenticated shell header is rewritten by credential redaction, use a short Python `urllib.request`/`subprocess` client that reads the token from `os.environ` internally. Never interpolate or print the token.

For Vercel-specific project rename, alias, and SSO-protection handling, use the cloud deployment umbrella's `references/vercel-project-rename-and-alias-migration.md`.

## 7. Repository Settings

**With gh:**

```bash
gh repo edit --description "Updated description" --visibility public
gh repo edit --enable-wiki=false --enable-issues=true
gh repo edit --default-branch main
gh repo edit --add-topic "machine-learning,python"
gh repo edit --enable-auto-merge
```

**With curl:**

```bash
curl -s -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO \
  -d '{
    "description": "Updated description",
    "has_wiki": false,
    "has_issues": true,
    "allow_auto_merge": true
  }'

# Update topics
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.mercy-preview+json" \
  https://api.github.com/repos/$OWNER/$REPO/topics \
  -d '{"names": ["machine-learning", "python", "automation"]}'
```

## 6. Branch Protection

```bash
# View current protection
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection

# Set up branch protection
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": ["ci/test", "ci/lint"]
    },
    "enforce_admins": false,
    "required_pull_request_reviews": {
      "required_approving_review_count": 1
    },
    "restrictions": null
  }'
```

## 7. Secrets Management (GitHub Actions)

**With gh:**

```bash
gh secret set API_KEY --body "your-secret-value"
gh secret set SSH_KEY < ~/.ssh/id_rsa
gh secret list
gh secret delete API_KEY
```

**With curl:**

Secrets require encryption with the repo's public key — more involved via API:

```bash
# Get the repo's public key for encrypting secrets
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/secrets/public-key

# Encrypt and set (requires Python with PyNaCl)
python3 -c "
from base64 import b64encode
from nacl import encoding, public
import json, sys

# Get the public key
key_id = '<key_id_from_above>'
public_key = '<base64_key_from_above>'

# Encrypt
sealed = public.SealedBox(
    public.PublicKey(public_key.encode('utf-8'), encoding.Base64Encoder)
).encrypt('your-secret-value'.encode('utf-8'))
print(json.dumps({
    'encrypted_value': b64encode(sealed).decode('utf-8'),
    'key_id': key_id
}))"

# Then PUT the encrypted secret
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/secrets/API_KEY \
  -d '<output from python script above>'

# List secrets (names only, values hidden)
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/secrets \
  | python3 -c "
import sys, json
for s in json.load(sys.stdin)['secrets']:
    print(f\"  {s['name']:30}  updated: {s['updated_at']}\")"
```

Note: For secrets, `gh secret set` is dramatically simpler. If setting secrets is needed and `gh` isn't available, recommend installing it for just that operation.

## 8. Backing Up Nested Repositories into a Parent Private Repo

When a user wants an active project backed up inside a larger private workspace repo, first check whether the project is itself a Git repo. If it is nested inside the parent repo, prefer a **Git bundle** committed to the parent repo over trying to `git add` the nested worktree directly.

When auditing a broad automated Git backup, use `references/git-backup-hygiene-audits.md`: classify human-authored/recovery-defining state versus reproducible machine state, inspect gitlinks separately from ordinary tracked files, harden both copier exclusions and `.gitignore`, add a fail-closed staged-content gate, and validate with a command-scoped temporary index. For an approved cleanup of files that are already tracked but now ignored, the same reference contains the index-only `git rm --cached` workflow, nested-ignore diagnostics, durable false-positive restoration, submodule invariants, and divergence-safe publication procedure. Treat future-ignore policy, current index cleanup, historical compaction, and remote publication as separate approval/verification scopes.

If the user explicitly asks to make inner repos submodules, use real Git submodules instead of bundles: register each child path in `.gitmodules`, stage the child path as a `160000` gitlink, run `git submodule absorbgitdirs` for existing nested worktrees, and verify with `git submodule status` plus `git ls-files -s`. See `references/nested-repo-submodules-and-backup-cache-hygiene.md` for the command pattern and backup-cache cleanup checklist. When consolidating multiple existing workspace codebases into one new child repo and then placing that child back under `/opt/data/HeRmEz/projects` as a submodule, use `references/consolidated-child-repo-submodule.md`: inspect internal files before/after copy, preserve any pre-existing target files under `legacy-existing/`, exclude media/runtime/secrets, push/verify the child, then stage the parent gitlink.

When consolidating malware, phishing, exploit, leaked, or other dual-use research repositories into an attributed source monorepo, use `references/security-research-source-monorepos.md`: pin provenance, preserve per-folder licensing and original bytes, scan statically without execution, default to private for sensitive/no-license collections, and verify the remote tree through GitHub API readback.

Recommended sequence:

1. In the child repo, verify status, remote, branch, and latest commit.
2. From the child repo, create a bundle under the parent workspace's project backup directory, typically `git bundle create <parent>/projects/_backups/<name>/<name>.bundle --all`. For this user's HeRmEz workspace, project backup artifacts belong under `/opt/data/HeRmEz/projects/_backups/`, not under `.hermes/`.
3. Add a small README next to the bundle documenting source path, remote URL, branch, latest commit, and restore commands.
4. Add the active nested worktree path to the parent repo's `.gitignore` so runtime files, local DBs, media uploads, caches, and nested `.git` internals do not get tracked accidentally while the bundle/README remain tracked.
5. Verify the bundle with `git bundle verify` **and** by cloning it into `/tmp` and checking expected files.
6. Commit and push only the bundle, README, and parent `.gitignore` change.
7. Verify the parent remote with `git ls-remote origin refs/heads/main`.

See `references/nested-repo-backup-bundles.md` for a concrete command template and restore verification pattern, including the user's preferred `/opt/data/HeRmEz/projects/_backups/` layout. See `references/nested-repo-submodules-and-backup-cache-hygiene.md` when the user explicitly wants nested repos to remain live submodules and when backup scripts need cache/runtime exclusions. For the user's active HeRmEz OSRS plugin workspace, see `references/hermez-osrs-submodule-sync.md`: use `GITHUB_ACCESS_TOKEN`, push child plugin repos first, verify remote/local SHAs, stage exact parent submodule pointers only, and then push the HeRmEz control repo.

For broader imports of many unfinished legacy folders into the private workspace, use `references/legacy-project-imports.md` and treat the work as a secure migration: inventory, ignore runtime artifacts, remove nested git internals, secret-scan, create a deployment URL tracker, then commit/push.

When the user asks to create a **new standalone repo after reviewing an existing workspace project/lab**, use `references/standalone-repo-from-workspace.md`: review source architecture, scaffold a tested MVP, publish the child repo, ignore the child worktree in the parent repo unless a submodule/bundle is intended, then commit parent trackers separately.

### Pitfalls

- Do not assume `git add projects/foo/` is a safe backup if `projects/foo` is itself a Git repo; it can become submodule-like or miss the intended history.
- A bundle captures committed Git history, not dirty working tree changes. If the child repo has uncommitted changes, commit them in the child first or explicitly tell the user what is not captured.
- Do not bundle or track secrets, local SQLite DBs, uploaded media, caches, or environment files unless the user explicitly asks for a full machine/runtime snapshot and approves the security implications.
- If a parent backup push is rejected for large `.hermes`/cache/runtime files, do not push harder or add Git LFS by default. Remove those artifacts from the index with `git rm --cached`, add ignore/exclude rules, verify no staged additions exceed 50MB, then recommit and rerun the backup script.
- If the push is still rejected after `git rm --cached`, inspect whether the large blobs live in earlier local commits that are ahead of the remote. For unpublished commits only, create a local backup branch, rewrite `origin/main..main` with an index-filter that removes the generated/cache paths, verify `git rev-list --objects origin/main..HEAD` contains no objects over 50MB, then push and manually run the backup script once. See `references/backup-cache-history-cleanup.md` for the exact recovery recipe and verification script.
- When deleting unused GitHub repositories, especially portfolio cleanup repos, first list all candidate repos, correlate them against active local project/submodule paths, present explicit keep/delete lists, and get final user confirmation. After deletion, verify each repo returns 404/gone and re-scan the remaining repo list before reporting success.
- When updating Hermes Agent itself from a gateway chat, `hermes update` may update code successfully but refuse an in-process gateway restart. Report that the gateway must be restarted from an external shell rather than attempting restart loops from inside Discord/Telegram.
- When converting existing nested worktrees to submodules, do not just edit `.gitmodules`; stage the child path as a gitlink and run `git submodule absorbgitdirs` so clones understand the submodule relationship. When consolidating two submodule-backed child repos into one, push the surviving child repo commit first, then remove the obsolete submodule from the parent with `git submodule deinit -f <path>`, `git rm -f <path>`, cleanup `.git/modules/<path>`, stage `.gitmodules` plus the surviving submodule pointer, and commit/push the parent. For Windows handoff after parent pull, include `git submodule sync --recursive` and `git submodule update --init --recursive <surviving-path>`; plain `git pull` is not enough to populate/update submodule contents. If recursive submodule operations fail with `No url found for submodule path ... in .gitmodules` or `no submodule mapping found`, see `references/stale-submodule-gitlinks.md`: inspect the local folder, ensure it is ignored if it is a standalone project, remove the stale parent gitlink with `git rm --cached -f <path>`, then rerun full recursive status/update checks.
- In Hermes sessions for this user, prefer `GITHUB_ACCESS_TOKEN` for authenticated GitHub API/git tasks. When `gh` is unavailable, build authenticated push/verify URLs without printing the token, and verify `git ls-remote <auth-url> refs/heads/<branch>` equals `git rev-parse HEAD`. If shell quoting around token URL construction becomes fragile, use a short Python `subprocess` snippet that constructs `url = 'https://x-access-token:' + os.environ['GITHUB_ACCESS_TOKEN'] + '@github.com/' + remote.split('github.com/', 1)[1]` and passes it directly to `git push`/`git ls-remote`.
- For this user's HeRmEz workspace submodule updates, push and verify each child repo first, then stage only the child path gitlink in `/opt/data/HeRmEz` plus any intentional OSRS docs. Do not use broad `git add .` in HeRmEz because the control repo commonly has unrelated dirty automation/trading/video files. Build authenticated push URLs from the existing remote plus `GITHUB_ACCESS_TOKEN`, then verify `git ls-remote <auth-url> refs/heads/<branch>` equals `git rev-parse HEAD`. If unauthenticated `git fetch origin` fails after an authenticated push, update local tracking with `git update-ref refs/remotes/origin/main HEAD` only after remote/local SHA equality is proven.
- For token-authenticated GitHub work in Hermes sessions, prefer the durable `GITHUB_ACCESS_TOKEN` fallback even when `gh` is absent. When pushing with an embedded token, avoid brittle shell quoting; use a small Python snippet to build `https://x-access-token:${TOKEN}@github.com/...`, run `git push`, then verify with `git ls-remote`. After a verified token-backed push, if ordinary `git fetch origin` fails because no credential helper is configured, it is acceptable to update the local tracking ref with `git update-ref refs/remotes/origin/<branch> HEAD` so `git status` reflects the verified remote state.
- For submodule pointer updates: build/test and push the child repo first, verify child local SHA equals remote SHA, then stage exactly the parent submodule path (the gitlink) and any intended docs. Do not stage unrelated dirty files from the parent workspace; use exact pathspecs and verify `git diff --cached --stat` before committing.
- If a parent/control-repo push is blocked by unrelated unpublished commits or the local parent has diverged from remote, do not rewrite, discard, stash, merge, or force-push that unrelated history merely to publish submodule pointers. Fetch authenticated `origin/main`, verify ancestry, and publish from an isolated checkout based on the remote tip. Prefer a clean temporary clone; if the parent is very large and clone/checkout is too slow, use `git worktree add --detach <tmp> origin/main`. In the isolated checkout, use `git update-index --add --cacheinfo 160000,<verified-child-sha>,<submodule-path>`, inspect the exact staged gitlink, commit, and push `HEAD:main`. Verify remote parent SHA and GitHub's stored submodule SHA afterward. See `references/hermez-osrs-submodule-sync.md`.
- When token URLs are mangled by command redaction or shell quoting, avoid embedding the token in the command. Use an ephemeral `GIT_ASKPASS` helper outside all repositories that returns `x-access-token` for username and reads `GITHUB_ACCESS_TOKEN` for password; run with `GIT_TERMINAL_PROMPT=0`, restrictive permissions, and never commit the helper.
- For this user, when handing off commands for Windows `cmd`, provide single-line commands only. Avoid backslash/caret continuations and multi-line command blocks; chain steps with `&&` instead.

## 9. Importing Legacy Project Collections into a Workspace

Use this when the user provides a folder such as `legacy-projects/` and wants unfinished apps moved into the active workspace `projects/` directory for future development/deployment. For this user's HeRmEz workspace, active project work belongs under `/opt/data/HeRmEz/projects`, project backups under `/opt/data/HeRmEz/projects/_backups`, and deployment/manual-testing tracking belongs in `/opt/data/HeRmEz/projects/README.md`.

Recommended sequence:

1. Inspect the source and destination directories before moving anything; verify requested paths that may differ from the mounted path in the current environment.
2. Move/copy each legacy app into a top-level folder under `projects/`, preserving existing destination folders and documenting conflicts instead of overwriting blindly.
3. Create or update `projects/README.md` as a Vercel/manual-testing tracker with columns for project, local path, type, status, production URL, preview URL, and notes/next step.
4. Add ignore rules before staging: `.env`, `.vercel/`, `node_modules/`, build outputs, caches, SQLite DBs, and the original `legacy-projects/` source copy if it remains on disk.
5. Remove nested `.git/` directories from imported project copies unless submodules are explicitly intended; verify no gitlinks are staged.
6. Stage the import, then run a staged-content secret scan before committing. Sanitize hardcoded credentials/API keys/passwords/SECRET_KEY values to placeholders and restage.
7. If local DBs were accidentally staged, add `**/db.sqlite3` and `**/*.sqlite3`, then `git rm --cached` the tracked DB files before the final push.
8. Commit/push and verify with `git ls-remote origin refs/heads/main`.

See `references/legacy-project-imports.md` for a concrete command template, staged secret scan, and README tracker guidance.

### Pitfalls

- Do not commit `.env`, `.vercel`, `node_modules`, build folders, SQLite DBs, runtime tokens, or generated caches.
- Do not quote discovered secret values in user-facing replies or persistent notes; report that credentials were sanitized.
- Scan staged content, not only the working tree, because large imports and duplicated legacy archives can hide old secrets in notebooks, docs, and scripts.
- If the user mentions a Docker host path that is not mounted, verify and use the active workspace path rather than failing or pretending the path exists.

## 10. Releases

**With gh:**

```bash
gh release create v1.0.0 --title "v1.0.0" --generate-notes
gh release create v2.0.0-rc1 --draft --prerelease --generate-notes
gh release create v1.0.0 ./dist/binary --title "v1.0.0" --notes "Release notes"
gh release list
gh release download v1.0.0 --dir ./downloads
```

**With curl:**

```bash
# Create a release
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  -d '{
    "tag_name": "v1.0.0",
    "name": "v1.0.0",
    "body": "## Changelog\n- Feature A\n- Bug fix B",
    "draft": false,
    "prerelease": false,
    "generate_release_notes": true
  }'

# List releases
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  | python3 -c "
import sys, json
for r in json.load(sys.stdin):
    tag = r.get('tag_name', 'no tag')
    print(f\"  {tag:15}  {r['name']:30}  {'draft' if r['draft'] else 'published'}\")"

# Upload a release asset (binary file)
RELEASE_ID=<id_from_create_response>
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  "https://uploads.github.com/repos/$OWNER/$REPO/releases/$RELEASE_ID/assets?name=binary-amd64" \
  --data-binary @./dist/binary-amd64
```

## 11. GitHub Pages for Static Sites

Use this when publishing a simple static site (plain HTML/CSS/JS) to GitHub Pages.

### Recommended sequence

1. Create or reuse a public repo.
2. Commit the static site at the repository root, with `index.html` in `/`.
3. Push to `main`.
4. Enable Pages from the `main` branch and `/` root.
5. Poll the Pages URL until it returns HTTP 200; first deploys commonly return 404 for a minute or two.
6. Verify key pages and static assets over the live `github.io` URL.

### With gh

```bash
cd /path/to/static-site
OWNER=$(gh api user --jq '.login')
REPO=my-static-site

gh repo create "$REPO" --public --source . --push

gh api -X POST \
  "/repos/$OWNER/$REPO/pages" \
  -f source[branch]=main \
  -f source[path]=/

PAGES_URL="https://${OWNER,,}.github.io/$REPO/"
for i in {1..24}; do
  if curl -fsS "$PAGES_URL" | grep -q '<title>'; then
    echo "Live: $PAGES_URL"
    break
  fi
  sleep 5
done
```

### With git + curl fallback

Use this path when `gh` is unavailable but a token exists in `GITHUB_TOKEN`, `GH_TOKEN`, or `~/.git-credentials`.

```bash
cd /path/to/static-site
REPO=my-static-site
TOKEN=${GITHUB_TOKEN:-${GH_TOKEN:-}}
if [ -z "$TOKEN" ] && [ -f ~/.git-credentials ]; then
  TOKEN=$(grep github.com ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@github.com.*|\1|')
fi
OWNER=$(curl -fsS -H "Authorization: Bearer $TOKEN" https://api.github.com/user | python3 -c 'import sys,json; print(json.load(sys.stdin)["login"])')

curl -fsS -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO\",\"private\":false,\"auto_init\":false}" || true

git init
git branch -M main
git add .
git commit -m "Launch static site" || true
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$OWNER/$REPO.git"
git push -u origin main

curl -fsS -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$OWNER/$REPO/pages" \
  -d '{"source":{"branch":"main","path":"/"}}'

PAGES_URL="https://$(echo "$OWNER" | tr '[:upper:]' '[:lower:]').github.io/$REPO/"
for i in {1..24}; do
  if curl -fsS "$PAGES_URL" >/tmp/pages-index.html 2>/dev/null; then
    echo "Live: $PAGES_URL"
    break
  fi
  sleep 5
done
```

### Pitfalls

- A newly enabled Pages site can return `404 Not Found` briefly even after the API returns success; poll before reporting failure.
- GitHub Pages username/organization subdomains are lowercase even when the account login has uppercase letters.
- For plain static sites, keep `index.html` at repository root if Pages source path is `/`.
- Verify the deployed site over HTTPS, not only the local files: homepage, secondary pages, CSS, JS, images, and important external links.
- If adding client-provided external links, place them in a visible section as well as the footer/social icons when the user asks for “side links” or “additional links.”

## 12. GitHub Actions Workflows

**With gh:**

```bash
gh workflow list
gh run list --limit 10
gh run view <RUN_ID>
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID>
gh run rerun <RUN_ID> --failed
gh workflow run ci.yml --ref main
gh workflow run deploy.yml -f environment=staging
```

**With curl:**

```bash
# List workflows
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/workflows \
  | python3 -c "
import sys, json
for w in json.load(sys.stdin)['workflows']:
    print(f\"  {w['id']:10}  {w['name']:30}  {w['state']}\")"

# List recent runs
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?per_page=10" \
  | python3 -c "
import sys, json
for r in json.load(sys.stdin)['workflow_runs']:
    print(f\"  Run {r['id']}  {r['name']:30}  {r['conclusion'] or r['status']}\")"

# Download failed run logs
RUN_ID=<run_id>
curl -s -L \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs \
  -o /tmp/ci-logs.zip
cd /tmp && unzip -o ci-logs.zip -d ci-logs

# Re-run a failed workflow
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/rerun

# Re-run only failed jobs
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/rerun-failed-jobs

# Trigger a workflow manually (workflow_dispatch)
WORKFLOW_ID=<workflow_id_or_filename>
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/workflows/$WORKFLOW_ID/dispatches \
  -d '{"ref": "main", "inputs": {"environment": "staging"}}'
```

## 13. Gists

**With gh:**

```bash
gh gist create script.py --public --desc "Useful script"
gh gist list
```

**With curl:**

```bash
# Create a gist
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/gists \
  -d '{
    "description": "Useful script",
    "public": true,
    "files": {
      "script.py": {"content": "print(\"hello\")"}
    }
  }'

# List your gists
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/gists \
  | python3 -c "
import sys, json
for g in json.load(sys.stdin):
    files = ', '.join(g['files'].keys())
    print(f\"  {g['id']}  {g['description'] or '(no desc)':40}  {files}\")"
```

## Quick Reference Table

| Action | gh | git + curl |
|--------|-----|-----------|
| Clone | `gh repo clone o/r` | `git clone https://github.com/o/r.git` |
| Create repo | `gh repo create name --public` | `curl POST /user/repos` |
| Fork | `gh repo fork o/r --clone` | `curl POST /repos/o/r/forks` + `git clone` |
| Repo info | `gh repo view o/r` | `curl GET /repos/o/r` |
| Edit settings | `gh repo edit --...` | `curl PATCH /repos/o/r` |
| Create release | `gh release create v1.0` | `curl POST /repos/o/r/releases` |
| List workflows | `gh workflow list` | `curl GET /repos/o/r/actions/workflows` |
| Rerun CI | `gh run rerun ID` | `curl POST /repos/o/r/actions/runs/ID/rerun` |
| Set secret | `gh secret set KEY` | `curl PUT /repos/o/r/actions/secrets/KEY` (+ encryption) |
