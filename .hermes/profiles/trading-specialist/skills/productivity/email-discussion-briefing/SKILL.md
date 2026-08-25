---
name: email-discussion-briefing
description: Read the user's current Gmail profiles read-only, summarize what matters, and prepare discussion topics without deleting or modifying email.
version: 1.0.0
created_by: agent
---

# Email Discussion Briefing

Use this skill when the user asks to read through email, discuss current email, summarize inbox state, identify important messages, or decide what to do with emails.

## Scope and safety

- Default to read-only Gmail access.
- Do not trash, archive, label, unsubscribe, report spam, send replies, or modify messages unless the user explicitly approves the exact action and scope.
- Exception only if a separate established pipeline rule applies, such as newsletter source emails being trashed after verified YouTube upload.
- Never expose OAuth tokens, auth URLs, recovery codes, passwords, or credential filenames that reveal secrets.
- As of explicit user instruction on 2026-06-29, both personal accounts (`personal-main / affan.fareed@gmail.com` and `personal-secondary / fareed320@gmail.com`) have full Gmail/Workspace read-write permission. Still default email review/audit to read-only, and do not trash/archive/label/send unless the user approves the exact action/scope or an established source-email cleanup rule applies.

## User's known Gmail profiles

Use these profile tokens under `/opt/data/google_profiles/<profile>/google_token.json` when present:

- `personal-main` → `affan.fareed@gmail.com`, primary personal, full Gmail/Workspace read-write permission.
- `personal-secondary` → `fareed320@gmail.com`, newsletter/source account, full Gmail/Workspace read-write permission.
- `trapiistan` → `trapiistan@gmail.com`, Trapiistan/Sosai automation account.
- `classicalechos` → `classicalechos@gmail.com`, Classical Echos channel/account.
- `burner` → `laflametoast@gmail.com`, temporary/burner.
- `hermes-agent` → automation-linked communications; token may need repair if refresh fails.

## Read-only audit workflow

1. Load `google-workspace` first.
2. Read profile inventory from `/opt/data/google_profiles` and ignore old backup profiles unless needed.
3. For each active profile, verify Gmail identity with `users.getProfile`.
4. Count true Inbox using `messages.list(labelIds=['INBOX'])` paging; do not use broad `messagesTotal` as Inbox count.
5. Pull unread and recent Inbox samples with metadata/snippets first:
   - `is:unread newer_than:30d`
   - `newer_than:7d`
   - Apply `labelIds=['INBOX']` where possible.
6. Classify messages into:
   - urgent/action-needed,
   - money/account/security,
   - work/business/vendor,
   - Robinhood trade/order/account routing candidates (`Hermes/Finance/Robinhood`, useful for Agentic trading MCP context),
   - Zoom meeting-assets archive candidates (`Hermes/Archive/Zoom Meeting Assets`),
   - content/newsletter source,
   - duplicate newsletter/source copies on `affan.fareed@gmail.com` when the same sender exists in `fareed320@gmail.com`,
   - personal-info holds such as Grammarly Insights,
   - shopping/subscriptions,
   - junk/low-priority,
   - needs user review.
7. Only fetch full bodies for messages that need deeper discussion or where snippets are insufficient.
8. Write a local non-secret audit JSON under `/opt/data/HeRmEz/projects/_ops/` when useful.
9. Report concise account-by-account bullets in Discord, not big tables.

## Discussion style

- Start with what requires the user's attention.
- Separate actual account/security/money emails from newsletters.
- For newsletters, suggest possible video/topic use only; do not delete unless a verified upload happened or user approves.
- For suspected junk, say why it looks low-priority and ask before cleanup unless user has explicitly pre-approved that exact junk scope.
- Offer next actions: reply draft, calendar task, cleanup proposal, video topic, or ignore.
- When the user agrees to a proposed newsletter/video cleanup path, follow `references/email-discussion-to-newsletter-pipeline-handoff.md`: upload first, verify YouTube IDs, keep source cleanup bounded to newsletter pipeline rules, and report read-only Gmail cleanup failures separately from successful uploads.

## Answering "did you clean up my emails?"

When the user asks whether cleanup happened, do not rely on memory or assume from cron names. Reconstruct the status from durable evidence:

1. Search recent sessions/cron transcripts for cleanup, trash/delete, verified upload IDs, and email-sorting reports.
2. Inspect the relevant email cron/job definitions or last-run status when available, especially newsletter/video backlog jobs and the email sorting agent.
3. If there is a safe read-only or bounded no-agent script that only performs the established sorting/labeling workflow, rerun or dry-run it to get current auth/status signals; do not run broad destructive cleanup without explicit approval.
4. Report in three buckets:
   - **verified source/newsletter cleanup**: source emails trashed only after a confirmed YouTube `video_id`;
   - **sorting/labeling**: messages moved out of Inbox into Hermes labels, not deleted;
   - **broad inbox/junk cleanup**: only claim it happened if there is explicit evidence.
5. Call out auth-blocked profiles by profile/email only, with no secrets, and distinguish them from healthy profiles.

Keep the answer concise and direct: "yes for X, partially for Y, no evidence for Z" is better than a long audit dump.

## Verification checklist

- [ ] Gmail profiles checked live.
- [ ] Inbox counts are true INBOX counts.
- [ ] Important messages surfaced first.
- [ ] No destructive action taken without approval.
- [ ] Any auth failures reported with profile name only, no secrets.
