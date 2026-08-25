# Gmail Inbox Audit + Cleanup Pattern

Use this when the user asks to audit, triage, or clean up Gmail inboxes across profile-scoped Google OAuth accounts.

## Core safety rule

- Gmail cleanup is destructive enough to require explicit approval.
- Do **read-only audit first**: list profiles, actual Inbox counts, sender/subject/category buckets.
- Only after the user approves a sender/category should you modify labels, report spam, trash, delete, or unsubscribe.
- Morning-report jobs must stay read-only and only propose cleanup candidates.

## Count actual Inbox, not broad mailbox totals

Pitfall: `users.getProfile().messagesTotal` is all-mail-ish profile metadata, not Inbox count. Also `messages.list(q="in:inbox", maxResults=1).resultSizeEstimate` can be misleading for small mailboxes.

Preferred actual Inbox count pattern:

```python
def count_inbox(gmail):
    total = 0
    page = None
    while True:
        kwargs = {"userId": "me", "labelIds": ["INBOX"], "maxResults": 500}
        if page:
            kwargs["pageToken"] = page
        resp = gmail.users().messages().list(**kwargs).execute()
        total += len(resp.get("messages", []))
        page = resp.get("nextPageToken")
        if not page:
            return total
```

For filtered Inbox searches, pass both `labelIds=["INBOX"]` and a query like `q="is:unread newer_than:14d"` instead of relying only on `q="in:inbox ..."`.

## Audit shape

For each profile:

1. Get account email with `gmail.users().getProfile(userId="me")`.
2. List actual Inbox messages with `labelIds=["INBOX"]`.
3. Fetch metadata only: `From`, `Subject`, `Date`, labels, snippet.
4. Classify into concise buckets:
   - **Priority**: billing/charges/receipts, credit-card/bank, subscriptions, cloud/AI APIs, portfolio/brokerage, tickets, security, official notices.
   - **Interesting/source**: newsletters/content the user wants summarized before cleanup.
   - **Cleanup candidates**: known junk senders/categories and duplicate subscriptions.
   - **Needs review**: ambiguous service/marketing/account emails.
5. Show exact sender/count examples before acting.

## Cleanup action pattern

When the user approves junk cleanup:

- Operate on the approved message IDs only.
- For spam-like marketing/junk, use Gmail modify to remove `INBOX`/`UNREAD` and add `SPAM` when appropriate, then `trash` if the user approved deletion/trashing.
- Verify by re-counting actual Inbox per profile.
- Report counts and failures; do not claim unsubscribe happened unless you actually processed the unsubscribe route.

Example modification:

```python
gmail.users().messages().modify(
    userId="me",
    id=message_id,
    body={"addLabelIds": ["SPAM"], "removeLabelIds": ["INBOX", "UNREAD"]},
).execute()
gmail.users().messages().trash(userId="me", id=message_id).execute()
```

## User-specific email policy snapshot

Current user preference for email triage:

- Priority: billing/charges/receipts, Chase, Apple receipts/Card, cloud services, AI APIs, Robinhood account/transaction/brokerage/security mail, Landing, Ticketmaster ticket/venue info, myQ/Chamberlain garage alerts, GitGuardian/security, official/vehicle notices.
- Priority: billing/charges/receipts, Chase, Apple receipts/Card, cloud services, AI APIs, Robinhood account/transaction mail, Landing, Ticketmaster ticket/venue info, myQ/Chamberlain garage alerts, GitGuardian/security, official/vehicle notices.
- TLDR: source only from `fareed320@gmail.com`; TLDR on other accounts is duplicate cleanup.
- Source/newsletter: Kino Body, Daily Stoic, and Robinhood Snacks (`hello@snacks.robinhood.com`) are content sources, not account/finance mail.
- Priority/finance: Robinhood account/transaction emails go to finance/review; do not group Robinhood Snacks with these.
- Junk: FoundersCard, Yieldi, Crunch, Higgsfield, Fundrise, Kling AI, Instagram notifications, Lumen marketing, Chess.com nags, YEEZY, City Experiences, LELO, GNC, generic consumer sales/promotional emails.
- Junk: FoundersCard, Yieldi, Crunch, Higgsfield, Fundrise, Kling AI, Instagram notifications, Lumen marketing, Chess.com nags, YEEZY, City Experiences, LELO, GNC, generic consumer sales/promotional emails.
- Unity is fine/keep.
- Always confirm before destructive email actions unless the user has explicitly approved that sender/category in the current cleanup request.
