# Google Workspace multi-profile morning context

Session-derived pattern for morning reports that summarize the user's connected Google accounts.

## Canonical collector

Use the read-only pre-run script:

```bash
python /opt/data/scripts/google_morning_context.py
```

The morning report cron (`92f873723241`) is configured to run this script before the LLM report. It prints compact Markdown context for the agent to summarize.

## Profiles

Read all currently authorized profile-scoped OAuth tokens under `/opt/data/google_profiles/<profile>/google_token.json`:

- `hermes-agent` / `trapiistan@gmail.com` — Hermes, YouTube, operator account
- `personal-main` / `Affan.fareed@gmail.com` — personal main, read-focused
- `personal-secondary` / `fareed320@gmail.com` — personal secondary, read-focused
- `classicalechos` / `classicalechos@gmail.com` — Classical Echos / classy content lane
- `burner` / `laflametoast@gmail.com` — burner / low-stakes account

## What to include in the report

Summarize high-signal read-only items only:

- Gmail unread / important / starred / recent inbox signals
- Calendar events in the next 7 days
- Recent Drive movement that looks operationally useful
- Deadlines, renewals, receipts, opportunities, warnings, travel/housing/work items
- AI/content/tooling leads from burner or project accounts

Keep it skimmable. Consolidate by `Needs attention`, `Calendar`, `Ops/admin`, and `Interesting/useful` unless account-level grouping is clearer.

## Safety rules

- Never send, reply, archive, delete, label, share, create, or modify Google resources from the morning report run.
- Personal accounts stay read-first; sending from `personal-main` or `personal-secondary` requires explicit approval of the exact message.
- Hide raw secrets, token contents, recovery-code filenames, and credential-looking Drive filenames.
- The collector strips common invisible tracking characters from Gmail snippets so the report stays legible and avoids prompt-scanner noise.

## OAuth scope note

No reauth is needed for this report while using the existing Workspace scopes: Gmail read/send/modify, Calendar, Drive, Contacts readonly, Docs, and Sheets. Reauth is only needed when adding new scopes such as YouTube upload, Google Tasks, Meet, or private YouTube Analytics/Reporting.

## Verification pattern

After editing this flow, verify:

```bash
python /opt/data/scripts/google_morning_context.py >/tmp/google_morning_context_verify.md
```

Then verify the relevant cron prompt still passes Hermes' cron prompt-injection scanner before relying on the next scheduled run.
