# Serverless Commerce Backend Delivery Pattern

Use this reference when converting a polished storefront prototype into a real, key-ready commerce operation on Next.js/Vercel.

## Delivery order

1. Inspect the existing catalog, checkout, deployment link, environment example, tests, and git boundary.
2. Define pure commerce rules first: variants/SKUs, integer-cent prices, stock, cart quoting, order transitions, social URL normalization.
3. Add a repository contract and a keyless in-process adapter for unit tests/local fallback.
4. Provision durable Postgres through the hosting provider when authorized. Prefer provider-managed environment injection so the user does not need to shuttle database credentials.
5. Check in idempotent SQL migrations and a deterministic migration runner; execute them against the real database and inspect resulting tables.
6. Seed products, variants, SKUs, weights, and stock. Do **not** seed fictional creator endorsements or engagement into legitimate evidence tables.
7. Build signed anonymous carts whose browser payload contains only variant IDs and quantities. Rebuild every quote server-side.
8. Add multi-item Stripe Checkout configuration, then a signed webhook before considering payment complete.
9. Finalize paid orders in one database transaction/function: lock cart and inventory, validate totals, deduplicate the event, snapshot order lines, decrement stock, write movements/audit events, and convert the cart.
10. Add passwordless admin invitations with hashed one-time tokens and hashed revocable sessions; never persist or log raw bearer tokens.
11. Implement admin catalog/inventory/social/order/fulfillment operations with role checks and audit logs.
12. Add provider adapters, policies, monitoring hooks, end-to-end tests, deploy, and verify production.

## PostgreSQL migration runner pattern

HTTP Postgres drivers commonly reject a whole migration file containing multiple prepared statements. Run ordinary schema files statement-by-statement. For PL/pgSQL functions, semicolons occur inside the function body, so use an explicit delimiter such as:

```sql
CREATE OR REPLACE FUNCTION ... $$
BEGIN
  ...;
END $$;
-- statement-breakpoint
INSERT INTO schema_migrations(version) VALUES ('002') ON CONFLICT DO NOTHING;
```

The runner should process migration files in lexical order and split delimiter-aware files on `-- statement-breakpoint`; naive semicolon splitting breaks PL/pgSQL.

### Repeat-safe migration discipline

Run the complete migration set at least twice against the same database before deployment. A migration log table alone does not make a runner safe if the runner still executes every file.

- Prefer inherently idempotent DDL (`CREATE TABLE IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS`, conflict-safe version inserts).
- Column renames are not inherently repeatable. Wrap compatibility renames in a catalog check:

```sql
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'admin_sessions' AND column_name = 'legacy_name'
  ) THEN
    ALTER TABLE admin_sessions RENAME COLUMN legacy_name TO current_name;
  END IF;
END $$;
-- statement-breakpoint
```

- A file containing `DO $$`, functions, or other semicolon-bearing blocks must opt into delimiter-aware parsing with explicit `-- statement-breakpoint` markers after each top-level statement.
- Verification is not merely “migration command exited successfully”: query `schema_migrations` and inspect the expected table/column set after the second run.

## Conditional-write atomicity

For admin mutations, do not run a transaction containing an `UPDATE ... RETURNING`, followed by unconditional movement/audit inserts, and then throw in application code when the update returned no rows. The transaction may already have committed the side records.

Use one data-modifying CTE whose dependent writes select from the successful change:

```sql
WITH changed AS (
  UPDATE product_variants
  SET inventory = inventory + $2
  WHERE id = $1 AND inventory + $2 >= reserved
  RETURNING id
), movement AS (
  INSERT INTO inventory_movements (...)
  SELECT ... FROM changed
), audit AS (
  INSERT INTO audit_events (...)
  SELECT ... FROM changed
)
SELECT * FROM changed;
```

If `changed` is empty, inventory, movement, publication flags, and audit records all remain untouched. Apply this pattern to inventory adjustments, moderation/publication, support-state changes, receiving, and similar conditional workflows.

## Atomic webhook pattern

