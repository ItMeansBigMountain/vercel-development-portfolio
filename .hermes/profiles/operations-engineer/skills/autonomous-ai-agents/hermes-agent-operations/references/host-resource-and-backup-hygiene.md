# Host resource and Git-backup hygiene

## Scope

Use this playbook for unattended Hermes hosts where agent tasks, development servers, language servers, media rendering, and scheduled backups share limited RAM and disk.

## Full host audit before stopping anything

Collect and classify, not just rank by RSS:

1. RAM: `free`, `/proc/meminfo`, memory PSI, `vmstat`, swap availability, cgroup `memory.current`, `memory.max`, and `memory.events`.
2. CPU: core count, load, CPU PSI, and current high-CPU bounded work such as FFmpeg or builds.
3. Storage: bytes, inodes, I/O PSI, Git object/pack size, open-deleted files, and major directory sizes.
4. Processes: PID/PPID, age, RSS, CPU, command, CWD, process tree, listeners, open/deleted files, and launch metadata.
5. Services: systemd/s6 state, containers, user sessions, zombies, and network listeners.
6. Automation: Hermes cron jobs, system cron/timers, currently running jobs, overlap windows, last status, and exact failure output.

Low `MemFree` alone is not proof of unhealthy RAM; use `MemAvailable` and PSI. No swap plus historical OOM increments means the machine lacks burst resilience even when current PSI is low. Cgroup OOM counters can preserve evidence not present in a short journal window.

## Process classification

Classify each process as one of:

- **Active bounded work**: current FFmpeg render, build, test, migration. Keep it while CPU/output/progress is active.
- **Required service**: gateway, dashboard, provider, API, MCP server, production listener. Verify listener and launch metadata.
- **Restartable development helper**: Pyright, tsserver, language server. Old instances with no active client/listener are strong stop candidates, but still require lifecycle approval.
- **Expired bounded task**: a `gradlew run --no-daemon`, test client, or preview launched with completion notification that survives for days. Strong stop candidate.
- **Redundant preview/service**: multiple production/dev instances of the same app on different ports. Ask which canonical port should remain.
- **Unknown**: inspect CWD, parent, sockets, registry, and project context before deciding.

Hermes background-process metadata (commonly `processes.json`) is high-value evidence: it reveals the original command, CWD, session/channel, whether completion was expected, and whether the process was meant to be permanent. A process registered as bounded with `notify_on_complete` is not automatically a service merely because it survived.

Never kill by age/RSS alone. Present exact process groups and expected memory recovery, preserve active renders and required services, and obtain approval for a precise scope. Terminate the parent process group gracefully, then verify descendants, listeners, RAM, and task state.

## Monitoring design

Use two complementary alert-only monitors:

- **Frequent pressure watchdog** (for example every 30 minutes): silent when healthy; alert on low `MemAvailable`, sustained memory full PSI, disk threshold, or an increased cgroup OOM-kill counter. Persist the prior OOM count and alert signature; rate-limit repeated alerts.
- **Daily stale-process digest**: report old high-RSS development processes with PID, age, RSS, command/CWD, and `alert_only` status.

Do not schedule automatic termination unless the user separately authorizes an exact lifecycle policy. Monitoring output must explicitly say that no process was stopped.

## Cron planning

- Stagger media generation, backup, cleanup, and monitoring so heavy tasks do not begin together.
- Script-only health checks should use `no_agent=true`; empty stdout means healthy/silent.
- Inspect last-run output before changing a schedule. A non-fast-forward Git push, auth failure, or bad source state is not fixed by retry frequency.
- Smoke-test scripts directly and manually run a newly created/updated job once.
- Route operations/resource alerts to the code/operations channel, not content or personal channels.

## Git backup policy

A Git backup should preserve human-authored and recovery-defining state, not reproduce the host filesystem.

Back up:

- source, tests, docs, migrations, manifests and lockfiles;
- deployment definitions without secrets;
- submodule pointers and `.gitmodules`;
- Hermes skills, scripts, hooks, plugin source/config, cron definitions, profile preferences, and sanitized templates;
- curated runbooks, decisions, journal summaries, and deliberate recovery bundles.

Omit:

- temporary collectors, raw scans, one-off outputs, scratch clones/worktrees;
- package stores, SDK downloads, virtualenvs, `node_modules`, build output, provider caches;
- sessions, logs, process state, locks, browser/media caches, generated audio/video;
- runtime databases/WAL/SHM, OAuth pending state, credentials, tokens, and private keys.

Enforce the policy in both `.gitignore` and the backup copier. Add a fail-closed pre-commit/staging verifier that rejects generated/runtime prefixes, secret-like filenames, runtime database suffixes, and oversized blobs. Validate with an isolated temporary Git index so the live staging area is untouched; scope `GIT_INDEX_FILE` to a subprocess to avoid contaminating later commands.

Parent `.gitignore` rules do not govern files inside child submodules. Audit each child repository's own ignore rules; the parent backup should normally store only the Git pointer.

Before untracking files already covered by new ignore rules, report counts and major groups. `git rm --cached` and history rewriting are separate, approval-requiring phases. A `.gitignore` improvement prevents future additions but does not shrink existing history.

## Common pitfalls

- Treating `MemFree` as available RAM.
- Calling an active render stale because it ranks high by RSS/CPU.
- Assuming an old process is intentional solely because it appears in a process registry.
- Auto-killing language servers without checking active clients or getting approval.
- Rescheduling a failed backup without reading the Git/auth/error output.
- Running alternate-index tests with a globally exported `GIT_INDEX_FILE`, causing false mass-deletion status output.
- Blanket-ignoring a journal directory that mixes durable decisions with reproducible raw output.
