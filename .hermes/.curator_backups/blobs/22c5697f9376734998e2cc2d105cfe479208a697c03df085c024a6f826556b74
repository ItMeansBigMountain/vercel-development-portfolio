# Raw application logs for timed-out social-video cron scripts

Use this when a `no_agent=true` social-video cron reports only a generic provider/script timeout and the user wants the underlying application failure.

## Diagnose from the source of truth

1. Read the persisted cron artifact under `$HERMES_HOME/cron/output/<job_id>/<run-time>.md` before repeating the Discord summary. `$HERMES_HOME` may differ from `$HOME`; resolve it from the live environment/config rather than assuming `~/.hermes`.
2. Inspect gateway/agent logs around the exact run timestamp only as secondary scheduler context.
3. Read the scheduled wrapper. If it redirects child stdout/stderr to a temporary file and prints it only after the child exits, a scheduler kill can erase the only application trace.
4. State the distinction clearly: a scheduler message such as “provider timeout” may wrap a deterministic `no_agent` script timeout. Quote the raw artifact and do not infer a model-provider failure when the artifact says the script exceeded its limit.

## Timeout-safe wrapper pattern

Persist and stream child output while retaining the child exit code:

```bash
log_dir="$ROOT/OUTPUTS/backlog-processor-logs"
mkdir -p "$log_dir"
output="$log_dir/$(date -u +%Y-%m-%dT%H%M%SZ).log"
printf 'raw_log: %s\n' "$output"
set +e
"$PYTHON" "$RUNNER" 2>&1 | tee "$output"
rc=${PIPESTATUS[0]}
set -e
```

This ensures partial output survives a scheduler timeout both in cron capture and on disk. Avoid `mktemp` plus an EXIT deletion trap for the only copy of long-running application logs.

## Reporting format for this user

- When mentioning a failure, include the relevant raw application or scheduler lines, not only a prose classification.
- Put multiline commands and logs in Discord-compatible fenced blocks with a language tag such as `bash`, `text`, or `json`.
- Be verbose enough to show the failing stage, timestamps, exit/timeout condition, artifact path, and nearby stderr. Separate raw logs from interpretation.
- If historical application output was not preserved, quote the surviving scheduler artifact, explain exactly why deeper logs are unavailable, and repair logging for future runs. Never fabricate a traceback.
- Do not publicly rerun an upload-capable pipeline merely to regenerate logs unless the user authorized the side effects.
