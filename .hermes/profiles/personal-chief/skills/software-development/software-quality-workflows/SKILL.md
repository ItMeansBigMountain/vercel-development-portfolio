---
name: software-quality-workflows
description: "Use when validating, debugging, simplifying, or spiking software work. Umbrella for root-cause debugging, throwaway feasibility spikes, pre-commit verification, and focused code cleanup."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [software-development, debugging, code-review, verification, refactor, spike, quality]
    related_skills: [test-driven-development, plan, github-pr-workflow]
---

# Software Quality Workflows

## Overview

Use this umbrella when software work needs disciplined validation instead of ad-hoc edits. It covers four recurring classes of work:

1. **Root-cause debugging** — understand why a bug happens before fixing it.
2. **Feasibility spikes** — build disposable experiments before committing to a production approach.
3. **Pre-commit verification** — run security, tests, lint, and independent review before shipping.
4. **Simplification review** — use focused reviewers to remove duplication, reduce complexity, and improve efficiency in recent changes.

The common rule across all modes: collect evidence, make scoped changes, and verify with real commands.

## When to Use

- User reports a bug, failing test, build failure, or unexpected behavior.
- User asks to prototype, validate an idea, compare approaches, or "spike" something before building.
- User asks to review, verify, ship, commit, push, simplify, or clean up recent code changes.
- You have edited code and need a quality gate before claiming completion.

Do not use this for non-code research, document-only edits, or broad product planning unless the next step is a concrete software experiment or verification pass.

## Mode A — Systematic Debugging

**Iron law:** no fixes before root cause investigation.

Follow the four phases:

1. **Root cause investigation**
   - Read full error messages and stack traces.
   - Reproduce the issue with an exact command.
   - Inspect recent changes with `git diff`, `git log`, and relevant file reads.
   - Trace data flow across component boundaries; add temporary diagnostics when necessary.
   - Form a specific hypothesis: "X causes Y because Z."
2. **Pattern analysis**
   - Find similar working code in the same repo.
   - Compare broken and working paths; list meaningful differences.
   - Read reference implementations completely before adapting them.
3. **Hypothesis testing**
   - Test one hypothesis with the smallest possible change.
   - If it fails, return to investigation; do not pile on speculative fixes.
4. **Implementation and verification**
   - Add or run a regression test when practical.
   - Fix the root cause, not the symptom.
   - Run targeted tests first, then broader tests/lint if available.

If three attempted fixes fail, stop and question the architecture before making a fourth attempt.

## Mode B — Feasibility Spikes

Use spikes when the answer requires touching code, APIs, or runtime behavior before committing to a real build.

Workflow:

1. **Decompose** into 2-5 feasibility questions unless the user already specified a single spike.
2. **Research just enough** to choose candidate tools or approaches.
3. **Build disposable artifacts** under `spikes/<NNN-topic>/` or the repo's established planning directory.
4. **Prefer observable output**: CLI demo, minimal HTML page, tiny endpoint, or focused test.
5. **Write a verdict** in each spike README:
   - `VALIDATED` — core question works with evidence.
   - `PARTIAL` — works with stated constraints.
   - `INVALIDATED` — does not work; document why and what to do instead.

For comparison spikes, use numbered variants like `002a-approach-one/` and `002b-approach-two/`, then produce a head-to-head table with setup complexity, output quality, performance, maintainability, and recommendation.

## Mode C — Pre-Commit Verification

Use before committing, pushing, or calling code "done".

1. **Get the diff**
   - Prefer `git diff --cached`; if empty, use `git diff` or the user-specified scope.
   - Split large diffs by file rather than truncating.
2. **Run security checks on added lines**
   - hardcoded secrets/tokens/passwords
   - shell injection (`os.system`, `subprocess(..., shell=True)`)
   - unsafe `eval`/`exec`
   - unsafe deserialization (`pickle.loads`)
   - SQL built with string formatting
3. **Run project checks**
   - Python: `python -m pytest`, `ruff`, `mypy` when configured.
   - Node: `npm test`, `eslint`, `tsc` when configured.
   - Rust: `cargo test`, `cargo clippy`.
   - Go: `go test ./...`, `go vet ./...`.
   - Compare against a known baseline when the repo already has failures.
4. **Independent review**
   - Use a separate `delegate_task` reviewer for security and logic issues when the diff is non-trivial.
   - Fail closed: unparseable reviewer output, security concerns, or logic errors block the commit.
5. **Fix and reverify**
   - Limit to two fix-and-reverify cycles unless the user explicitly asks to continue.

## Mode D — Simplification Review

Use when the user explicitly asks to simplify, clean up, or review recent changes for maintainability.

1. Capture the relevant diff (`git diff`, staged diff, last commit, branch diff, or files named by the user).
2. Run up to three focused reviewers, ideally in parallel:
   - **Reuse reviewer** — find duplicated logic and existing helpers/constants the change should use.
   - **Quality reviewer** — find redundant state, parameter sprawl, leaky abstractions, copy-paste variation, and stringly-typed logic.
   - **Efficiency reviewer** — find repeated work, missed concurrency, hot-path bloat, TOCTOU patterns, leaks, and overly broad reads.
3. Aggregate findings, discard weak false positives, resolve conflicts by correctness first, then user focus, then readability/reuse, then performance.
4. Apply only scoped fixes related to the diff unless the user asked for a larger refactor.
5. Run targeted verification after applying changes.

If the user asks for a dry run, report findings without editing.

## Common Pitfalls

- Guessing at fixes before reading the full error and reproducing the bug.
- Treating a spike as production code; spikes should be easy to throw away.
- Reviewing only the visible diff when repository conventions or shared helpers matter.
- Letting a reviewer refactor unrelated code under the banner of cleanup.
- Skipping verification because the change "looks obvious."
- Running a full expensive suite first when a targeted test would isolate the issue faster.

## Domain-Specific Review References

- For PostgreSQL functions, scheduled workers, Stripe ledgers/webhooks, and Next.js hydration QA, use `references/full-stack-marketplace-lifecycle-verification.md`. It covers runtime database-function tests, double-run idempotency assertions, exact refund/payout checks, app-client chunk diagnosis, and responsive interaction gates.
- For reviewing a portfolio of standalone RuneLite/OSRS external plugins, use `references/runelite-plugin-portfolio-review.md`. It covers multi-repo inventory, Gradle verification, Plugin Hub metadata checks, product-readiness ranking, and common consolidation families.
- For consolidating many OSRS plugin repos into canonical child repos inside a parent workspace/submodule repo, use `references/runelite-osrs-consolidation-submodule-workflow.md`. It covers TDD feature absorption, child-first pushes, exact parent submodule pointer staging, Java 11 verification, and authenticated GitHub push patterns with `GITHUB_ACCESS_TOKEN`.
- For RuneLite side-panel QA, treat default sidebar width as a hard requirement: verify controls do not trail off, prefer compact dropdowns/icon buttons over wide tabs, and call out Swing controls that need explicit preferred/maximum sizing.

## Verification Checklist

- [ ] The selected mode matches the user's request.
- [ ] Evidence was gathered with real tool output, not inferred from memory.
- [ ] Changes were scoped to the root cause, spike, verification failure, or simplification target.
- [ ] Tests, lint, type checks, or runnable demos were executed when available.
- [ ] The final report states what was verified and any remaining risk.
