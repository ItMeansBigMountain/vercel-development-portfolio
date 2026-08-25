---
name: cron-job-management
description: Manage scheduled cron jobs for Hermes projects, including locating scripts, verifying execution permissions, testing scripts, updating job definitions, and ensuring reliable delivery.
version: 1.0.0
platforms: [linux]
metadata:
  hermes:
    tags: [cron, automation, troubleshooting, scripts]
    related_skills: [cloud-app-deployment-ops, webhook-subscriptions, kanban-orchestrator]
---

# Cron Job Management — Playbook

**Purpose**: Manage scheduled cron jobs for Hermes projects, including locating scripts, verifying execution permissions, testing scripts, updating job definitions, and ensuring reliable delivery.

## When to use
- Fixing broken cron jobs where script paths are missing or misconfigured.
- Reactivating paused jobs after environment changes.
- Debugging token refresh or permission errors in automated tasks.
- Verifying that cron jobs produce expected output before relying on scheduled runs.

## Prerequisites
- Access to the Hermes project directory structure under `/opt/data/HeRmEz/projects`.
- Ability to run `cronjob` tool and `terminal` commands.
- Sufficient permissions to edit cron job definitions and script files.

## Core Steps
1. **Locate the script** referenced in the cron job definition.
   - Use `ls -la <project>/scripts/` to verify the script exists.
   - Confirm the script has execute permission (`chmod +x <script>` if needed).

2. **Validate script functionality** manually.
   - Run the script directly: `bash <script>` or `./<script>`.
   - Capture output and check for expected results or error messages.

3. **Update the cron job definition** if the script path changed.
   - Use `cronjob action=update job_id=<ID> script=<full_path_to_script>`.
   - Ensure the job is `enabled: true` and `state: scheduled`.

4. **Handle token refresh / credential issues** (e.g., email sorting agent).
   - Identify missing or expired credentials (OAuth tokens).
   - Re‑authenticate using associated helper scripts (e.g., `generate_google_mass_auth_urls.py`).
   - Verify that the script can acquire a fresh token before resuming the cron job.

5. **Verify job status** after updates.
   - Run `cronjob action=list` to confirm the job shows `enabled: true` and `state: scheduled`.
   - Optionally trigger an immediate run with `cronjob action=run job_id=<ID>` to confirm immediate execution.

6. **Document any pitfalls** discovered (e.g., token expiration, missing environment variables).

## Common Pitfalls
- **Missing script file** – job stays paused; verify script exists in the expected directory.
- **Stale token** – jobs fail with `invalid_grant`; re‑run credential generation scripts and re‑enable the job.
- **Insufficient permissions** – script not executable; `chmod +x` resolves.
- **Incorrect workdir** – ensure the script runs in its intended directory; set `workdir` in the cron job if needed.
- **Expanding a no-agent discovery cron into an action pipeline** – preserve the watchdog contract. Wrap the old discovery command in a new script that captures stdout, exits silently when stdout is empty, prints discovery output when non-empty, then runs the downstream action. Keep `no_agent=true` only if the wrapper itself emits the exact user-facing status. Smoke-test the wrapper before `cronjob action=update`, but remember that discovery smoke tests may mark items as seen or consume “new item” state.
- **Prompt-injection scanner false positives** – cron jobs can be blocked by the assembled prompt, not just the job's own prompt. If the error names `deception_hide`, inspect attached skills and references for literal hidden/deception phrasing such as instructions about hiding information from the user. Rephrase those docs transparently, then trigger a manual run before declaring the cron fixed.

## Related Skills
- `cloud-app-deployment-ops` – for deploying scripts to cloud‑hosted environments.
- `webhook-subscriptions` – for event‑driven alternatives to cron.
- `kanban-orchestrator` – when managing multiple related cron jobs across projects.

## Support Files
- `scripts/verify_cron_job.sh` – helper script to test a cron job's script and report status.
- `references/cron-job-debugging.md` – detailed troubleshooting guide and error transcript examples.