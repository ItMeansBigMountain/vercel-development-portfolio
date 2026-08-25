# GitHub portfolio branch correlation workflow

Use this reference when the user asks to analyze an entire GitHub account, understand each repo's branches, correlate those repos to the local `projects/` workspace, and bring missing unfinished projects local for refinement.

## Workflow

1. **Inventory GitHub repos**
   - For public repos, GitHub REST `/users/<owner>/repos?per_page=100&page=N` is enough for repo metadata.
   - For branches, prefer `git ls-remote --heads https://github.com/<owner>/<repo>.git` after the initial API pass. It avoids branch-list API rate limits and works without `gh` auth for public repos.
   - Record repo name, full name, URL, description, language, default branch, pushed date, archived/fork flags, and branch list.

2. **Inventory local projects**
   - Walk `/opt/data/HeRmEz/projects`, skipping `_` operational folders.
   - For each project, record path, whether it is a git repo, origin URL, current branch, remote branches, dirty state, top-level framework markers (`package.json`, `pyproject.toml`, `requirements.txt`, `manage.py`, `build.gradle`, `pom.xml`, `vercel.json`, README/product docs), and README hint.

3. **Correlate names and remotes**
   - Match normalized repo/project names first (`lowercase`, remove punctuation).
   - Add manual aliases for historical naming differences, e.g. `3D-React-Web` ↔ `3d-react-web`, `musicAI` ↔ `MusicAI`, `osrs-plugins-boilerplate-osrs` ↔ `osrs-plugins-boilerplate`.
   - If name matching fails, match by `origin` remote URL.

4. **Clone missing repos safely**
   - Clone missing GitHub repos into `/opt/data/HeRmEz/projects/<repo-name>`.
   - Treat each clone as a nested standalone repo unless the user explicitly asks for submodules or bundle backups.
   - Update the parent workspace `.gitignore` with `/projects/<repo-name>/` for each nested clone so the parent HeRmEz repo does not accidentally swallow nested `.git` histories.
   - Do not commit these nested repos into the parent as normal directories.

5. **Produce durable reports**
   - Write a human report such as `projects/PORTFOLIO_GITHUB_CORRELATION.md` with totals, repo→local correlations, multi-branch repos, project clusters, and unfinished/refinement candidates.
   - Write raw JSON under `projects/_ops/` for repeatable follow-up:
     - `github_repos_inventory.json`
     - `local_projects_inventory.json`
     - `github_local_correlations.json`
     - `github_missing_repos.json`
     - `unfinished_candidates.json`

## Classification hints

- Multi-branch repos need branch-aware review before declaring completeness.
- Old coursework/template branches can be clustered as archive/template material unless they have a current product direction.
- Product lanes worth surfacing for this user include OSRS/RuneLite plugins, finance/news/trading, security/networking/redteam labs, education/school CRM, music/content/AI, and legacy learning/templates.

## Pitfalls

- Do not assume default branch is `main`; some repos use `NOTES`, `master`, or a feature branch as default.
- Do not rely only on the GitHub branch API if unauthenticated; rate limits may make branches appear empty. Retry branch discovery with `git ls-remote --heads`.
- Do not ingest nested project repos into the parent workspace backup repo; ignore them, bundle them, or make real submodules deliberately.
- Do not overwrite existing local project folders when cloning; report conflicts and correlate instead.
