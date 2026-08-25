# Social-Proof Commerce MVP Pattern

Use this pattern when building a marketplace that links products to social posts, creator attention, or aggregate engagement.

## Product model

Keep commercial truth and social evidence separate, then derive presentation metrics server-side:

- Product: stable ID, name, brand/vendor, category, price, currency, images, description, variants/sizes, inventory state.
- Social evidence: platform, platform post ID or canonical URL, creator identity, attribution, engagement snapshot, collection timestamp, product mapping, and media usage-right status.
- Derived metrics: cumulative engagement, post count, recency-weighted momentum, and a bounded display score (for example, 0–100).

Never label seeded/demo engagement as live or verified. A production score should be reproducible from stored snapshots and should disclose its basis in customer-friendly language.

## Sustainable ingestion

Prefer:

1. Platform-approved APIs for connected Business/Creator accounts and approved permissions.
2. Merchant or creator submission with ownership/usage-right confirmation.
3. Licensed campaign, affiliate, or product feeds.

Do not make unauthorized scraping the production architecture. Store attribution and usage rights alongside the post mapping, not in an unrelated spreadsheet.

## Stripe Checkout boundary

For an MVP, hosted Stripe Checkout is safer and faster than custom card UI.

- Browser submits only a stable product ID and selected variant.
- Server looks up trusted product/price data; never accept a client-supplied amount.
- Server creates the Checkout Session and records product/variant metadata.
- Use request origin as a safe default for success/cancel URLs; allow a canonical site URL environment override.
- If `STRIPE_SECRET_KEY` is absent, return an explicit configuration response rather than a fake successful purchase.
- Start in Stripe test mode and verify with test cards before live-mode credentials.
- Production fulfillment requires a verified Stripe webhook; the success-page redirect alone is not an order fulfillment signal.

## Customer-facing MVP

A useful first vertical slice includes:

- Visual product feed with one primary discovery action.
- Category/filter controls.
- Product details with social evidence, aggregate engagement, and clear attribution.
- Variant selection.
- Server-side checkout route.
- Success and cancellation paths.
- Responsive desktop/mobile behavior.

Keep API readiness, seed-data caveats, and deployment instructions in README/admin surfaces—not in the main shopping flow. A checkout configuration notice is appropriate only when the customer attempts checkout.

## Repository-boundary preflight

Scaffolding tools may detect a Git repository in a parent workspace and skip creating a child `.git` directory. Immediately after scaffolding:

1. Run `git rev-parse --show-toplevel` from the child.
2. Confirm it equals the intended standalone project directory.
3. If it resolves to the parent, unstage only the child path from the parent index if necessary, then initialize Git inside the child before any commit.
4. Never run broad `git add .` until the repository boundary is confirmed.

This is especially important under portfolio containers such as `projects/` with unrelated dirty work.

## Community voting and abuse controls

When products can be liked or disliked, treat voting as server-owned state rather than a cosmetic client counter:

- Accept only stable server-known product IDs and an enum-like vote (`like` or `dislike`).
- Give each anonymous browser one active vote per product; changing direction must decrement the previous side before incrementing the new side.
- Make repeated identical votes idempotent.
- Issue an `HttpOnly`, `Secure`, `SameSite=Lax` anonymous voter cookie and HMAC-sign it with a deployment secret. An unsigned random ID can be replaced manually to evade per-browser limits.
- Layer limits: a short per-product cooldown, a normal per-voter window, and a higher IP safety ceiling. Do not make the normal allowance IP-only because mobile carrier NATs and shared networks can punish unrelated shoppers.
- Return `429` with `Retry-After` and customer-friendly feedback near the control that triggered it.
- In serverless deployments, an in-memory `Map` is only an interactive preview: totals and limits reset on cold starts and diverge across instances. Disclose this and move production mutation/rate checks to shared Redis-compatible storage using an atomic transaction or script.
- Keep vote controls at least 44×44 CSS pixels, expose descriptive accessible names, and use `aria-pressed` for the selected direction.

Test vote accounting separately from HTTP behavior: first vote, repeated identical vote, direction reversal, product/voter isolation, window exhaustion, boundary reset, and signed-cookie tampering. Then probe the built API with a real cookie jar for `200`, immediate `429`, delayed reversal, and invalid-product `400`.

## iPhone and mobile viewport QA

For a requirement covering iPhone X/10 and newer, automate representative CSS viewport families rather than claiming responsiveness from one screenshot:

- 375×812 — iPhone X/XS/11 Pro
- 414×896 — XR/11/XS Max
- 390×844 — 12/13/14 family
- 393×852 — recent Pro family
- 430×932 — recent Pro Max family
- 320×568 — optional extra-narrow safety check

At each viewport assert: no horizontal overflow, primary headings render, vote targets are at least 44px, voting updates selected state, the product modal opens without page overflow, and checkout remains reachable. Use exact accessible-name matching when controls include both “Like …” and “Dislike …”; fuzzy matching can select both. Trigger or await lazy-loaded images before judging screenshot placeholders.

Keep unit and browser suites isolated. For Vitest, restrict `include` to unit-test paths when Playwright specs also end in `.spec.ts`; otherwise Vitest may import Playwright tests and fail before the E2E runner starts. Do not run `next build` while a `next start` process owns the same `.next` output—stop the tracked QA server first, rebuild, then start the verified build for E2E.

## Full-commerce expansion and standing delivery directives

When the user upgrades a storefront prototype into a complete operation, treat the request as one continuous delivery mandate rather than a sequence of status-report turns.

- Recover the prior plan from conversation history and inspect the live repository before writing code.
- Maintain a durable task list spanning domain model, persistence, cart, admin, checkout/webhooks, inventory, shipping/receiving/returns, social ingestion/moderation, policies, operations, QA, push, and deployment.
- Keep working through that list across continuation turns. A passing domain-layer slice is progress, not a stopping condition; do not conclude with a handoff-style summary while executable work remains and tools are available.
- Use vertical TDD slices: write a behavior test, observe the expected failure, implement the minimum domain/API/UI behavior, run the focused suite, then run regression gates.
- Preserve the existing storefront while replacing hardcoded catalog truth with server-owned products, variants, inventory, and normalized social evidence.
- Distinguish credential boundaries precisely. "Only Stripe remains" is true only when databases, storage, email, shipping, authentication, Redis, monitoring, and social providers have either been provisioned, have a fully functional keyless adapter, or are explicitly optional. Do not hide additional required keys behind placeholder abstractions.
- For external social platforms, complete URL normalization, submission, rights confirmation, moderation, provider interfaces, webhook/refresh contracts, truthful unavailable states, and tests without credentials. Platform OAuth approval and tokens may remain external blockers; arbitrary scraping is not an acceptable substitute.
- Do not declare the goal complete until the repository is pushed, the canonical deployment is live, and cart/admin/checkout-preview/social/shipping-policy/mobile flows have been exercised against production.

## Verification

- Lint, type-check, unit tests, and production build.
- Run the production server, not only development mode.
- Exercise filter/detail/variant/checkout and voting behavior.
- Verify configured and unconfigured checkout paths.
- Inspect browser console and image load state.
- Compare `document.documentElement.scrollWidth` with `clientWidth` to catch subtle horizontal overflow.
- Trigger lazy-loaded images by scrolling before declaring media complete.
- Visually inspect desktop and mobile/modal layouts.
- Run the representative mobile viewport matrix against the built app and again against the canonical production alias.
- After deployment, verify the canonical production alias rather than only a one-off deployment URL.
