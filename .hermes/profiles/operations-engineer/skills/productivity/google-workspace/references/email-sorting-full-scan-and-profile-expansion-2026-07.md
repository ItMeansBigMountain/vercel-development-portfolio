# Email sorting full scan and profile expansion (2026-07)

Use this when the user asks to add all readable Google email accounts to the deterministic email sorter or run a full email scan.

## Current sorter shape

- Core script: `/opt/data/scripts/email_sorting_agent.py`
- Cron wrapper: `/opt/data/scripts/email_sorting_agent_apply.sh`
- Morning cron job: `Morning email sorting agent`, script `email_sorting_agent_apply.sh`
- Normal cron scan limit: `--max-results 250`
- Full scan pattern: run with `--max-results 5000`.

## Active readable Gmail profiles for sorting

The sorter should cover all Workspace profiles with working Gmail read/modify tokens:

- `personal-main` / `affan.fareed@gmail.com`
- `personal-secondary` / `fareed320@gmail.com`
- `trapiistan` / `trapiistan@gmail.com`
- `classicalechos` / `classicalechos@gmail.com`
- `burner` / `laflametoast@gmail.com`

Do not include stale aliases or revoked tokens in the default sorter:

- `fareed320` is a legacy alias for `personal-secondary`; avoid scanning both to prevent duplicate work.
- `*.old-*` profile directories are historical backups.
- `hermes-agent` had `invalid_grant` during the 2026-07 full scan; add it only after reauth and live Gmail identity verification succeeds.

## Safe expansion workflow

1. Inventory `/opt/data/google_profiles/*/google_token.json` and `/opt/data/HeRmEz/projects/_ops/google-email-profiles.json`.
2. For each candidate profile, run a harmless Gmail live probe with Gmail readonly/modify scopes:
   - load token
   - refresh if needed
   - `gmail.users().getProfile(userId='me')`
3. Add only profiles that successfully return the expected email address.
4. Patch `PROFILES` in `/opt/data/scripts/email_sorting_agent.py`.
5. Compile/check the script.
6. Run a full apply scan:
   - `python3 /opt/data/scripts/email_sorting_agent.py --apply --max-results 5000`
7. Verify with a dry run:
   - `python3 /opt/data/scripts/email_sorting_agent.py --max-results 5000`

## Verification interpretation

A nonzero remaining dry-run match is not always a failure. Grammarly Insights routes to `Hermes/Personal Info` with `remove_inbox=False`, so it can remain visible in Inbox by design.

Report by profile with compact bullets: accounts scanned, sorted counts by label, blocked accounts, and any intentionally retained Inbox items.
