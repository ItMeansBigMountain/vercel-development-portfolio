# Git Backup Hygiene Audits

Use this when a broad parent/control repository is used as an automated backup of projects or agent state. The goal is to preserve human-authored and recovery-defining material without turning Git into a machine image.

## Classification

### Back up

- Source, tests, documentation, migrations, and deliberate assets
- Dependency manifests and lockfiles
- Deployment/configuration templates with secrets removed
- Git submodule pointers and `.gitmodules`
- Agent skills, scripts, hooks, plugin source/config, cron definitions, and profile preferences
- Curated runbooks, trackers, decision records, and post-task/post-trade summaries
- Deliberate Git bundles with a README and restore instructions

### Usually omit

- Dependency stores and downloaded SDKs: `node_modules`, virtualenvs, NuGet, Dotnet, Gradle, Terraform providers
- Build/provider state: `.next`, `dist`, `build`, coverage, `.terraform`, `.vercel`, `.angular`, Turbo caches
- Sessions, logs, process files, locks, PIDs, sockets, scratch workspaces, temporary clones
- Runtime databases and journals: SQLite, WAL, SHM, corruption snapshots
- Generated/downloaded media and render output
- OAuth pending callbacks, tokens, credentials, auth files, private keys
- Root-level dated collectors, raw API responses, temporary analyzers, and intermediate reports

Do not blanket-ignore a domain directory such as a trading journal when it mixes raw output with durable decisions. Classify within it: retain curated summaries and reusable scripts; omit reproducible raw payloads.

## Audit sequence

1. Inspect the current `.gitignore`, backup script, status (including ignored files), remotes, branch, tracked file count, and Git object size.
2. Measure top-level disk usage and identify large tracked blobs and suspicious tracked paths.
3. Distinguish ordinary files from nested repositories/submodules using `git ls-files -s`; mode `160000` is a gitlink. Parent ignore rules cannot govern content inside a child repository.
4. Inspect child repositories' own ignore rules/status for dependencies and build output.
5. Scan tracked filenames for secret-like names and transient suffixes without printing secret values.
6. Add conservative ignore rules before changing the index. Anchor workspace-specific scratch patterns at repository root so legitimate project files are not hidden globally.
7. Harden the copier itself (for example, rsync excludes), not only `.gitignore`; copied runtime state can already exist and remain tracked.
8. Add a fail-closed staged-content gate that rejects:
   - generated/runtime directory components,
   - secret-like filenames except approved templates,
   - runtime DB/cache suffixes,
   - oversized blobs (50 MiB is a useful conservative threshold).
9. Validate using a temporary Git index so the live staging area is untouched. Scope `GIT_INDEX_FILE` to one command/subshell; do not export it persistently.
10. Verify both positive and negative cases: scratch is ignored, durable source remains includable, and a simulated generated staged path is rejected.
11. Report separately:
   - future additions now prevented,
   - already-tracked generated files,
   - historical pack debt.

## Important Git semantics

- `.gitignore` affects untracked files only. It does not remove tracked files or shrink history.
- `git ls-files -ci --exclude-standard` identifies tracked paths now covered by ignore rules and therefore candidates for a later `git rm --cached` cleanup.
- Ignore evaluation includes nested `.gitignore` files. A root-level `!path` exception cannot override a later matching rule in a child `.gitignore`; add the narrow exception in the nested file that owns the rule.
- Index cleanup and history rewriting are separate destructive scopes. Do neither without explicit user approval.
- A broad `git add projects .hermes` in an automated backup is unsafe unless ignore rules and a staged-content gate are both in place.
- Gitlinks store only child commit pointers in the parent; dependency trees seen on disk inside a child are not parent blobs. Registered `160000` paths in `.gitmodules` are recovery-defining metadata and must not be removed merely because a broad ignore rule matches their worktree directories.

## Approved tracked-ignore cleanup

When the user explicitly asks to clean already-tracked ignored files, use an index-only workflow and preserve local copies:

1. Capture `git status --short`, `git ls-files -ci --exclude-standard`, `.gitmodules`, and `git ls-files -s` before mutation. Group the candidate list by path family.
2. Classify false positives before removal. Common recovery-critical exceptions include registered submodule gitlinks, skill/source directories whose names resemble generated media, sanitized inventories/runbooks, deliberate recovery backups, and `.gitkeep` placeholders.
3. Add narrow ignore exceptions at the same precedence level as the matching rule. Use `git check-ignore -v --no-index <path>` to identify the exact file and line responsible; inspect nested `.gitignore` files too.
4. Remove only the final candidate set from the index, not disk:

   ```bash
   git ls-files -ci --exclude-standard -z | xargs -0 -r git rm -r --cached --ignore-unmatch --
   ```

5. Stage only the hygiene policy, verifier, and intended index removals. Avoid `git add .` in a dirty control repository.
6. Before committing, verify the deletion summary and explicitly prove representative local cache/runtime paths still exist.
7. Run the staged-content gate while additions/modifications are staged, then run `git diff --cached --check`.
8. After committing, verify all invariants independently:
   - `git ls-files -ci --exclude-standard` returns zero;
   - every `.gitmodules` path is still mode `160000` in the parent index;
   - representative durable skills/runbooks/placeholders remain tracked;
   - representative caches remain present locally but absent from `git ls-files`;
   - `git diff-tree --check HEAD^ HEAD` passes.
9. If final review finds an over-broad rule, restore durable paths from the pre-cleanup commit, narrow the rule, and amend before publishing. Do not accept a zero-match result achieved by silently deleting recovery-critical metadata.
10. Treat publication as a separate phase. Preflight authenticated fetch before promising a push. If local and remote have diverged, fetch the remote tip and apply the narrow cleanup commit in an isolated worktree/clone; never force-push or overwrite remote-only commits merely to publish hygiene changes.

### Cleanup pitfalls

- Never use worktree deletion (`rm`, `git clean`, plain `git rm`) when the request is to stop backing files up. `git rm --cached` is the safe default.
- Do not use blanket names such as `**/media/` without checking for human-authored source categories also named `media`.
- Do not assume root exceptions override nested ignore files; diagnose with `git check-ignore -v`.
- A staged verifier run after the commit may be vacuous because the index has no staged additions. Run it before commit, then use tree/index invariants after commit.
- If authentication is unavailable, report the exact local commit and verified local state, but do not say the GitHub repository itself is clean until remote readback proves it.

## Safe validation pattern

Use an alternate index without contaminating later commands:

```bash
idx=$(mktemp)
rm -f "$idx"
trap 'rm -f "$idx"' EXIT
env GIT_INDEX_FILE="$idx" bash -c '
  set -e
  git read-tree HEAD
  git add .gitignore
  python3 scripts/verify_backup_stage.py
'
```

Never globally export `GIT_INDEX_FILE` across unrelated tool calls. If status suddenly shows mass deletions, inspect and clear that variable before touching the real index.

## Staged gate design

Read staged paths with:

```bash
git diff --cached --name-only --diff-filter=ACMR -z
```

Read staged blob sizes from the index rather than the worktree:

```bash
git cat-file -s ":path/to/file"
```

This makes checks deterministic and catches exactly what the backup commit would publish.

## Verification checklist

- Backup shell/Python syntax checks pass
- Parent canonical index is unchanged during audit
- Scratch patterns are ignored
- Durable source, lockfiles, and curated records remain visible
- Simulated generated/secret-like/oversized staged content is rejected
- Child submodule ignore behavior is checked independently
- No deletion, `git rm --cached`, commit, push, or history rewrite occurred without approval
