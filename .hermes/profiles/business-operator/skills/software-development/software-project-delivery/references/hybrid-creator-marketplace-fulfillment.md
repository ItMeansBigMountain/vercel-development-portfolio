# Hybrid Creator Marketplace Fulfillment Pattern

Use this reference when one storefront sells both first-party inventory and creator/vendor dropship products, with creator-post media, manual review, customer protection, and Stripe Connect payouts.

## Model mixed orders per line

Do not put creator ownership, tracking deadlines, earnings, or refund state only on the whole order. One cart may contain Wornly inventory plus products from several creators. Snapshot seller identity and product/variant truth into immutable order items, then create one fulfillment record per order line.

Core ledgers:

- `creator_accounts`: identity, approval state, Stripe account, onboarding state.
- `creator_product_submissions`: proposed product/variant JSON, fee basis points, primary approved post, review notes/state.
- `order_item_fulfillments`: seller, model (`warehouse` or `creator_dropship`), tracking deadline, tracking/delivery/refund state.
- `creator_earnings`: gross item value, platform fee, creator net, hold/availability/status.
- `refund_requests` plus `refund_request_items`: one durable refund intent linked to exact failed lines.
- `creator_payouts` plus payout items: one transfer batch linked to exact earnings.

Use integer cents and basis points. Never recompute historic earnings from mutable current product settings.

## Rights-reviewed post media

Keep commercial product truth separate from social evidence. A creator should first submit:

- canonical allowlisted platform URL;
- creator attribution;
- explicit storefront-display rights and basis;
- HTTPS media URL or controlled storage object;
- accessible alt text and media provenance.

Moderate the post separately. Product approval must verify that every referenced post is rights-confirmed and approved. The server should copy the primary image URL and alt text from the approved post record into the product; do not trust an unrelated image URL in the product draft. Publish the product-post association atomically with product approval. Takedown or rights revocation must unpublish the association and provide a safe product-media fallback or hide the listing.

## 48-hour tracking watchdog

At payment-webhook finalization, create creator fulfillments with `tracking_deadline_at = paid_at + interval '48 hours'` and pending creator earnings in the same database transaction as the order.

The authenticated scheduled worker should:

1. Lock only `awaiting_tracking` lines past the deadline (`FOR UPDATE SKIP LOCKED` or an equivalent transactional function).
2. Mark those lines delinquent exactly once.
3. Hide only the affected creator products and record a delinquency reason/time.
4. Reverse unpaid earnings for those lines.
5. Group affected lines into durable refund requests per order.
6. Link every refund request to its exact fulfillment lines.
7. Submit Stripe refunds with a stable idempotency key derived from the refund-request ID.
8. Leave refund state `submitted` until a signature-verified Stripe webhook reports terminal success/failure.

Repeated worker runs must produce no duplicate refund requests, product transitions, or earnings reversals.

### Mixed-cart refund allocation

For a creator line that never shipped, refund its merchandise and proportional tax. Refund shipping only when every fulfillment line in the order failed. Compute the aggregate failed subtotal once per order before applying tax/shipping; do not add full shipping or full tax separately for every line.

Mark the whole order `refunded` only when every line is refunded. Otherwise retain the paid/partially fulfilled order and show line-level outcomes.

## Delivery holds and payouts

A practical separate-charges-and-transfers flow:

1. Stripe Checkout charges the customer on the platform.
2. Verified payment webhook creates line fulfillments and creator earnings.
3. Creator submits carrier, tracking number, and HTTPS tracking URL before deadline.
4. Delivery is confirmed by a trusted carrier webhook or an authorized operator—not by the creator alone.
5. Delivery starts a return-risk hold (for example, the disclosed 30-day return window).
6. An atomic database function promotes matured earnings and groups them into one payout per creator.
7. Stripe transfer uses an idempotency key based on the payout ID and metadata containing that ID.
8. API success marks the payout `submitted`; a verified `transfer.created` webhook marks it paid. A reversal moves allocated earnings to a reconciliation state, not back into a general unallocated pool.

Prevent concurrent payout workers with a transaction-scoped advisory lock or equivalent serialization. Payout-item uniqueness plus atomic status movement prevents one earning from entering two batches.

## Creator and admin portals

Use separate passwordless creator and admin invitations/sessions. Persist only SHA-256 token hashes; expose a raw invite link once through an authorized private channel.

If mutation APIs live under `/api/admin/*` and `/api/creator/*`, cookies scoped to `/admin` or `/creator` will not be sent to those API routes. Use a common path such as `/`, distinct cookie names, `HttpOnly`, `Secure` in production, `SameSite=Strict`, expiry, revocation, and server-side role/ownership checks.

Unified admin capabilities should cover creator invitations, account state, post/media rights review, product review, tracking exceptions, delivery confirmation, refunds, earnings, payouts, support, and audit history. The creator portal should show submissions, deadlines, tracking, Stripe onboarding, earnings, and payout history without exposing other sellers' records.

## Stripe event boundaries

At minimum classify and verify:

- `checkout.session.completed` / `checkout.session.expired`
- `refund.created` / `refund.updated`
- `charge.refunded` for externally initiated whole-order refunds
- `transfer.created` / `transfer.reversed`

Put durable ledger IDs in Stripe metadata. Payment, refund, and payout terminal state must come from signature-verified, idempotently recorded webhooks rather than redirects, cron attempts, or optimistic UI.

## Verification

- Unit-test deadline calculation, fee math, mixed-order tax/shipping allocation, URL/media validation, role capabilities, and webhook classification.
- Live-DB test duplicate payment events, one line fulfillment per order item, watchdog idempotency, exact listing hiding, exact refund-request lines, tracking-before-deadline, delivery hold, atomic payout grouping, and repeat payout runs.
- Browser-test unauthorized admin/creator APIs, one-time invitation exchange, submission/review, approved media on storefront, seller labels, tracking submission, exception controls, and mobile layouts.
- Run migrations twice against the same database; inspect constraints, functions, and expected tables.
- Without Stripe keys, keep review/tracking/refund intent ledgers functional while returning truthful unavailable states for charging, refund submission, Connect onboarding, and transfers.
