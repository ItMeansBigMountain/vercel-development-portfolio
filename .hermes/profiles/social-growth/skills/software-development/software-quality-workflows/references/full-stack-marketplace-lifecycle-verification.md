# Full-stack marketplace lifecycle verification

Use this reference for PostgreSQL/Stripe/Next.js workflows whose correctness spans database functions, scheduled workers, webhooks, and browser hydration.

## PostgreSQL functions: migration success is not runtime proof

PL/pgSQL may defer validation of statements inside a function until the function executes. A migration can succeed while runtime calls fail because of:

- references to renamed or nonexistent columns;
- status literals no longer accepted by current constraints;
- output-parameter names colliding with unqualified table columns;
- idempotency queries reselecting rows already allocated to another ledger record.

Add a live integration test that invokes every newly created function. Use controlled fixtures and cleanup. For state machines, exercise the complete path and invoke queue/watchdog functions twice.

Minimum assertions for a marketplace lifecycle:

1. Overdue fulfillment is selected once.
2. The listing is hidden with an explicit reason.
3. Refund amount matches merchandise plus proportional tax and the intended shipping policy.
4. Unpaid earnings are reversed.
5. A second watchdog run returns no work.
6. Delivery starts the return hold.
7. Mature earnings create one payout allocation.
8. A second payout-queue run creates nothing.

Qualify columns in PL/pgSQL whenever output parameters or local variables have common names such as `order_id`, `status`, `id`, or `payout_id`.

## Browser QA: rendered HTML is not proof of hydration

A Next.js page can look correct and expose a complete accessibility tree while app-client chunks fail and no React event handlers attach. Verify at least one stateful interaction:

- open a product dialog;
- cast a vote and observe `aria-pressed` change;
- add an exact variant to a persistent cart;
- reload and verify cart state remains.

For focused diagnosis, capture `pageerror`, `console`, `requestfailed`, and non-2xx chunk responses. Inspect a control for React fiber/props markers only as a diagnostic, not as a product assertion.

### Next.js development-origin symptom

If browser script requests to `/_next/static/chunks/*` return 403 while plain curl/fetch returns 200, reproduce with the browser's `Origin`, `Referer`, and `Sec-Fetch-*` headers. Next development CSRF protection may require a narrow `allowedDevOrigins` hostname allowlist. Keep it limited to local development hosts; do not loosen production CORS.

After correcting development origin handling, restart the dev server and prove:

- browser-style chunk request returns 200;
- React handlers attach;
- the focused interaction works;
- the full responsive E2E suite passes.

## Stable gate order

1. Apply migrations twice or use an idempotent migration runner.
2. Run unit tests.
3. Run live database lifecycle tests.
4. Run lint and type checks.
5. Build production assets.
6. Run browser interactions at representative desktop/mobile widths.
7. Scan staged additions for credentials.
8. Commit/push/deploy only after every gate is green.
