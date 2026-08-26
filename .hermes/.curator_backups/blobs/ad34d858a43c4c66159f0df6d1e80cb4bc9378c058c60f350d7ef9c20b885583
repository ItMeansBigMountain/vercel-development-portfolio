---
name: hermes-agent-operations
description: "Use when configuring, extending, troubleshooting, or operating Hermes Agent systems: skills, specialist profiles, cron jobs, Kanban workers, automation scripts, and profile-scoped operational workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes-agent, operations, skills, cron, kanban, profiles, automation]
    related_skills: [hermes-agent, native-mcp, cloud-app-deployment-ops, webhook-subscriptions]
---

# Hermes Agent Operations

## Overview

This umbrella skill covers recurring operational work around Hermes itself: writing and maintaining skills, configuring specialist profiles, managing scheduled jobs, and running Kanban worker workflows. Load it when the task is about making Hermes behave reliably as an operating system for agents rather than about one application domain.

## When to Use

- Creating, editing, validating, or consolidating Hermes skills.
- Configuring named specialist profiles with separate models, tools, env files, working directories, or consult wrappers.
- Creating, updating, debugging, or smoke-testing Hermes cron jobs and scripts.
- Operating Kanban worker/orchestrator flows, especially blocked/retry/review handoffs.
- Troubleshooting profile isolation, environment variables, job delivery, worker summaries, or automation state.

Do not use this as a substitute for the official Hermes docs or the `hermes-agent` skill when the user is configuring Hermes itself; use those as the source of truth and this skill for operational playbooks and pitfalls.

## Skill Authoring and Consolidation

For skill work, treat the library as class-level procedural memory, not one-session-one-skill notes.

1. Inspect existing peer skills first (`skills_list`, then `skill_view`).
2. Prefer patching an existing umbrella or adding `references/`, `templates/`, or `scripts/` files over creating a narrow sibling.
3. Keep frontmatter valid: byte-zero `---`, `name`, `description`, non-empty body, and description under 1024 characters.
4. Use `skill_manage(action='patch')` for small fixes, `edit` only for full rewrites, and `write_file` for support files.
5. Before archiving or demoting a skill, inspect the complete package: `SKILL.md`, `references/`, `templates/`, `scripts/`, and `assets/`. Do not leave relative links pointing to files that were not re-homed or preserved.

### Skill package shape

```text
<skill>/
  SKILL.md
  references/   # detailed notes, research, provider quirks, transcripts
  templates/    # copy-and-modify starters
  scripts/      # statically reusable helpers/probes
  assets/       # media or static fixtures when needed
```

## Specialist Profile Operations

Use named profiles when a recurring class of work benefits from separate model/provider settings, tools, secrets, or a canonical workspace.

1. Inspect or create the profile: `hermes profile list`; `hermes profile create <name> --clone default` when needed.
2. Put secrets in the profile env file, not raw config; reference them as env vars.
3. Configure the model/provider explicitly, including `base_url`, `default`, `api_key`, and `api_mode` for OpenAI-compatible custom providers.
4. Set a profile-specific working directory when the specialist has a canonical repo.
5. Scope tools to the role instead of copying every tool.
6. Add a standing `agent.environment_hint` with role, boundaries, repo path, and conventions.
7. Create a consult wrapper such as `/opt/data/scripts/<profile>_consult.sh` only after the profile passes a live smoke test.

For security/red-team specialists, describe authorized defensive/lab uses and explicit boundaries. Do not frame a profile/provider as a safety bypass.

### Profile-scoped gateway sessions

When a user asks for only one gateway lane/session to use a specialist profile while other sessions remain on default, do not assume per-channel routing exists. First distinguish a **model switch** from **profile isolation**: `/model` may switch the current chat's model, but the profile's memory, skills, config, and credentials stay unchanged. Full profile isolation requires gateway profile routing (`gateway.multiplex_profiles` plus an inbound source stamped with the target profile). For Discord, the robust pattern is a separate specialist Discord bot token/adapter restricted to that channel; two profiles should not share the same Discord bot token concurrently. See `references/profile-scoped-gateway-routing.md` for the routing model, Discord guidance, and verification checklist.

For user-specific Discord lane organization, cron delivery routing, and the fallback watchdog pattern for keeping an additional profile gateway such as `redteam` alive after Docker/container reset, see `references/discord-channel-cron-routing-and-profile-autostart.md`.

## Cron Job Operations

Use this pattern for scheduled Hermes jobs and script-backed automations.

1. List jobs and identify the exact job id before update/remove operations.
2. Locate the referenced script and verify it exists, has expected permissions, and runs manually.
3. Smoke-test the script directly before updating the job definition. For `no_agent=true`, empty stdout means silent success; design watchdog scripts accordingly.
4. For Discord/server delivery changes, map jobs to the user's channel taxonomy and ask for confirmation plus concrete channel mentions/IDs before changing `deliver` fields. Do not silently move reports between channels.
5. Update the job with explicit `script`, `workdir`, `profile`, `enabled_toolsets`, and delivery target as needed.
6. Trigger one manual run after significant fixes and inspect returned output or errors.
7. For prompt-injection scanner blocks, inspect the job prompt plus attached skills/references; rephrase risky literal wording transparently and rerun.

