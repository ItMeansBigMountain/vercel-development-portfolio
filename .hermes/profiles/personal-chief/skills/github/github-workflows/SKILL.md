---
name: github-workflows
description: "Use when operating GitHub from Hermes: authentication, issues, pull requests, code review, repository setup, releases, and API/gh fallbacks. Provides one class-level workflow with support for templates and scripts."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, gh, git, issues, pull-requests, review, auth]
    related_skills: [requesting-code-review]
---

# GitHub Workflows

## Overview

This umbrella covers GitHub work across authentication, issue management, PR lifecycle, reviews, repository administration, and REST/GraphQL fallbacks. Prefer `gh` when available, but keep git-only and curl/API paths in mind.

## When to Use

- Authenticate git/gh/API access.
- Create, triage, label, assign, or search issues.
- Review local diffs or GitHub pull requests.
- Create branches, commits, PRs, monitor CI, merge, or manage repositories.

## Capability Map

### Authentication

1. Check `gh auth status` and `git remote -v`.
2. If `gh` is unavailable, use git credential/token or SSH key flows.
3. For API-only tasks, use a token with curl and report permission failures explicitly.

### Issues

- Search before creating duplicates.
- Use bug/feature templates when available.
- Include reproduction steps, expected behavior, actual behavior, labels, and assignees when known.

### Pull Requests and CI

- Create a clean branch, commit focused changes, push, and open a PR with a test plan.
- Monitor CI status and fetch logs before changing code.
- Do not merge until checks and requested reviews are satisfied unless the user explicitly directs otherwise.
- For Azure deployments, see `references/azure-oidc-environment-gates.md`: prefer GitHub OIDC + environment-gated federated credentials, and split Terraform infra workflows from app deploy workflows.
- For repos that contain both Terraform and app code, see `references/split-infra-app-deployment-path-filters.md`; keep infra deploys restricted to `infra/**` and app deploys restricted to app/frontend/deploy-config paths.
- If Azure Actions fail at `azure/login` with blank `ARM_CLIENT_ID`/`ARM_TENANT_ID`/`ARM_SUBSCRIPTION_ID`, load `references/azure-actions-oidc-variable-preflight.md`; inspect repo/environment variables and add a preflight step before `azure/login`. If `azure/login` reports missing `client-id`/`tenant-id`, check `references/azure-actions-oidc-variable-preflight.md` and add a preflight step before `azure/login` so missing repo/environment variables fail clearly.

### Code Review

- Review local changes before push and PR diffs after push.
- Prioritize correctness, security, data loss, race conditions, migrations, tests, and user-visible regressions.
- Provide file/line findings with severity and minimal fix suggestions.

### Repository Management

- Clone/create/fork repositories, manage remotes, releases, branch protection, and secrets.
- Be careful with destructive settings changes; confirm scope first.
- When an automated backup branch diverges and GitHub also rejects oversized generated blobs, do not blindly pull/rebase the dirty checkout. Use the clean-clone/net-diff recovery and verification workflow in `references/diverged-backup-large-artifact-recovery.md`.

## Fallback Ladder

1. `gh` CLI for high-level GitHub operations.
2. `git` for local repository and transport operations.
3. REST/GraphQL API with curl for unsupported or automation-heavy paths.
4. Browser only when authentication/UI state cannot be handled otherwise.

## Common Pitfalls

1. **Assuming `gh` auth implies git push auth.** Check both when push/pull fails.
2. **Creating duplicate issues.** Search first.
3. **Reviewing only generated summaries.** Inspect the actual diff.
4. **Ignoring CI logs.** Fetch failing logs before guessing a fix.
5. **Dropping templates.** Preserve repository issue/PR templates when present.
6. **Leaving local tracking refs stale after token-authenticated pushes.** If using an explicit token URL because normal HTTPS auth is unavailable, verify `git ls-remote <token-url> refs/heads/<branch>` equals `git rev-parse HEAD`; if it matches, update the local tracking ref with `git update-ref refs/remotes/origin/<branch> HEAD` so later status output does not falsely report ahead/behind.

## Verification Checklist

- [ ] Correct owner/repo confirmed.
- [ ] Authentication and permissions verified for the chosen operation.
- [ ] State-changing operation produced a URL, ID, or status.
- [ ] CI/review status checked when relevant.
- [ ] User-facing report includes links/IDs and tests run.
