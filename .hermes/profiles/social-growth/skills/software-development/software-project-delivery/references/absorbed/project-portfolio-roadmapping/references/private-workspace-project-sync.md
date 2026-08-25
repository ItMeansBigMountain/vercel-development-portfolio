# Private HeRmEz workspace project-sync pattern

Use this reference when the user asks to keep `/opt/data/HeRmEz/projects` current because they clone the private HeRmEz repo locally to grab project code.

## User workflow

- The private GitHub repo `ItMeansBigMountain/HeRmEz` is the user's durable workspace/backup surface.
- The user expects useful project artifacts, reports, repo maps, and handoff docs to live under `/opt/data/HeRmEz/projects` so they can clone/pull HeRmEz locally and inspect code or references.
- Security boundary, per the user: treat the private GitHub repo as the outer sharing boundary; still do not commit raw secrets/tokens.

## Update cadence pattern

When a session creates or imports project code:

1. Put durable outputs under `/opt/data/HeRmEz/projects` or `projects/_ops/`, not random temp paths.
2. For nested standalone repos under `projects/`, keep each repo's own `.git` and remote intact.
3. Add nested standalone repo paths to the parent `/opt/data/HeRmEz/.gitignore` unless the user explicitly asks for submodules or vendoring.
4. If you modify a nested child repo, commit/push inside that child repo first. Then update parent workspace docs/reports/maps and commit/push the parent if requested.
5. For repo refreshes, run or create a deterministic updater such as `/opt/data/scripts/update_projects_repos.sh` that walks `projects/`, detects nested `.git` dirs, runs `git fetch --all --prune`, and writes logs under `projects/_ops/update-logs/`.
6. Before telling the user code is ready to pull, verify with `git status`, remote URL, current branch, and a real push/remote check where relevant.

## What to save in parent HeRmEz

Good parent-tracked artifacts:

- Portfolio reports (`projects/PORTFOLIO_GITHUB_CORRELATION.md`).
- Repo correlation maps under `projects/_ops/`.
- Completion plans, README updates, and product direction docs.
- Update logs when they are useful for audit/handoff.

Avoid parent-tracking:

- Nested repo source trees as ordinary files.
- `.git/` internals from child repos.
- API keys, `.env` files, OAuth tokens, or token-bearing logs.
