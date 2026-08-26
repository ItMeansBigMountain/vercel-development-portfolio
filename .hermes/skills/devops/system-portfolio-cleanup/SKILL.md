---
name: system-portfolio-cleanup
description: "Audit workspace against mandate; classify, archive, dehost."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cleanup, portfolio, kanban, orchestration, git, vercel]
    related_skills: [kanban-orchestrator]
---

# System Portfolio Cleanup

## When to use
A user provides a portfolio mandate (like `message.txt`) that defines canonical parent projects, consolidation rules, and dehost/discard lists. You must:
1. Classify every repo in the workspace against that mandate
2. Get **explicit interactive approval** before any destructive action
3. Archive (not delete) local repos to preserve git history
4. Dehost Vercel/other deployments to save bandwidth
5. Create a Kanban task graph so specialists execute the implementation work

## Core workflow

### 1. Discover & classify
```bash
find /path/to/projects -maxdepth 2 -type d -name ".git"
# Cross-reference against mandate:
# - Canonical parents (keep + CI/CD + active)
# - Absorbed prototypes (archive, already merged)
# - Learning/history only (archive, no product)
# - Duplicate/legacy (archive)
```

### 2. Interactive approval (mandatory)
Use `clarify` with **checkboxes** for each category. Never assume approval.

### 3. Archive local repos (safe, reversible)
```bash
mkdir -p /path/to/projects/_archive
for d in <approved_list>; do
  if [ -d "$d" ]; then mv "$d" "/path/to/projects/_archive/$(basename $d)"; fi
done
```
**Never** `rm -rf` a `.git` directory. Move only.

### 4. Dehost Vercel projects
Requires valid `VERCEL_TOKEN`. If invalid/expired:
- Block dehosting task (`block_kind="credentials"`)
- Resume when user provides fresh token

```bash
npx -y vercel@latest ls --token "$VERCEL_TOKEN"
npx -y vercel@latest remove <project-id> --token "$VERCEL_TOKEN" --yes
```

### 5. Create Kanban task graph
Master → specialist CI/CD cards → reviewer gate → ops dehost card (gated on master+reviewer).

## Pitfalls
- **Token expiry**: Verify with `vercel ls` before batch dehosting
- **Silent dispatcher**: Unknown assignees = stuck in `ready`; run `hermes profile list` first
- **Board env pin**: Prefix CLI with `HERMES_KANBAN_BOARD=<slug>` or fresh session
- **Archive location**: Use `_archive/` sibling to `projects/`
- **No history deletion**: "Preserve everything, archive instead of delete"

## References
- `references/vercel-token-troubleshooting.md`
- `references/portfolio-classification-template.md`
- `references/portfolio-cleanup-and-dehosting.md` — detailed Kanban workflow, token troubleshooting, and pitfalls from 2026-08-25 session