# Reconciling a stale Kanban board against newer chat context

Use this when the user says the current conversation has newer information than the Kanban board, or asks to review/finish all tasks after significant work happened outside the board.

## Workflow

1. **Audit the active board first**
   - Confirm the intended board (`hermes kanban boards current`).
   - List tasks with JSON output and group by status.
   - For every non-`done` task, inspect `hermes kanban show <id> --json`, especially comments, events, latest summary, and runs.

2. **Treat newer explicit user direction as authoritative**
   - If the user rejected a concept in chat, stale furnishing/publishing cards for that concept should not stay blocked waiting for review.
   - Annotate already-terminal cards if their old result conflicts with the current product direction, so future agents do not recreate rejected ideas.

3. **Close review-required cards only when there is evidence**
   - Accept old `review-required` blocks as complete when their handoff records passing tests/builds, clean git state, commit IDs, or other verifiable completion evidence.
   - If a card was blocked by a transient resource issue, re-run the verification before completing it.
   - If evidence is missing and cannot be verified, keep it blocked or create a specific follow-up rather than bulk-closing blindly.

4. **Handle obsolete/deleted projects explicitly**
   - For rejected local/GitHub projects, verify local absence and remote absence where possible.
   - Complete the task with a result like: `obsolete per updated product direction; local project removed and remote absent`.

5. **Bulk completion caveat**
   - `hermes kanban complete` supports multiple task IDs with `--result`, but `--summary`/`--metadata` are per-task and cannot be used with multiple IDs.
   - If shared prose is sufficient, use one bulk `--result`. If structured metadata matters, complete tasks one at a time.

6. **Fan-in publishing tasks**
   - If a publish fan-in card depends on per-repo furnishing cards, verify all active repos have clean remotes and pushed heads before closing it.
   - For Git repos, compare local `HEAD` to `git ls-remote origin refs/heads/main` or the relevant branch.

## Pitfalls

- Do not assume `blocked` means unfinished. Many coding workers block with `review-required` after completing tests and commits.
- Do not let stale board tasks override the user's newer product decisions.
- Do not re-create repos or projects the user rejected just because a stale task says to furnish or publish them.
- Do not record environment-specific transient tool failures as durable rules; record the verification/retry pattern instead.