Common cron pitfalls: missing scripts, stale OAuth tokens, wrong workdir, non-executable files, silent no-agent jobs that should have emitted status, wrappers that consume discovery state during smoke tests, and rerouting cron deliveries without first confirming the target Discord channel.

### VPS storage, safe scratch, unattended resources, and backup hygiene

Agent-driven Git reconciliation and publish commands can leave multi-gigabyte clones behind when a tool session is interrupted. Use source-level `trap` cleanup **and** a locked, allowlist-only retention watchdog; neither is sufficient alone. Before any broad VPS cleanup, audit disk, inodes, RAM, swap, PSI/cgroup OOM history, process trees/CWD/listeners, open-deleted files, launch metadata, services, and cron overlap; then obtain explicit approval for exact paths or process groups. Never turn approval for named paths into permission to remove adjacent caches or stop other processes. See `references/stale-worktree-retention-and-disk-guard.md` for the deletion safety model and `references/host-resource-and-backup-hygiene.md` for full host triage, process classification, pressure monitoring, cron planning, and Git-backup boundaries.

For GitHub backups, preserve human-authored and recovery-defining state rather than a machine image. Enforce exclusions in both `.gitignore` and the backup copier, and use a fail-closed staging verifier for generated paths, secret-like filenames, runtime databases, and oversized blobs. Remember that parent ignore rules do not apply inside child submodules, and that newly ignored tracked files remain in Git until a separately approved untracking/history-cleanup phase. A backup push rejected as non-fast-forward requires controlled reconciliation, not more frequent retries.

When hosted deployments restrict file tools with `HERMES_WRITE_SAFE_ROOT`, keep `/tmp` outside the boundary and provide `$HERMES_HOME/tmp/agent-scratch/` as restrictive (`0700`) durable scratch. Put this path in file-tool guidance and return an actionable out-of-root error rather than misclassifying ordinary scratch files as credentials. A file-mutation verifier warning is not itself a RAM/disk alert: repeated retries add context, while stale high-RSS language servers and Java/Gradle processes are the likely unattended RAM hazard. Monitor those processes with age/RSS thresholds in **alert-only** mode; do not auto-kill without explicit lifecycle authorization. See `references/safe-write-roots-and-unattended-memory-guard.md` for implementation, testing, and deployment-restart checks.

## Kanban Worker Operations

Workers are headless. Use durable board signals instead of live-user clarification.

- Start by reading task state and comments; a task may have been blocked, archived, or retried after dispatch.
- Use the assigned workspace boundary; do not modify outside it unless the task explicitly says so.
- Heartbeat only for meaningful long work, not "still working" noise.
- For code-changing work that needs human review, comment structured handoff metadata, then block with `review-required: ...` instead of completing prematurely.
- Capture real ids returned by `kanban_create`; never invent follow-up card ids in prose or metadata.
- Block with one clear decision question plus a comment containing deeper context.

## Support Package Index

Archived source packages absorbed into this umbrella are preserved under `references/absorbed/<old-skill-name>/` when available. Start with these subpackages when you need the old full detail:

- `references/absorbed/cron-job-management/` — detailed cron debugging playbook plus `verify_cron_job.sh`.
- `references/absorbed/hermes-agent-skill-authoring/` — in-repo skill authoring validator notes and peer structure.
- `references/absorbed/kanban-worker/` — worker lifecycle pitfalls, handoff shapes, and retry scenarios.
- `references/absorbed/specialist-agent-profiles/` — profile setup, red-team profile guardrails, and consult wrapper template.

## Common Pitfalls

1. Creating a narrow skill when an umbrella section or reference file would be more discoverable.
2. Editing another profile's skills/plugins/cron/memories without explicit direction.
3. Reporting a cron fix without a direct script run or manual job run.
4. Calling `clarify` from a headless Kanban worker; block the task instead.
5. Leaking env values, tokens, or profile secrets while debugging; if a user pastes a token into chat, complete the immediate setup only if requested, then explicitly advise rotating the token after verification.
6. Confusing Discord bot connection with server/channel access: `Connected as ...` means authentication worked, while `403 Missing Access` usually means the bot has not been invited or lacks channel permission.
7. Using usage counters as proof that a skill should or should not exist.

## Verification Checklist

- [ ] Official Hermes docs / `hermes-agent` skill were used when the task modifies Hermes behavior.
- [ ] Skill/profile/job state was inspected before modification.
- [ ] Scripts or jobs were actually smoke-tested when changed.
- [ ] Package support files were preserved when consolidating skills.
- [ ] Final report includes exact changed skill/profile/job names and verification output.
