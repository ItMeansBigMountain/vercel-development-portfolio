# Client Website README / Ops Handoff Pattern

Use this reference when building or maintaining client-editable Django sites where the user wants the README to explain deployment and operations in non-technical terms.

## Goal

A README for a client/operator should explain both code workflow and admin workflow. It should make clear that code changes and content changes are different paths.

## Core Diagram

```text
AI / developer updates code
        ↓
GitHub stores the code
        ↓
Render watches GitHub main branch
        ↓
Render builds and deploys the Django website
        ↓
Website runs online with a Django Admin panel
        ↓
Client updates weekly content through /admin/
```

## Include Live Links

- Production website URL
- Admin panel URL (`/admin/`)
- Hosting dashboard URL (e.g. Render dashboard)
- GitHub repo URL

## Accounts / Services Needed

List the operational accounts clearly:

- GitHub — source code and deploy trigger
- Render or equivalent host — running website and database
- Stripe — Payment Links / donations
- Domain registrar — custom domain / DNS later
- Object storage account later if admin-uploaded media must be durable (Cloudinary/S3/Supabase/etc.)

## Code Update Workflow

```text
Change code locally or with AI → test → commit → push to GitHub main → Render auto-deploys → wait a few minutes → refresh live site
```

Explicitly say this is for design/feature/code changes, not weekly content edits.

## Content Update Workflow

```text
Log into /admin/ → add/edit/publish content → refresh public page
```

List the admin-managed areas: announcements, newsletters, events, volunteer opportunities, volunteer submissions, resources, fundraising campaigns, site settings.

## Free-Host Caveats

If using Render Free or another ephemeral filesystem host:

- Explain that uploaded files may disappear after redeploy/restart if stored only under `/media/`.
- Mention any temporary DB-backed image fallback currently implemented.
- Say broken pre-existing images must be re-uploaded once.
- Recommend persistent storage for production handoff.

## Keep Tone Non-Technical

Write as an operator guide, not an engineering deep dive. Use plain English and short numbered workflows. Avoid unexplained acronyms unless necessary.
