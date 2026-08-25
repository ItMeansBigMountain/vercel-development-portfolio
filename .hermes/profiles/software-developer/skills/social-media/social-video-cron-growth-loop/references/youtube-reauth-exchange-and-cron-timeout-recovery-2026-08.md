# YouTube OAuth recovery and long-running cron verification (2026-08)

Use this pattern when Viral Radar repeatedly reports `invalid_grant`, the queue is preserved, and a replay later reports a scheduler timeout.

## OAuth exchange: trust the live CLI syntax

1. Generate a fresh URL per profile with:
   ```bash
   python3 /opt/data/scripts/google_reauth_workflow.py youtube-auth-url <profile>
   ```
2. Have the user return the complete `http://localhost:1/?state=...&code=...` callback URL. An unreachable localhost page is expected; the browser address bar still contains the required URL.
3. Exchange with the currently supported syntax:
   ```bash
   python3 /opt/data/scripts/google_reauth_workflow.py youtube-exchange <profile> '<full callback URL>'
   ```
   Do not assume `youtube-exchange` accepts a `--verify` flag merely because recovery output suggests it. If the helper rejects an option, rerun without that option; argument parsing occurs before token exchange, so the authorization code has not been consumed.
4. Verify all profiles separately:
   ```bash
   python3 /opt/data/scripts/youtube_auth_healthcheck.py --verbose
   ```
5. Require `valid: true`, exact channel ID/title match, required scope set, and a retained refresh token before resuming upload jobs.
6. Run the metrics monitor as an independent live API probe. This distinguishes restored OAuth from a token that merely serialized successfully.

## Pause/replay discipline

- After confirming a repeated hard auth blocker, pause only the affected upload/discovery/backlog jobs so they do not keep generating noisy failures. Preserve the auth watchdog.
- Confirm active and held queue counts before any replay.
- After successful verification, resume the paused jobs and drain the rendered queue first.
- Verify success from the upload ledger and returned public URL, not from queue disappearance or scheduler status alone. A timed-out wrapper may have uploaded and cleaned the queue item before being killed.

## Script-only scheduler timeout pitfall

A `no_agent=true` cron can be terminated by the scheduler's fixed script timeout even when the underlying media pipeline is behaving correctly. Long clip/discovery pipelines commonly exceed that window after the initial queue drain.

If a deterministic wrapper repeatedly exceeds the script-only timeout:

1. Keep durable logging with `tee` so partial output survives scheduler termination.
2. Inspect the newest raw log, queue state, and upload ledger before retrying; do not duplicate an upload that completed before timeout.
3. Convert the cron to an agent-run job when reasoning and a longer terminal timeout are required:
   - clear `script`;
   - set `no_agent=false`;
   - attach the social-video skill;
   - restrict tools to terminal/file;
   - instruct the agent to execute the wrapper via terminal with an explicit long timeout;
   - require raw-log, queue-count, ledger, and public-URL verification.
4. Run the updated cron once and require `execution_success: true`, then rerun auth health and queue probes.

Do not paper over timeouts by reporting the scheduler's status as product success. Conversely, do not call a public upload failed solely because the scheduler timed out after the ledger recorded it.
