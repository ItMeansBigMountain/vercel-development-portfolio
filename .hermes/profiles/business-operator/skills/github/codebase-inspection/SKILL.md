---
name: codebase-inspection
description: "Inspect codebases w/ pygount: LOC, languages, ratios."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [LOC, Code Analysis, pygount, Codebase, Metrics, Repository]
    related_skills: [github-repo-management]
prerequisites:
  commands: [pygount]
---

# Codebase Inspection with pygount

Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios using `pygount`.

## When to Use

- User asks for LOC (lines of code) count
- User wants a language breakdown of a repo
- User asks about codebase size or composition
- User wants code-vs-comment ratios
- General "how big is this repo" questions
- User asks to inventory/import all coding exercises, algorithms, or question-bank content from a repo, especially when they say to check every branch

## Prerequisites

```bash
pip install --break-system-packages pygount 2>/dev/null || pip install pygount
```

## Project Inventory Status Reports

When the user asks for an inventory/status check across many project folders:

1. Prefer an existing tracker first (`PROJECT_REVIEW_SHEET.md`, deployment URL lists, README inventories) before rescanning every directory.
2. Verify the inventory count and live URLs with a lightweight scripted HTTP check when URLs are part of the status.
3. Produce one bullet per project in the user’s requested length. If they request “10–20 words,” keep each bullet tight and avoid extra analysis paragraphs.
4. Include operational facts only when verified: live status, stack/classification, modernization need, or recent known work.
5. Don’t expose tokens, environment variable values, deployment logs, or secret-bearing command output in the status summary.
6. If all URLs verify, state the aggregate once, then move directly into the bullets.
7. If the inventory turns into project retirement, consolidation, tracker updates, or product roadmapping, switch to or also load `project-portfolio-roadmapping`; this skill covers inspection, while that one governs durable direction docs and repo/tracker changes.

## 1. Basic Summary (Most Common)

Get a full language breakdown with file counts, code lines, and comment lines:

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

**IMPORTANT:** Always use `--folders-to-skip` to exclude dependency/build directories, otherwise pygount will crawl them and take a very long time or hang.

## 2. Common Folder Exclusions

Adjust based on the project type:

```bash
# Python projects
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript/TypeScript projects
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"

# General catch-all
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
```

## 3. Filter by Specific Language

```bash
# Only count Python files
pygount --suffix=py --format=summary .

# Only count Python and YAML
pygount --suffix=py,yaml,yml --format=summary .
```

## 4. Detailed File-by-File Output

```bash
# Default format shows per-file breakdown
pygount --folders-to-skip=".git,node_modules,venv" .

# Sort by code lines (pipe through sort)
pygount --folders-to-skip=".git,node_modules,venv" . | sort -t$'\t' -k1 -nr | head -20
```

## 5. Output Formats

```bash
# Summary table (default recommendation)
pygount --format=summary .

# JSON output for programmatic use
pygount --format=json .

# Pipe-friendly: Language, file count, code, docs, empty, string
pygount --format=summary . 2>/dev/null
```

## 6. Multi-Branch Exercise / Algorithm Inventory

When importing algorithms or coding exercises into another app, do not inspect only the default branch. Fetch all branches and enumerate remote branch trees without changing the worktree:

```bash
git fetch --all --prune
for branch in $(git branch -r --no-color | sed 's#^[[:space:]]*origin/##' | grep -v '^HEAD'); do
  echo "=== $branch ==="
  git ls-tree -r --name-only "origin/$branch"
done
```

For generated question banks, preserve source traceability (`sourcePath`, `branches`, `language`, `category`, `difficulty`) and verify counts by branch and assessment. See `references/multi-branch-code-exercise-harvesting.md` for the full workflow and difficulty bucketing heuristics.

## 7. Interpreting Results

The summary table columns:
- **Language** — detected programming language
- **Files** — number of files of that language
- **Code** — lines of actual code (executable/declarative)
- **Comment** — lines that are comments or documentation
- **%** — percentage of total

Special pseudo-languages:
- `__empty__` — empty files
- `__binary__` — binary files (images, compiled, etc.)
- `__generated__` — auto-generated files (detected heuristically)
- `__duplicate__` — files with identical content
- `__unknown__` — unrecognized file types

## Pitfalls

1. **Always exclude .git, node_modules, venv** — without `--folders-to-skip`, pygount will crawl everything and may take minutes or hang on large dependency trees.
2. **Markdown shows 0 code lines** — pygount classifies all Markdown content as comments, not code. This is expected behavior.
3. **JSON files show low code counts** — pygount may count JSON lines conservatively. For accurate JSON line counts, use `wc -l` directly.
4. **Large monorepos** — for very large repos, consider using `--suffix` to target specific languages rather than scanning everything.
5. **Default-branch blind spots** — when the user asks for “all” algorithms/exercises or says “check all branches,” use `git fetch --all --prune` plus `git ls-tree -r --name-only origin/<branch>` before generating inventories. The default branch may not contain the whole corpus.
6. **Dirty worktrees** — if converting an inventory into app changes, check `git status --short` first and avoid committing generated changes alongside unrelated existing modifications.
