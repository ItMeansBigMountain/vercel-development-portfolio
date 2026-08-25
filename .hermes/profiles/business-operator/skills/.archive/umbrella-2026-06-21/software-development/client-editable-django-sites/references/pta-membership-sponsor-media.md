# PTA Membership CTA + Sponsor Media Pattern

Use this note when refining a client-editable PTA/nonprofit Django site after launch feedback.

## $15 Join PTA / Membership Flow

Pattern that worked well:

- Add a dedicated `join-pta/` page rather than burying membership under fundraising.
- Add a high-visibility nav CTA like `Join PTA $15`, especially top-right on desktop and full-width inside the mobile menu.
- Store membership fee and payment URL in `SiteSettings` or a similar singleton model:
  - `membership_fee = DecimalField(default=15.00)`
  - `membership_payment_link = URLField(blank=True)`
- Use Stripe Payment Links first; do not build custom checkout unless needed.
- If no payment link is configured, render a disabled/soft CTA such as `Payment link coming soon` instead of a broken checkout link.
- Copy should reduce intimidation: membership is low-pressure belonging; volunteering is optional and secondary.

Testing checklist:

- Nav contains `Join PTA $15`.
- `/join-pta/` returns 200.
- Page renders `$15` and the configured payment link.
- Payment link is editable in admin/site settings, not hard-coded.

## Sponsor Logo Media on Render Free

Issue pattern:

- Admin shows `Currently: sponsors/creativeice.png`, but public sponsor card shows no thumbnail or only alt text.
- This can mean the database has an `ImageField` filename but the binary file is missing from Render Free ephemeral storage, or the template never rendered the logo.

Robust prototype fix:

1. Add DB-backed fields to the model, e.g.:
   - `logo_data = BinaryField(blank=True, null=True, editable=False)`
   - `logo_content_type = CharField(max_length=80, blank=True, editable=False)`
   - `logo_filename = CharField(max_length=255, blank=True, editable=False)`
2. In `save()`, open the uploaded `ImageField`, copy bytes into `logo_data`, guess content type, then `seek(0)` before `super().save()`.
3. Add `logo_src` property:
   - prefer `data:{content_type};base64,{encoded}` when binary data exists
   - optionally fall back to `self.logo.url` for pre-existing records that still have accessible media files
   - otherwise return empty string
4. Template:
   - render `<img src="{{ sponsor.logo_src }}" ...>` when present
   - add an `onerror` fallback or adjacent placeholder so stale `/media/...` URLs do not display ugly alt text
   - render sponsor name/website even when the image is absent
5. Tell the client to re-upload once if the old file was already lost; after save, DB-backed rendering should survive redeploys.

Testing checklist:

- New upload renders `src="data:image/..."` and not `/media/sponsors/foo.png`.
- Existing filename-only record renders a safe fallback path or placeholder without losing sponsor name/link.
- Live fundraising page does not show broken alt-text-only sponsor cards.
