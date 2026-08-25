---
name: ai-coding-agents
description: "Use when delegating software work to external coding agents or Hermes subagents: Codex, Claude Code, OpenCode, Kanban lanes, or delegate_task execution/review loops. Covers mode selection, isolation, prompts, monitoring, reconciliation, and verification."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, coding, delegation, codex, claude-code, opencode, kanban, subagents]
    related_skills: [writing-plans, requesting-code-review, systematic-debugging]
---

# AI Coding Agents

## Overview

This umbrella covers class-level workflows for handing coding work to an autonomous coding agent while Hermes remains responsible for scope, verification, reconciliation, and final user reporting. Treat external agents as implementation workers, not authorities.

## When to Use

- A feature, bug fix, PR review, or refactor is large enough to benefit from an isolated worker.
- You need parallel attempts, worktree isolation, or a review lane.
- A plan can be decomposed into self-contained tasks with explicit acceptance gates.

## Agent Menu

### Codex CLI

Best for OpenAI Codex one-shot implementation, PR review, and worktree-based parallel issue fixing. Use non-interactive mode when possible; use a PTY only for truly interactive sessions.

### Claude Code CLI

Best for feature implementation, broad codebase edits, and CLI-driven review loops when Claude Code is installed and authenticated. Watch for interactive prompts and permission flows.

### OpenCode CLI

Best for lightweight one-shot coding and review tasks when OpenCode is the available configured worker. Resolve the binary path first and avoid assuming a global install.

### Hermes `delegate_task` Subagents

Best for bounded research/review/coding subtasks inside Hermes where results return as summaries. Pass full context because subagents do not inherit conversation state.

### Specialized Hermes Profiles

Best when the user wants a standing alternate model/profile for a class of work while the main assistant keeps orchestration, policy, verification, and final reporting. For security/redteam consultation, use `references/redteam-consult-profile.md`: pass explicit authorization/scope, treat the profile as an advisor rather than a bypass, and verify outputs before acting.

### Kanban Codex Lanes

Best when a Hermes Kanban worker needs Codex as an isolated implementation lane while Hermes owns lifecycle, reconciliation, tests, and handoff.

## Standard Delegation Workflow

1. Confirm the repository state, branch, worktree, and dirty files.
2. Choose the worker based on installed CLI, task shape, and isolation needs.
3. Write a self-contained prompt: objective, paths, constraints, test command, non-goals, output format.
4. Run the worker in foreground for short tasks or tracked background mode for long tasks.
5. Inspect diffs yourself. Never trust the worker's self-report.
6. Run tests, linters, and any acceptance checks.
7. Reconcile or revert bad edits before reporting success.

## Prompt Contract

Every coding-agent prompt should include:

- The exact task and desired behavior.
- Relevant paths and files to inspect.
- Constraints: do not change public APIs, do not commit, no network, etc.
- Verification command(s) and expected pass criteria.
- Required final summary: files changed, tests run, blockers.

## Common Pitfalls

1. **Letting the worker own verification.** Hermes must read diffs and run checks.
2. **Omitting context.** External agents and subagents lack hidden session context.
3. **Running multiple workers in one worktree.** Use isolated worktrees/branches for parallel lanes.
4. **Hanging on interactive prompts.** Use PTY for interactive CLIs or non-interactive flags where available.
5. **Reporting success from a self-report.** Verify artifacts directly.

## Verification Checklist

- [ ] Worker had self-contained instructions.
- [ ] Worktree/branch isolation was appropriate.
- [ ] Diff was inspected by Hermes.
- [ ] Tests or equivalent checks were run by Hermes.
- [ ] Final user report distinguishes verified facts from worker claims.
