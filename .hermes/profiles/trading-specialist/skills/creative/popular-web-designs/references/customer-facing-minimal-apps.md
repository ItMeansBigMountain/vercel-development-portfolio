# Customer-facing minimal app redesign notes

Use this reference when a user says a web app feels cluttered, jumbled, too data-heavy, or too developer-facing.

## Pattern

1. **Start with the user's primary intent**
   - Put one clear action at the top, usually a universal search bar or a single CTA.
   - Avoid dashboards full of stats, filters, and panels on the first screen unless the product is explicitly an analytics tool.

2. **Use progressive disclosure**
   - First screen: search + primary object list.
   - Object page: focused list of child items.
   - Detail page: only what the customer needs to act.
   - Hide filters, metadata, source notes, API readiness, implementation details, and admin/developer language from public customer views.

3. **Reduce data density**
   - Show fewer fields per card: title, image, one short supporting line.
   - Move full instructions/details behind a click.
   - Prefer plain language over taxonomy-heavy copy.

4. **Make media reliable**
   - If external photo providers or hotlinked assets fail in browser verification, replace them with bundled/static/generated placeholder illustrations rather than shipping broken image cards.
   - Every card/detail media element needs alt text and a graceful visual fallback.

5. **Video enrichment without blocking**
   - When exact licensed videos are not available, provide a customer-facing YouTube search link using the item title + category/context + "demonstration".
   - Label it as "Watch a demonstration" instead of exposing data-source uncertainty.

## Verification checklist

- Landing page has one obvious primary action.
- No customer-visible words like API, Vercel, seed data, developer, source panel, credentials, build, import hook, implementation details, or agent-to-user phrasing such as “fake data”, “real data”, “development tweak”, “write endpoints”, or “this is from me to you”. Treat those as internal requirements and translate them into polished product copy.
- If the user says tabs are too cramped or asks for tabs to become pages, make real routes/pages with progressive disclosure rather than a single long scroller; verify direct route loads, not only client-side navigation.
- Search works globally across primary objects and child content.
- Click path is obvious: landing → object → item detail.
- Browser visual check confirms no broken images, no crowded panels, no awkward developer copy.
