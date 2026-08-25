# Safe write roots and unattended memory guard

## Problem class

Hosted Hermes deployments may set `HERMES_WRITE_SAFE_ROOT` to a durable volume such as `/opt/data`. File tools then correctly reject `/tmp`, but models commonly choose `/tmp` for one-off scripts. A rejected mutation is not itself a RAM/disk event; repeated retries add tool turns/context, while task-launched language servers and Java/Gradle processes can remain resident for days and create the real unattended RAM risk.

## Durable scratch pattern

- Preserve the safe-root boundary; do **not** globally permit `/tmp` merely to reduce warnings.
- Provide a profile-aware scratch location inside the writable root, conventionally `$HERMES_HOME/tmp/agent-scratch/`.
- Create it with restrictive permissions (`0700`).
- Put the location directly in `write_file`/`patch` guidance so prevention occurs before a denied tool call.
- Safe-root denials should distinguish ordinary out-of-root paths from credentials and return an actionable relocation message.
- Prefer the task's canonical project path for artifacts that are deliverables; use scratch only for disposable probes.

Example denial guidance:

```text
Write denied: '/tmp/example.py' is outside the configured writable roots.
For temporary scripts/files use '$HERMES_HOME/tmp/agent-scratch/' or write
inside the task's durable workspace.
```

## File-mutation verifier interpretation

A verifier footer means one requested path was not changed. It does not prove the task failed if an equivalent artifact landed at a different durable path. Check the mutation ledger or actual file state before reporting failure. Keep the verifier enabled: improve path guidance and error classification instead of suppressing a useful integrity control.

## Unattended RAM policy

Extend storage watchdogs to **report**, not automatically kill, stale high-RSS development processes. A conservative starting policy is:

- RSS at least 750 MiB
- Age at least 24 hours
- Command matches a development class such as Pyright, tsserver, Gradle, RuneLite, or language-server
- Include PID, RSS, age, command/project hint, and `alert_only`

Do not auto-kill solely from age/RSS: an active server or build can be legitimate. Process termination still requires explicit approval unless the user has separately authorized a precise automated lifecycle policy.

## Verification recipe

1. Probe the exact rejected `/tmp` path and confirm the error points to durable scratch.
2. Probe a canonical project path and confirm it remains writable.
3. Confirm the scratch directory owner/mode.
4. Run targeted file-safety and mutation-verifier tests with deployment-only environment variables removed from the legacy baseline; new tests should explicitly set them.
5. Run the watchdog live and confirm stale processes appear as `alert_only` and remain running.
6. Manually trigger the scheduled job once.
7. Determine whether the running gateway has already imported changed modules; source-path resolution alone does not prove hot reload. Avoid restarting an active gateway without approval.

## Pitfalls

- Treating a mutation-verifier warning as evidence of memory exhaustion.
- Calling every safe-root denial a credential violation.
- Opening `/tmp` globally rather than supplying safe scratch inside the durable root.
- Letting a hosted `HERMES_WRITE_SAFE_ROOT` leak into legacy tests that assume an unrestricted baseline.
- Auto-killing old language servers without checking ownership/activity or obtaining approval.
- Assuming a source edit is live in an already-running Python gateway; imported modules generally require a controlled restart.
