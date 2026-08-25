# Auth-error triage and batch reauth repair — 2026-06

Use this when the user says to "look back at errors" and tackle Google/YouTube auth failures.

## Pattern

1. **Start from history, then verify live state.**
   - Use session history to recover the reported auth failures and affected jobs.
   - Do not rely only on old generated OAuth links or prior summaries; tokens and pending PKCE state can be stale.
   - Run the unified helper inventory and live probes before telling the user what still needs action:
     - `python3 /opt/data/scripts/google_reauth_workflow.py inventory`
     - `python3 /opt/data/scripts/google_reauth_workflow.py verify workspace <profile>`
     - `python3 /opt/data/scripts/google_reauth_workflow.py verify youtube <profile>`

2. **Group by auth lane, not by cron job.**
   - Workspace profiles: Gmail/Calendar/Drive/Docs/Sheets/Contacts scope and refresh-token health.
   - YouTube profiles: upload/metadata/private read/analytics scopes and channel identity.
   - Explain which downstream jobs are blocked only after identifying the broken auth lane.

3. **Regenerate fresh auth URLs after live failures.**
   - If a token reports `invalid_grant`, `insufficient authentication scopes`, or a stale/narrow scope set, generate a new URL with the helper.
   - Prefer one labeled Markdown bundle under `/opt/data/HeRmEz/projects/_ops/` over pasting many long URLs into chat.
   - Include account/channel expectations and paste-back labels.

4. **Exchange callbacks and verify harmless probes before replay.**
   - Exchange callbacks with the matching helper command for `workspace` or `youtube`.
   - Verify the returned token owns the expected email/channel before declaring repair complete.
   - Only after live verification should blocked cron runs or uploads be replayed.

## Pitfalls

- Scheduler `ok` is not product success; auth-blocked jobs may still finish without producing useful output.
- A profile can have a valid Gmail token but still lack Calendar/Drive scopes; report this as partial auth, not healthy.
- `login_hint` is not an account lock. The consent-screen account must match the label before the user approves.
- Do not paste tokens, refresh tokens, client secrets, or full credential JSON into chat or reference files.
