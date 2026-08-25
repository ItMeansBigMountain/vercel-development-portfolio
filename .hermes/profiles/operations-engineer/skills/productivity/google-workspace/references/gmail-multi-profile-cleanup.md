# Gmail Multi-Profile Cleanup Pattern

Use this when the user asks to clean, unsubscribe, archive, spam, or otherwise modify Gmail across multiple Google Workspace/OAuth profiles.

## Pitfall

Do **not** start bulk Gmail cleanup just because a token directory contains multiple profiles. Always ask the user to confirm the target scope before modifying messages:

- `one profile`
- `all listed profiles`
- `only newsletters/junk`
- `only unread messages`
- `archive/trash/spam/unsubscribe`

## Token layout

For this workspace, profile-scoped Gmail OAuth tokens live under:

```text
/opt/data/secrets/google/tokens/<profile>/google_token.json
```

Known profiles in this setup:

- `personal-main`
- `personal-secondary`
- `hermes-agent`
- `burner`
- `classicalechos`

## Safe workflow

1. **Audit first, per profile.**
   - Get the account email for each profile.
   - Count actual Inbox messages with `labelIds=["INBOX"]`; do not use total mailbox counts.
   - Search newsletter/junk candidates with Gmail queries such as `subject:(newsletter OR digest OR weekly OR summary OR unsubscribe)` and sender probes for known junk senders.
   - Fetch metadata only at first: From, Subject, Date, labels, snippet.

2. **Classify before acting.**
   - Keep priority items: billing/charges, security, cloud/API bills, brokerages, tickets, official notices.
   - Keep user-interest newsletters separately if requested.
   - Mark generic consumer sales/promos and duplicate newsletters as cleanup candidates.

3. **Get explicit scope approval.**
   - Show profile, sender/category, count, examples, and proposed action.
   - Do not trash, spam, delete, unsubscribe, or label messages until the user approves the exact scope.

4. **Act only on approved message IDs.**
   - For cleanup: remove `INBOX`/`UNREAD`.
   - For junk: add `SPAM` or trash only if approved.
   - For unsubscribe: use Gmail's unsubscribe route only when available; otherwise report that the email was cleaned but unsubscribe was not processed.

5. **Verify.**
   - Re-count actual Inbox messages for each modified profile.
   - Report counts and any failed message IDs.
   - Do not claim an unsubscribe succeeded unless the unsubscribe action was actually processed.
