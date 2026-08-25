# Gmail email sorting agent rules

Use this reference when maintaining Hermes-level Gmail sorting for the user's five Google profiles.

## Purpose

Keep Inbox clean without losing high-signal source material. Sorting should usually create/apply Gmail labels and remove `INBOX`; it should not delete source or priority mail.

## Current source/finance split

- `Hermes/Source/TLDR` — TLDR newsletters, with `fareed320@gmail.com` as preferred TLDR source.
- `Hermes/Source/Daily Stoic` — Daily Stoic lessons/source emails.
- `Hermes/Source/Kino Body` — Kino Body health/fitness source emails.
- `Hermes/Source/Robinhood Snacks` — **Robinhood Snacks is a financial markets newsletter**, not Robinhood account mail.
- `Hermes/Finance/Robinhood/Order Receipts` — Robinhood brokerage order lifecycle receipts from `noreply@robinhood.com`, including executed, placed, and canceled/cancelled order confirmations. This specific rule must run before the broader Robinhood account-mail rule.
- `Hermes/Finance/Robinhood` — other Robinhood account, deposit, statement, trade-confirmation, brokerage, and security-related mail.

## Important pitfall

Do not classify `hello@snacks.robinhood.com` / `snacks.robinhood.com` as Robinhood finance/account mail just because the domain includes `robinhood.com`. Route it before the broader Robinhood rule, to `Hermes/Source/Robinhood Snacks`.

## Self-sent mail exemption

Never sort, relabel, archive, or remove `INBOX` from a message whose parsed `From` address is one of the user's managed account addresses. Apply this exemption before every content/sender classification rule so mail the user sends between their own accounts— including the `💌` “your day ahead” message—stays unsorted in the general Inbox.

## Safe action pattern

1. Dry-run first across all profiles and show counts/examples when exploring a new sender class.
2. For explicitly requested sender/folder routing, create the Gmail label if missing.
3. Apply the label and remove `INBOX` for matched messages.
4. Re-run dry-run or direct label counts to verify no matching messages remain in Inbox.
5. Morning cron can run the deterministic sorter and stay silent when no messages are sorted.

## Current deterministic sorter

Local script path used in this environment:

- `/opt/data/scripts/email_sorting_agent.py`
- wrapper cron script: `/opt/data/scripts/email_sorting_agent_apply.sh`

The sorter should cover all readable approved Workspace Gmail profiles, currently including `personal-main`, `personal-secondary`, `trapiistan`, `classicalechos`, and `burner`. Do not include a locally present profile such as `hermes-agent` unless a live Gmail verification succeeds; report `invalid_grant`/blocked tokens as needing reauth.

If maintaining this workflow, keep rules ordered from most-specific to broadest. Newsletter/source rules should run before broader finance/account rules.

- `personal-main` / `affan.fareed@gmail.com`
- `personal-secondary` / `fareed320@gmail.com`
- `trapiistan` / `trapiistan@gmail.com`
- `classicalechos` / `classicalechos@gmail.com`
- `burner` / `laflametoast@gmail.com`

If maintaining this workflow, keep rules ordered from most-specific to broadest. Newsletter/source rules should run before broader finance/account rules. For adding newly readable accounts or running a full scan, use `references/email-sorting-full-scan-and-profile-expansion-2026-07.md`; do not add stale aliases like `fareed320` or revoked-token profiles like `hermes-agent` until reauth and live Gmail identity verification pass.
