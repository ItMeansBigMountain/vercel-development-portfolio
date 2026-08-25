# Legacy project imports into a private workspace repo

Use this checklist when the user gives a directory of unfinished/legacy projects and wants them moved into the active project workspace for future deployments.

## HeRmEz layout

```text
/opt/data/HeRmEz/legacy-projects/       # original/import source; ignore after import
/opt/data/HeRmEz/projects/              # active project workspace
/opt/data/HeRmEz/projects/README.md     # deployment/manual-testing tracker
/opt/data/HeRmEz/projects/_backups/     # project backup artifacts
```

## Import checklist

1. Inspect source/target directories and parent git status.
2. List top-level legacy project names and check for name conflicts in `projects/`.
3. Copy/move projects into `projects/`; preserve original only if permissions prevent deletion.
4. Remove nested `.git` directories from imported copies unless intentionally keeping submodules.
5. Create/update `projects/README.md` with a deployment tracker table:
   - project
   - status
   - Vercel production/preview URL
   - alias/friendly URL
   - manual testing notes
6. Update parent `.gitignore` before staging:

```gitignore
/legacy-projects/
**/.git/
**/.env
**/.vercel/
**/node_modules/
**/build/
**/dist/
**/coverage/
**/__pycache__/
**/db.sqlite3
**/*.sqlite3
```

7. Stage carefully, then inspect:

```bash
git status --short --ignored | sed -n '1,160p'
git diff --cached --stat
git diff --cached --raw | awk '$3=="160000" || $4=="160000" {print}'
```

8. Run a basic secret scan on staged files. Redact obvious API keys, tokens, passwords, bearer strings, Firebase keys, local credential files, and service account material. Never print the secret values.
9. Commit/push and verify:

```bash
git commit -m "Import legacy projects into active workspace"
git push origin main
git ls-remote origin refs/heads/main
```

10. If a local DB/runtime file was staged, fix with a follow-up commit:

```bash
git rm --cached -- path/to/db.sqlite3
git add .gitignore
git commit -m "Ignore local project SQLite databases"
git push origin main
```

## Triage classification

After import, classify each project before promising deployment:

- **Immediate deploy/redeploy candidates:** have `package.json`, framework/build scripts, and existing/clear Vercel config.
- **Backend/API candidates:** Django/Flask/Express APIs needing host/database/env decisions.
- **Project-plan folders:** mostly README/PROJECT specs; require implementation before deployment.
- **Script/archive folders:** useful code/notebooks/automation; not Vercel apps until wrapped in UI/API.

## Pitfalls

- Do not use a blind `git add projects/` without reviewing staged files and ignored files.
- Do not commit `.env`, local SQLite DBs, `.vercel`, `node_modules`, generated builds, caches, media uploads, or token files.
- Do not report deploy readiness solely because a folder exists; inspect framework markers and run at least one build/check for top candidates.
