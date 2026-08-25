---
name: client-editable-django-sites
description: Build dynamic, client-editable Django websites with admin-managed content, forms, deployment, domains, and payment links.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [django, cms, admin, websites, render, stripe, client-sites, forms]
    related_skills: [claude-design, test-driven-development, github-pr-workflow]
---

# Client-Editable Django Sites

Use this skill when a user wants a polished website that non-technical clients can update through an admin panel, especially when a static mockup must become a live site with recurring updates, forms, newsletters, events, resources, fundraising, or custom domains.

Typical examples:
- PTA, school, nonprofit, church, club, or community organization sites
- small-business sites where staff need weekly updates
- converting a static HTML/GitHub Pages mockup into Django
- adding `/admin/`, editable newsletters/events/resources, form capture, or Stripe donations
- deploying a Django site to Render/Railway/Fly.io/PythonAnywhere and later attaching a custom domain

## Core Approach

1. **Separate visual design from content operations**
   - Preserve the visual system from the mockup: colors, typography, assets, nav order, card treatments, spacing, mascot/brand cues.
   - Convert recurring content into Django models instead of hard-coding it.
   - Keep client-facing pages simple, fast, and mobile-first.

2. **Model what the client updates**
   - Newsletters/announcements: title, issue date, summary/body, flyer/image/file, external link, published flag.
   - Events: title, start/end date, description, location, flyer, CTA link, category, featured/published flags. For parent-facing calendars with many items, group events automatically by month/year and use accordion sections so the current month or next upcoming month opens first while past months stay collapsed.
   - Volunteer opportunities: title, committee/category, description, time commitment, signup CTA, active flag.
   - Volunteer interest submissions: parent/guardian name, email, phone, interests, message, created_at, reviewed flag. Surface unreviewed counts in admin (dashboard banner and/or changelist title/filter) so non-technical clients immediately know what needs follow-up. If an opportunity dropdown is optional, remove Django's `---------` placeholder (`empty_label = None`) and hide the field entirely when there are no active opportunities.
   - Shareable announcements/flyers: title, body, image/file, CTA URL, publish/expire dates, published flag, and dedicated detail/print URLs with QR codes for offline distribution.
   - Fundraising/donations: campaign title, goal amount, raised amount or manual display amount, Stripe Payment Link, sponsor highlights, published flag.
   - Membership/join pages: flat fee, admin-editable Stripe Payment Link, prominent nav CTA, and low-pressure belonging copy so joining feels easier than volunteering.
   - Resources: label, category, URL/file, description, sort order, published flag.
   - Site settings: school name, PTA email, address, social links, hero copy, global Stripe link, footer text.

3. **Use Django Admin as the first CMS**
   - Register all editable models with `list_display`, `list_filter`, `search_fields`, and useful ordering.
   - Add `prepopulated_fields` for slugs where appropriate.
   - Prefer boolean `published`/`active` fields so the client can draft content safely.
   - Use readable `help_text` for fields the client will edit.
   - Keep destructive or technical fields out of the default workflow.

4. **Use Stripe Payment Links before custom checkout**
   - For simple nonprofit fundraising, store a Stripe Payment Link in the admin and send Donate buttons there.
   - This avoids PCI scope and reduces maintenance.
   - Only build direct Stripe Checkout/session logic if the user explicitly needs custom donation amounts, webhooks, receipts, or donor records inside Django.

5. **Deploy where Django can run**
   - GitHub Pages is static-only; use it only for static previews.
   - For Django admin and database-backed content, deploy to a Python host such as Render, Railway, Fly.io, or PythonAnywhere.
   - Render pattern: web service + PostgreSQL + `render.yaml` + env vars + `gunicorn` + WhiteNoise for static files.

## Recommended File/Project Structure

