# Email sorting expanded profile scan lessons (2026-07)

Use this when maintaining the Hermes Gmail sorting agent or reviewing the user's personal email.

## Current sorting agent coverage

The deterministic sorter should scan every readable Workspace Gmail profile the user has approved, not just the newsletter/source accounts. Current readable profiles for sorting/review are:

- `personal-main` / `affan.fareed@gmail.com`
- `personal-secondary` / `fareed320@gmail.com`
- `trapiistan` / `trapiistan@gmail.com`
- `classicalechos` / `classicalechos@gmail.com`
- `burner` / `laflametoast@gmail.com`

`hermes-agent` may exist in the local token tree, but do not add it unless live Gmail verification succeeds. If its token returns `invalid_grant`, report it as needing reauth rather than treating it as readable.

## Full scan workflow

- Run the deterministic sorter in apply mode only for already-approved routing classes.
- For review/audit tasks, use read-only Inbox metadata first: account email, Inbox count, top senders, subjects, and categories.
- Do not trash/archive/delete/unsubscribe during a review unless the user approves the exact batch/category.
- After applying sorter changes, run a dry-run verification to confirm remaining matches.

## Affan inbox review guidance

For `personal-main` / `affan.fareed@gmail.com`:

- Preserve finance/security/billing/account emails by default.
- Chase account alerts, HSA Bank, Experian, vehicle registration, tollway/government notices, housing/stay/access details, and Google Business Profile reports are keep/review unless the user explicitly approves cleanup.
- Grammarly Insights is personal information: label as `Hermes/Personal Info` and keep in Inbox for review.
- Likely cleanup candidates can be grouped for approval: myQ/Chamberlain promos, generic apartment marketing, promo/referral/cashback marketing, Glassdoor promos, Unsplash marketing, Yeezy updates, and stale travel passcode/password-reset messages.

## Reporting style

Use compact bullets, no tables in Discord unless the user specifically asks. Clearly state whether the scan was Inbox-only or All Mail, and whether any mutation was performed.