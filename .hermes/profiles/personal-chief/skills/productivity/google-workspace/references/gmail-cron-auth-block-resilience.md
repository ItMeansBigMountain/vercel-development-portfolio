# Gmail Cron Auth-Block Resilience

Use this pattern for recurring Gmail/Workspace cron jobs that process multiple Google profiles.

## Durable lesson

A single revoked/expired Google token (`invalid_grant`) or insufficient-scope profile should not crash the whole cron job when other profiles can still be processed. Treat per-profile auth failures as structured blocks, continue with healthy profiles, and exit successfully when the job's business logic handled the block cleanly.

## Recommended pattern

1. Define the job's default profile list from the action policy, not from every token directory.
   - Exclude read-only profiles from write/move/delete jobs.
   - Exclude automation/service profiles unless they are explicitly part of that lane.
2. Wrap each profile's credential refresh and Gmail API calls independently.
3. Return per-profile status objects such as:
   - `ok: true`, `match_count: N`, `matches: [...]`
   - `ok: false`, `blocked: "auth"`, `error: "invalid_grant..."`
   - `ok: false`, `blocked: "permission"`, `status: 403`, `error: "insufficient scopes..."`
4. Let the wrapper script print a concise notification only when:
   - messages were actually moved/labeled, or
   - profiles are blocked and need reauth/scope repair.
5. Keep the process exit code `0` for handled auth blocks so the cron scheduler does not report a misleading traceback/error. Use nonzero only for unhandled script/runtime failures.
6. Generate a fresh profile-scoped OAuth URL for blocked profiles using `/opt/data/scripts/google_reauth_workflow.py`, then exchange and verify after the user returns the callback.

## Python exception handling sketch

```python
from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError

try:
    service = gmail(profile)
    # process messages...
    return {"profile": profile, "ok": True, "match_count": len(matches)}
except RefreshError as exc:
    return {"profile": profile, "ok": False, "blocked": "auth", "error": safe(exc)}
except HttpError as exc:
    status = getattr(getattr(exc, "resp", None), "status", None)
    blocked = "permission" if status in {401, 403} else "api"
    return {"profile": profile, "ok": False, "blocked": blocked, "status": status, "error": safe(exc)}
```

## User-specific policy reminder

For this user's email sorting lane, do not default to modifying `personal-main / affan.fareed@gmail.com`; it is read-only for Gmail. `personal-secondary / fareed320@gmail.com`, `classicalechos`, and `burner` are the normal writable sorting lanes unless the user explicitly changes the policy.