Avoid a loose sequence of API-side writes. Put finalization in a Postgres function or transaction that:

- returns the existing order for a duplicate Checkout Session/event;
- locks the active cart and all referenced variants;
- checks every line is active and sufficiently stocked;
- recomputes subtotal from stored integer-cent prices;
- compares Stripe total to server subtotal + shipping + tax;
- inserts the verified payment event;
- creates order and immutable order-item snapshots;
- writes inventory movements and decrements inventory once;
- marks the cart converted;
- writes an audit event;
- raises on mismatch so the entire operation rolls back and Stripe can retry.

Test this against the real database by delivering the same synthetic event twice and proving one order plus one stock decrement.

## Passwordless administrator pattern

A no-extra-provider-key approach:

- `admin_invites`: admin ID, SHA-256 token hash, expiry, consumed timestamp.
- `admin_sessions`: admin ID, SHA-256 session hash, expiry, last-seen timestamp.
- Invitation exchange must lock and consume the invitation atomically while creating the session.
- Cookie: `HttpOnly`, `Secure` in production, `SameSite=Strict`, bounded lifetime, and a path that covers both the UI and mutation APIs. If the UI is `/admin` but mutations are `/api/admin/*`, `Path=/admin` will silently exclude those API requests; use `/` (with a distinct cookie name) or colocate APIs under the scoped path.
- Browser-test an authenticated admin mutation, not only page rendering or server-side session resolution; this catches cookie-path mismatches.
- Roles should map to explicit capabilities (catalog, social moderation, inventory, fulfillment, refunds, support, admin management).
- Deliver the one-time link through an already authorized communication channel without printing/logging its raw token.

## Social evidence legitimacy

Keep product truth and social evidence separate. Ingest only approved API data or rights-confirmed submitted URLs. Store canonical URL, platform ID, creator attribution, permission status, moderation status, and timestamped engagement snapshots. AI similarity may suggest product correlations but does not prove a creator wore or endorsed the item. Require review before publishing.

When replacing a prototype’s seeded social proof, removing rows from the legitimate database is insufficient: search the entire public component tree for static creator handles, captions, engagement totals, post counts, “heat” functions, hero cards, modal copy, and explanatory marketing sections. Public claims must derive only from the approved-evidence query. The truthful empty state is “No approved social evidence yet,” while independent first-party community votes must be labeled separately from platform engagement.

Canonicalize submitted URLs before deduplication: validate an allowlisted host, remove tracking query parameters, normalize `www`, and trim irrelevant trailing slashes while preserving case-sensitive platform IDs. Approval should atomically set moderation state, publish product associations, and write audit history only when the rights-confirmed source row exists.

Optional provider credentials must not block the core operation. Administrator-submitted URLs, explicit rights basis, moderation, manual timestamped snapshots with source labels, and takedown handling should work without social API keys; official API adapters can enrich those records later without introducing a scraping fallback.

## Operational support and owner access

A commerce build is not operational merely because Checkout works. Include database-backed support requests, a least-privilege `support.write` capability, an admin inbox with status transitions, policy/support navigation, and privacy-minimized customer order status. A Stripe success redirect should say payment/order finalization may still be processing because webhook state—not the redirect—establishes payment truth.

For passwordless owner bootstrap, generate the raw invite token once, store only its hash, and deliver the raw link through an already authorized private communication channel. Do not print it in logs, summaries, commits, or public deployment output.

## Verification gates

- Unit tests for commerce rules, payload validation, role capabilities, event classification, and Stripe configuration.
- Live Postgres integration tests for cart persistence, webhook idempotency/stock, invitation replay rejection, and session revocation.
- Production build and lint.
- Runtime API probes with a cookie jar.
- Browser tests for add/update/remove/reload cart flows and mobile layouts.
- Without Stripe credentials, Checkout must return a truthful safe error and preserve the cart.
- Do not call the project complete until admin CRUD, fulfillment/returns, social moderation, policies, full QA, push, deploy, migration, and live verification are done.
