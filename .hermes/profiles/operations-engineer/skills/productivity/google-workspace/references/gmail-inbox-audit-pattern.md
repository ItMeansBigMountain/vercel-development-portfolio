# Gmail Inbox Audit Pattern

Use this when auditing a user's Gmail inbox/subscriptions or preparing cleanup actions.

## Safety workflow

1. Start read-only: list messages, labels, senders, subjects, and counts only.
2. Classify into: important/keep, review/summarize, likely junk, approved junk, duplicate-subscription cleanup.
3. Never delete, spam-report, unsubscribe, trash, archive, mark read, or apply labels until the user explicitly approves the exact batch.
4. For user-specified junk senders, treat that as a cleanup candidate, but still show the batch if the current instruction is an audit rather than an explicit cleanup command.
5. Preserve billing/charge/subscription/finance/security signals unless explicitly approved for cleanup.

## Counting pitfall

Do not rely on Gmail `resultSizeEstimate` or a broad `q="in:inbox ..."` estimate for actual inbox counts. It can return misleading rounded/sentinel-looking values. For an actual inbox audit, enumerate messages using `labelIds=['INBOX']` and count the returned message IDs, paginating through `nextPageToken`.

When combining label filters with search queries in the Gmail API, prefer:

```python
users().messages().list(userId='me', labelIds=['INBOX'], q='newer_than:90d', maxResults=500)
```

Then count `len(messages)` across pages and fetch metadata with `format='metadata'` and only needed headers (`From`, `Subject`, `Date`, `List-Unsubscribe`).

## User-facing reporting

Keep the report inbox-only unless the user asks for all mail. Explicitly state whether the scan was Inbox-only vs All Mail. Use compact bullets and separate:

- Approved junk ready for cleanup
- Likely junk needing approval
- Keep / important
- Review or summarize then decide

For cleanup confirmation, ask the user to approve the category or exact sender batch before any destructive action.