```text
project-root/
  manage.py
  requirements.txt or pyproject.toml
  render.yaml
  README.md
  docs/
    client-admin-guide.md
    deployment-guide.md
  appname/
    settings.py
    urls.py
    wsgi.py
  cmsapp/
    admin.py
    forms.py
    models.py
    tests.py
    urls.py
    views.py
    management/commands/seed_initial_content.py
  templates/
    base.html
    home.html
    newsletter.html
    events.html
    volunteer.html
    resources.html
    fundraising.html
    about_contact.html
  static/
    css/site.css
    js/site.js
    images/
```

## Implementation Workflow

1. **Read the brief and assets**
   - Identify required pages, nav order, content update frequency, payment needs, hosting constraints, and domain plan.
   - Inspect existing mockups/assets if the work continues from a design artifact.

2. **Write or update a short migration plan**
   - Static vs dynamic hosting implications.
   - Model list and who edits each model.
   - Deployment target and custom domain steps.
   - Payment strategy: Stripe Payment Link vs custom Stripe integration.

3. **Create tests first for required behavior**
   - Navigation order and page existence.
   - Newest-first newsletter/event sorting, plus month/year accordion grouping for event calendars when the audience needs cognitive ease.
   - Public wording avoids confusing CMS jargon (e.g. prefer `Newsletter` / `Read newsletter` over `Issue` when the audience may read issue as a problem).
   - Membership/join CTA is prominent in navigation, join page renders the flat fee, and an admin-editable Payment Link is used instead of hard-coded checkout URLs.
   - Form submissions persist in the database.
   - Volunteer opportunity selects do not show Django's default `---------` placeholder.
   - Share/print announcement pages render QR codes and return 200.
   - Fundraising page renders a Stripe link when configured.
   - Draft/unpublished content is hidden from public pages.

4. **Implement models, admin, forms, views, templates**
   - Keep views boring and explicit.
   - Use `get_queryset()` or manager filters for `published=True` content.
   - Use `messages.success()` or a success page after form submissions.
   - Keep templates modular only when repetition justifies it.

5. **Seed realistic starter content**
   - Create a management command with plausible events, newsletters, volunteer opportunities, resources, and fundraising placeholders.
   - Do not hard-code private credentials or real Stripe secret keys.

6. **Verify locally**
   - Run migrations.
   - Run the test suite.
   - Start the dev server on an available port.
   - Fetch all public endpoints and `/admin/` over HTTP to verify they return expected statuses.

7. **Document client and deployment workflows**
   - Client admin guide: how to log in, add newsletter/events/resources, review volunteer submissions, update fundraising link/progress.
   - Deployment/README guide: explain the operational chain in plain language (`AI/developer → GitHub → Render → live Django website → /admin/ content updates`), include live/admin/dashboard URLs, list required accounts (GitHub, Render, Stripe, domain registrar), and distinguish code updates from admin content updates. See `references/client-ops-readme-pattern.md`.
   - Deployment guide: Render setup, env vars, database, static files, createsuperuser, custom domain DNS.

8. **Commit and push**
   - Include tests, docs, deployment config, and README updates.
   - Mention that GitHub Pages can remain a static preview but cannot run Django.

## Mobile, Sharing, and Print UX Patterns

For parent/community sites, optimize for phone-first behavior and offline sharing:

- Treat the homepage as the conversion surface: urgent announcements, volunteer CTAs, event CTAs, and donation/share actions should be visible before archival content.
- Use mobile-app-like form controls: 56px+ tap targets, full-width primary submit buttons, rounded inputs, strong focus states, and no meaningless placeholder options.
- For announcement/flyer content, provide a web detail page plus a print page. The print page should include the flyer/image, short text, QR code, and `@media print` CSS that hides nav/footer/actions.
- For newsletter/flyer detail pages on mobile, stack content as image first then text/actions (`[image]` then `[text]`) rather than side-by-side columns; flyer images are often the primary reading surface.
- For event calendars, reduce overwhelm by grouping events into month/year accordions. Open the current month by default; if the current month has no events, open the next upcoming month; keep past months collapsed but available. Use large tap targets, event counts, status labels (`This month`, `Upcoming`, `Past`), and one-open-panel behavior on mobile.
- Use subtle child-friendly motion (reveal-on-scroll, gentle icon bob, CTA shine, tap feedback) while respecting `prefers-reduced-motion`. Keep animation polished and restrained so the site feels like a serious organization, not a toy.
- Use trust colors and hierarchy deliberately: navy for official/trustworthy primary actions, gold for warm/high-attention secondary actions, soft blue/white for safe breathing space.
- For PTA membership, make the join path visible as a top-right/top-nav CTA (e.g. `Join PTA $15`) and frame it as low-pressure belonging: joining is the easiest first step, volunteering can be secondary.

