# PTA Django + Render + Stripe Payment Links Pattern

Condensed pattern from a Cox Elementary PTA website migration.

## Situation

A user had a polished, mobile-friendly static PTA mockup with navy/gold school branding, eagle mascot assets, and pages such as Home, Events, and Volunteer. The client needed weekly updates without editing code, a standalone newsletter page, dynamic events/volunteer content, a fundraising page using Stripe, and a custom domain later.

## Durable Lessons

- Treat recurring PTA content as admin-managed database records, not static HTML.
- GitHub Pages can remain an old/static preview, but it cannot run Django or `/admin/`.
- Render is a practical free/low-cost hosting route for a Django + PostgreSQL app; include `render.yaml` and deployment docs.
- Stripe Payment Links are the right first step for simple PTA donations because they keep card handling out of Django.
- Preserve the client-approved visual system while changing the architecture; do not redesign from scratch unless asked.

## Pages/Nav Pattern

User-requested order:

```text
Home
Newsletter
Events
Volunteer
Resources
Fundraising
About & Contact
```

Routes:

```text
/
/newsletter/
/events/
/volunteer/
/resources/
/fundraising/
/about-contact/
/admin/
```

## Model Pattern

Useful initial models:

- `SiteSettings`: school/PTA name, hero copy, email, phone, address, social links, global Stripe link.
- `Newsletter`: title, issue_date, summary/body, flyer/file/image, external_url, published; order newest first.
- `Event`: title, date/start/end, category, location, description, flyer image/file, cta_url, featured, published.
- `VolunteerOpportunity`: title, committee/category, time commitment, description, cta_url, active.
- `VolunteerInterest`: name, email, phone, interests, message, created_at, reviewed.
- `FundraisingCampaign` or donation settings: title, goal, current amount, impact copy, Stripe Payment Link, sponsor fields, active.
- `Resource`: title, category, URL/file, description, sort order, published.

## Test Pattern

Write tests before implementation for:

1. Public pages return 200.
2. Navbar labels appear in the requested order.
3. Newsletter page renders newest issue before older issue.
4. Volunteer form `POST` persists a lead/submission for admin review.
5. Fundraising page renders the configured Stripe Payment Link.
6. Draft/unpublished content does not appear publicly.

## Deployment/Docs Pattern

Add docs such as:

- `docs/django-admin-migration-plan.md`: architecture, hosting choice, data models, payment strategy, domain plan.
- `docs/client-admin-guide.md`: non-technical guide for updating newsletters, events, volunteer opportunities, resources, and Stripe links.
- `render.yaml`: web service, build/start commands, DB env wiring.
- README section clarifying static preview vs dynamic Django deployment.

## Verification Pattern

- Install dependencies in a virtual environment.
- Run `python manage.py makemigrations` and `python manage.py migrate`.
- Run Django tests.
- Seed initial content with a management command.
- Start local server on an available port.
- Fetch all public endpoints and `/admin/` via HTTP before finalizing.

## Final Messaging Pattern

Be clear that:

- The dynamic admin site is in the repo and ready for Django hosting.
- The old GitHub Pages URL is only a static preview unless separately rebuilt.
- Final launch needs domain/DNS access, Stripe Payment Link, and a decision about whose hosting account owns the deployment.
