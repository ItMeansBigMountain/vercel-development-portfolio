# Email triage + cleanup policy notes

Session-derived policy for the user's morning-report/email-cleanup workflow.

## Importance buckets

**Always prioritize / preserve for review**

- Landing emails are important only when they can affect the user's actual housing/rent workflow: Landing Standby bump/rebook notices, active stay changes, payment/rent, parking, mail/packages, pets, support, or similar logistics. Do not treat generic Landing marketing as priority.
  - Landing Standby context: the user primarily pays rent through Landing Standby. Standby offers furnished apartments at a lower fixed monthly rate in exchange for mobility; members can be bumped when a standard booking takes the unit and typically get 3 days' notice to choose/rebook another Standby home. Bump/rebook/payment messages are high priority.
- Billing, charges, receipts, Chase, Apple/Card receipts, Robinhood, Ticketmaster, cloud/devops/API/security, official/vehicle registration, garage/security alerts, and similar life/admin signals should be surfaced before newsletters.
- Credit Karma should not be read aloud/summarized by default. Suppress it from priority, unread, and recent-sample sections unless the email clearly indicates the user's credit score dropped/decreased. Do not surface generic Credit Karma marketing, duplicate-charge promos, monitoring nudges, or account-connection nags.

**Interesting/source material**

- TLDR is useful and can be sourced for latest news, but for this user's account setup it should be treated as canonical only on `fareed320@gmail.com` unless the user changes that account-role rule.
- Kino Body, Daily Stoic, and Grammarly Insights can be summarized through the user's personal interests/self-improvement profile, then offered as cleanup candidates after review.

**Known junk examples**

- FoundersCard, Yieldi, Crunch, Higgsfield.
- Previously established junk examples include Fundrise, Kling AI, Instagram notifications, Lumen marketing, Chess.com nags, YEEZY, City Experiences, LELO, GNC, and generic promotional/sales mail.

## Cleanup actions and safety

- Junk email action means: unsubscribe when practical, report as spam when appropriate, then delete/trash.
- Never delete, unsubscribe, report spam, archive, or otherwise mutate email unless the user explicitly approved that action/rule.
- If the user explicitly says a sender/category is junk or can be deleted, that is enough approval for that named scope only; do not broaden it to adjacent senders without asking.
- Before acting, check that the active credentials/scopes permit the requested write action. If permissions are insufficient, tell the user exactly what re-authentication or scopes are needed.
- Keep destructive-action summaries concise and auditable: account, sender/category, count, and action performed.

## Subscription audit pattern

When asked to review subscriptions:

1. Scan recent mail/newsletters across all configured profiles read-only.
2. Group by sender/publication and account.
3. Classify each group: keep, interesting/source, review, junk.
4. Present a short approval list for destructive actions.
5. Only after approval: unsubscribe/report spam/delete within the approved sender/category/account scope.
