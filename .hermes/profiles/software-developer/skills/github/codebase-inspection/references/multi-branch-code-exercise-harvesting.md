# Multi-branch code exercise harvesting

Use this pattern when a user asks to import or inventory all coding exercises/algorithms from a repository and explicitly says to check all branches.

## Workflow

1. Fetch every branch before inventory:

```bash
git fetch --all --prune
git branch -a --no-color
```

2. Enumerate files from each remote branch without checking them out:

```bash
for branch in $(git branch -r --no-color | sed 's#^[[:space:]]*origin/##' | grep -v '^HEAD'); do
  echo "=== $branch ==="
  git ls-tree -r --name-only "origin/$branch"
done
```

3. For generated app content, preserve source traceability on each item:

- `sourcePath`
- `branches`
- `language`
- `category`
- `difficulty`

4. Deduplicate carefully:

- Same path on multiple branches: one item with multiple branch labels.
- Same algorithm under different paths/languages: keep separate if it teaches a different language/track.
- Non-code description files may need parsing into multiple exercises.

5. Difficulty bucketing heuristics for coding assessment apps:

- Beginner: basic loops, conditionals, simple arrays, string reversal, type conversion, simple errors.
- Intermediate: arrays/lists/maps/sets, dedupe, missing numbers, recursion basics, sorting drills.
- Advanced: LeetCode-style patterns, binary search, merge sort, stacks/queues, parentheses/brackets, max subarray, functional map/filter/reduce.

6. Build multiple assessments instead of one monolithic quiz:

- Difficulty tracks: beginner/intermediate/advanced.
- Language tracks: Java/Python/etc.
- Full repo review: all questions.

7. Verify generated artifacts:

- Count questions by assessment and branch coverage.
- Parse generated JavaScript/JSON with a syntax parser.
- Run the app build/export if project config supports it; otherwise report the config blocker separately from syntax validation.

## Pitfalls

- Do not assume the default branch contains all exercises.
- Do not mutate user worktrees by checking out branches unless necessary; `git ls-tree` and `git show origin/branch:path` are safer.
- Do not mix generated changes with unrelated dirty worktree changes in commits.
- If a repo already has many uncommitted changes, report changed files and avoid committing unless the user approves the exact scope.
