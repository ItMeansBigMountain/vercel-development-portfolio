# Replay failed Google cron runs after OAuth repair

Use this when a Google Workspace OAuth failure caused cron jobs or automation attempts to fail and the user asks to "go back", "rerun failures", or "fix all errors".

## Pattern

1. **Search session history for the failing class**
   - Search for the job name/id, script name, and errors such as `invalid_grant`, `invalid_scope`, `RefreshError`, `insufficient authentication scopes`.
   - Extract a compact list of affected jobs/scripts before rerunning anything.

2. **Repair the exact token first**
   - Use `/opt/data/scripts/google_reauth_workflow.py` for Workspace or YouTube OAuth lanes.
   - Exchange the user callback, then verify with the built-in harmless probes.
   - Confirm the returned account/channel identity matches the expected profile; `login_hint` is not an account lock.

3. **Rerun affected attempts one by one**
   - Start with the smallest deterministic script or no-agent cron script.
   - Then rerun the dependent cron job if applicable.
   - Record each result as `fixed`, `still_blocked_auth`, `blocked_source`, `blocked_provider`, `blocked_quality`, or `ok_noop` instead of a vague pass/fail.

4. **Do not let one broken profile crash multi-profile jobs**
   - Multi-profile collectors/sorters should catch `RefreshError` and `HttpError` per profile, emit a structured block for that profile, and continue with healthy profiles.
   - For Gmail-modifying jobs, do not include intentionally read-only profiles (for this user, `personal-main / affan.fareed@gmail.com`) in default modifying passes.

5. **After rerun, trigger or inspect cron status**
   - If the script path is deterministic and safe, run it directly first.
   - Then run the cron job manually and confirm `last_status` updated to `ok` or a meaningful structured blocker.

## Reporting format

Use concise bullets:

- `Job/script` — rerun result.
- What changed/fixed.
- Remaining blocker and exact next input needed from the user, if any.

Avoid claiming the whole system is fixed when downstream lanes still have separate OAuth/provider/source blockers.

## Pitfalls

- Do not treat a scheduler `ok` as product success if the business result is `blocked_auth`, `blocked_provider`, or `no upload`.
- Do not rerun upload/destructive cleanup blindly after auth repair; verify upload IDs before trashing source emails.
- Do not preserve one-off job run narratives in the skill; keep only the recovery pattern and durable profile policies.