## Render Deployment Checklist

- `requirements.txt` includes `Django`, `gunicorn`, `whitenoise`, `dj-database-url`, and PostgreSQL adapter (`psycopg[binary]` or `psycopg2-binary`).
- `settings.py` reads `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `DATABASE_URL` with a local SQLite fallback for development/tests.
- WhiteNoise configured for static files:
  - `whitenoise.middleware.WhiteNoiseMiddleware`
  - `STATIC_ROOT`
  - `python manage.py collectstatic --noinput`
- Prefer a Render Blueprint (`render.yaml`) when the user wants automatic deploys from GitHub:
  - use a plain build command that works on Render defaults, e.g. `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` unless the repo explicitly installs/configures `uv` first
  - set `startCommand: "gunicorn projectname.wsgi:application"`
  - include a managed PostgreSQL database under `databases:`
  - wire `DATABASE_URL` via `fromDatabase: { name: <db-name>, property: connectionString }`
  - set `PYTHON_VERSION` when the project has been verified against a specific Python version
- In Render dashboard, deploy via **New + → Blueprint → select GitHub repo → Apply** so pushes to `main` can auto-deploy.
- After deploy:
  - create a superuser/admin account:
- After deploy:
  - create superuser/admin account from Render Shell with `python manage.py createsuperuser` when Shell is available
  - on hosts/plans without Shell access (e.g. Render Free), add a management command such as `create_admin_from_env` and run it from the build command after migrations; read `ADMIN_USERNAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD` from host environment variables, then tell the user to remove `ADMIN_PASSWORD` after login succeeds
  - seed initial content if appropriate
  - verify public pages, uploaded media URLs, and `/admin/` on the `.onrender.com`/staging URL before handling Stripe/domain work
  - attach custom domain and configure DNS/CNAME or A records from host instructions

## Domain Attachment Pattern

1. Deploy the dynamic site first on the host-provided URL.
2. In the hosting dashboard, add the custom domain.
3. Copy the exact DNS records the host provides.
4. In the registrar DNS settings, add/update those records.
5. Wait for DNS propagation and HTTPS certificate issuance.
6. Add the custom domain to `ALLOWED_HOSTS`.
7. Verify both apex/root and `www` behavior, including redirects if configured.

Do not guess registrar-specific DNS values. Use the values provided by the chosen host.

## Testing Patterns

Django `TestCase` examples to include early:

```python
class PublicSiteBehaviorTests(TestCase):
    def test_nav_order(self):
        response = self.client.get("/")
        html = response.content.decode()
        labels = ["Home", "Newsletter", "Events", "Volunteer", "Resources", "Fundraising", "About & Contact"]
        positions = [html.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))

    def test_newsletters_newest_first(self):
        Newsletter.objects.create(title="Older", issue_date="2026-01-01", published=True)
        Newsletter.objects.create(title="Newer", issue_date="2026-02-01", published=True)
        response = self.client.get("/newsletter/")
        html = response.content.decode()
        self.assertLess(html.index("Newer"), html.index("Older"))

    def test_volunteer_interest_form_captures_submission(self):
        response = self.client.post("/volunteer/", {
            "name": "Jordan Parent",
            "email": "jordan@example.com",
            "interests": "Book Fair, STEM Night",
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(VolunteerInterest.objects.filter(email="jordan@example.com").exists())
```

## Client Admin Guide Must Cover

- Admin URL and login expectations.
- How to add/edit/publish newsletters.
- How to add events and flyers.
- How to update volunteer opportunities and review submitted interests.
- How to update resources/links.
- How to update fundraising progress and Stripe Payment Link.
- Image/file size guidance.
- A non-technical warning: unpublished/draft items may not appear publicly until marked published.

## Pitfalls

- Do not promise GitHub Pages can host Django admin. It cannot; it can only host the static preview/build output.
- Do not assume production uploaded media works just because admin uploads succeed. With `DEBUG=False`, Django does not automatically serve `MEDIA_URL`; for a quick free-hosting prototype you can add an explicit media route, but if a rendered `/media/...` image shows only alt text and returns 404, the file has likely disappeared from ephemeral storage and routing cannot recover it. Review **all public customer/admin-uploaded image surfaces** (announcements, newsletter cover images, sponsor logos, event flyers if rendered as images, site logos/mascots) rather than fixing only the first broken page. For small prototype images, store bytes in the database as a temporary fallback and require one re-upload; for durable client sites use persistent object storage (Cloudinary/S3/Supabase/etc.) or host persistent disks because free ephemeral files may disappear on redeploy/restart.
- When adding DB-backed image fallbacks after data already exists, handle both states: existing records may only have a filename (`sponsors/foo.png`) and no binary data until re-saved/re-uploaded, while newly saved records should render `data:image/...`; templates should avoid broken alt-text by using a visible fallback or `onerror` placeholder for stale file URLs.
- Do not bury time-sensitive announcements/flyers inside a newsletter archive unless the user explicitly wants that. Weekly PTA/client announcements usually belong on the homepage first, with Newsletter reserved for actual newsletter issues.
- Do not build custom card processing when Stripe Payment Links satisfy the requirement.
- Do not leave high-churn content hard-coded in templates; if the client updates it weekly, it belongs in the database/admin.
- Do not leave Django's default `---------` option visible in public select fields; set `empty_label = None`, choose a real initial value when available, or hide the field when no real choices exist.
- Do not call public newsletter entries `issues` if the audience may interpret that as problems; use `Newsletter`, `Update`, or `Post` in user-facing labels while keeping internal model names if changing them is not worth a migration.
- Do not render flyer/newsletter detail layouts side-by-side on mobile; stack the image above the text so phone users can read and screenshot/share it easily.
- Do not make QR/print sharing an afterthought for PTA/school sites; flyers are commonly shared offline, so add printable pages and QR codes for announcements when the client will print or distribute files.
- Do not show long flat event lists when parents need to know what is coming soon. Use predictable month/year grouping and collapse old months; otherwise the Events page becomes cognitively overwhelming on mobile.
- Do not bury mobile parents under long navigation or tiny tap targets; maintain large buttons and clear page hierarchy.
- Do not store Stripe secret keys, registrar credentials, or admin passwords in the repo.
- Do not skip deployment docs; non-technical client sites need operational instructions as much as code.
- Do not mark the project complete until tests pass and public endpoints have been fetched locally or in staging.

## Support Files

- `templates/create_admin_from_env.py`: copy into `<app>/management/commands/create_admin_from_env.py` when a host plan lacks shell access; invoke after migrations with `ADMIN_USERNAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD` env vars, then remove the password env var after first successful login.

## Reference Notes

- See `references/pta-django-render-stripe.md` for a condensed session pattern converting a PTA static site into a Django admin-backed Render deployment with Stripe Payment Links.
- See `references/render-free-django-admin-media.md` for the Render Free workaround: create admin users from env vars during build, production uploaded-media caveats, and admin unreviewed-count UX.
- See `references/mobile-pta-ux-print-sharing.md` for mobile-first PTA UX, removing default form placeholders, QR/print flyer pages, newsletter wording, and child-friendly but professional motion.
- See `references/pta-membership-sponsor-media.md` for the Join PTA flat-fee Payment Link pattern and sponsor-logo DB-backed media fallback for Render Free.
- See `references/monthly-event-accordions.md` for the month/year event accordion pattern that opens the current month, opens the next future month when needed, and collapses past months for mobile cognitive ease.
