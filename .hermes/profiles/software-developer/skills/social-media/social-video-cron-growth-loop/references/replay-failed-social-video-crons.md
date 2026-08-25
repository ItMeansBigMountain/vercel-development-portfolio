# Social-video cron replay after authentication or provider repair

Use this when the user asks to look back across recent sessions and replay work that was blocked by an OAuth, provider, or setup repair. The goal is selective recovery of unfinished product work—not indiscriminate rerunning of every historical error.

## 1. Build an affected-run ledger

Search recent conversation and cron sessions by exact job name/ID, script name, repaired failure signature (`invalid_grant`, revoked token, channel mismatch), and structured status such as `blocked_auth`.

For each candidate record:

- When it ran and which lane/account it used
- Exact blocking dependency
- Whether a later successful run superseded it
- Whether its output is still useful now
- Whether replay has side effects or competes for an exclusive lock

Do not infer that every job discussed near an auth incident was auth-blocked.

## 2. Apply replay eligibility before acting

Replay only when all are true:

1. The repaired dependency actually blocked the run.
2. The intended output is still useful and not stale.
3. A later run did not already complete or supersede the same work.
4. The lane is currently enabled by user policy.
5. Replaying will not duplicate uploads or compete with an active upload lock.

### Usually replay

- Workspace sorting that could not read authorized profiles
- One current morning/operator collection after Workspace repair
- Metrics collection that failed on the repaired YouTube token
- Current creator discovery/upload work stopped by upload OAuth
- Rendered upload queues that failed only at authenticated upload

### Usually do not replay

- A paused faceless/newsletter lane unless explicitly resumed
- Historical market/trading decisions whose data is stale
- Old reports fully superseded by one current live report
- Runs already superseded by later verified uploads
- Source-download failures, bot checks, duplicate rejections, timeouts, or provider failures unrelated to repaired OAuth

## 3. Run cheap deterministic preflights

Before expensive rendering/uploading, verify Workspace profiles, run the current metrics monitor, run YouTube token/channel identity health, inspect queue and duplicate state, confirm lane pause/enable state, and inspect the upload lock.

A healthy preflight proves only that the dependency is repaired. It does not prove the blocked product job finished.

## 4. Replay in dependency order

Safe default:

1. Email/source sorting
2. Metrics and auth/channel watchdogs
3. Current operator/report collector
4. Creator discovery feeder
5. Daily uploader or backlog drainer only if still needed after feeder output

Serialize jobs sharing an upload lock or duplicate ledger. Do not launch feeder, daily uploader, and backlog drainer concurrently. If Viral Radar is active and faceless/newsletter publishing is paused, exclude faceless jobs.

## 5. Verify product output after scheduler execution

`cron run` returning `execution_success=true` or `last_status=ok` is scheduler evidence only. After each replay:

1. Open the new cron session or persistent application artifact.
2. Read the final assistant/application result.
3. Check upload IDs/URLs, logs, queue state, and source/duplicate failures.
4. Classify product status independently.

Statuses:

- `ok_uploaded`: verified video ID/URL and durable log
- `ok_metrics`: current metrics fetched without token errors
- `ok_collected`: live Workspace context from intended profiles
- `ok_noop`: no eligible work after a valid check
- `partial`: exact deficit and reason stated
- `blocked_auth`, `blocked_source`, `blocked_provider`, or `blocked_duplicate`
- `scheduler_timeout`: scheduler killed the run; application outcome is unknown unless durable logs prove it

An empty upload queue is not completion: missing clips may never have rendered and thus never entered it.

## 6. Stop when the blocker changes

If authentication is healthy but replay now stops on source acquisition, missing media, or duplicate checks:

- Record auth recovery as successful.
- Report the new blocker with raw evidence.
- Do not repeatedly rerun expensive jobs that will deterministically hit it.
- Continue only when another approved source-ready candidate or fallback can materially advance work.

## Reporting

State:

- Jobs replayed and product outcomes
- Verified URLs or metrics counts
- Jobs deliberately not replayed and why (paused, stale, superseded, unrelated)
- Exact remaining blocker and next dependency

Do not say “all blocked jobs finished” when auth recovery succeeded but source/render/upload deficits remain. Say all **auth-blocked work was replayed**, then separately describe unresolved non-auth blockers.

## Pitfalls

- Scheduler success is not product success.
- Historical proximity is not causal proof.
- Do not replay paused lanes or stale decisions by default.
- Do not run upload-lock-sharing jobs concurrently.
- Do not delete newsletter/source emails without a verified corresponding upload ID.
- Viral Radar still requires transformative hook/context/captions/attribution.
