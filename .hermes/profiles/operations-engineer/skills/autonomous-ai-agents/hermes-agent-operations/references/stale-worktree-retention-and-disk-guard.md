# Stale temporary worktree retention and disk-pressure guard

Use this pattern when agent-driven Git reconciliation, restore, submodule, or publish workflows create multi-gigabyte temporary clones that may survive interruption.

## Why shell cleanup alone is insufficient

A command-local `trap` should still remove its own temporary clone, but it cannot cover every failure mode: agent cancellation, container restart, killed process, interrupted tool session, or a retry that creates a new clone before the old session resumes. Pair source-level cleanup with an independent retention watchdog.

## Required discovery and approval boundary

Before deleting or stopping anything on a VPS:

1. Audit both storage and RAM: `df`, inodes, top-level `du`, largest files, deleted-open files, process RSS/age/tree, and container/package-cache usage where applicable.
2. Distinguish canonical repositories and state databases from temporary clones, generated dependencies, and caches.
3. Present exact candidate paths and measured sizes.
4. Obtain explicit deletion/process-stop approval unless the user has already authorized a narrowly defined automated retention policy.
5. Capture before/after filesystem usage and verify every approved path is gone.

Do not broaden a one-time approval such as “delete these five paths and leave the rest alone” into permission to clean adjacent caches.

## Safe retention design

A production cleanup watchdog should:

- Default to dry-run; require an explicit apply mode.
- Use exact roots plus an explicit basename-prefix allowlist—never a broad `/tmp/*` or generic age deletion.
- Require a grace period (48 hours is a practical default; never silently lower below 24 hours).
- Reject symlinks, non-directories, mount points, and paths outside the approved root.
- Support a local hold marker such as `.hermes-keep`.
- Scan `/proc/*/{cwd,root,fd}` and refuse paths referenced by active processes.
- Use a non-blocking file lock to prevent overlapping cleanup runs.
- Measure allocated bytes before removal and verify nonexistence afterward.
- Keep persistent cache/worktree roots monitor-only unless separately approved.
- Emit structured output only for removals, eligible candidates, errors, or disk pressure; healthy no-op `no_agent` cron runs should be silent.
- Alert at a defined disk threshold (for example 80%) rather than waiting for ENOSPC.

## Verification

1. Add dependency-free tests for allowlisted-old, unknown-prefix, recent, keep-marker, process-reference, and symlink cases.
2. Create an isolated fake allowlisted worktree, age it beyond the grace period, run apply mode, and verify only that fixture was removed.
3. Run apply mode against production with no candidates and confirm it is silent.
4. Add a scheduler-compatible wrapper under the Hermes scripts directory; cron script fields accept script names rather than arbitrary absolute commands with arguments.
5. Manually run the newly created cron job and verify scheduler status plus script output semantics.

## Source-workflow prevention

For every workflow that creates a temporary clone:

- Prefer `mktemp -d` under an approved prefix.
- Install `trap 'rm -rf -- "$workdir"' EXIT INT TERM` immediately after creation.
- Avoid fixed reusable clone paths unless an explicit lock and cleanup policy exist.
- Put needed recovery artifacts in the approved backup directory, not in temporary clones.
- Do not rely on eventual manual cleanup as the primary lifecycle mechanism.
