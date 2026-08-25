# Standalone Repo Scaffold from a Workspace Project

Use this when a user asks to create a new GitHub repo after reviewing an existing project/lab inside a larger workspace.

## Pattern

1. Review the source project/lab first and write down reusable architecture, not just copy files blindly.
2. Create the new project directory under the user's active workspace, but initialize it as its own Git repo.
3. Scaffold the smallest working version with tests and a README that names the source inspiration.
4. Run the local test/CLI smoke check before publishing.
5. Create the GitHub repo using `gh repo create --source . --push` when available, or GitHub REST API + `git remote add origin` when `gh` is unavailable.
6. Add the new nested repo path to the parent workspace `.gitignore` unless the user explicitly wants a submodule or bundle backup.
7. Commit parent workspace tracker/direction updates separately from the child repo commit.
8. Verify both repos: parent `git status`, child `git status`, and latest commit hashes.

## GitHub REST fallback

```bash
TOKEN=${GITHUB_ACCESS_TOKEN:-${GITHUB_TOKEN:-${GH_TOKEN:-}}}
REPO=my-new-repo
python3 - <<'PY'
import json, os, urllib.request, urllib.error
repo = os.environ['REPO']
token = os.environ['TOKEN']
body = json.dumps({
  'name': repo,
  'description': 'Short useful description',
  'private': False,
  'auto_init': False,
}).encode()
req = urllib.request.Request(
  'https://api.github.com/user/repos',
  data=body,
  method='POST',
  headers={
    'Authorization': 'Bearer ' + token,
    'Accept': 'application/vnd.github+json',
    'Content-Type': 'application/json',
    'User-Agent': 'Hermes',
  },
)
try:
  res = json.load(urllib.request.urlopen(req, timeout=20))
except urllib.error.HTTPError as e:
  if e.code != 422:
    raise
  user = json.load(urllib.request.urlopen(urllib.request.Request(
    'https://api.github.com/user',
    headers={'Authorization': 'Bearer ' + token, 'User-Agent': 'Hermes'},
  )))['login']
  res = {'clone_url': f'https://github.com/{user}/{repo}.git', 'html_url': f'https://github.com/{user}/{repo}'}
print(res['clone_url'])
PY
```

Then:

```bash
git init -b main
git add .
git commit -m "Initial scaffold"
git remote add origin https://github.com/OWNER/$REPO.git
git push -u origin main
```

## Pitfalls

- Do not add nested `.git` directories to the parent repo; ignore the child path or intentionally use a submodule.
- Do not mix source-review notes and generated scaffold with secrets from the source project.
- Do not report the new repo as done until its tests/smoke check pass and `git push` succeeds.
