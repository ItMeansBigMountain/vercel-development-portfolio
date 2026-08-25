# Serverless Anonymous Voting and Rate-Limit Safety

Use for likes/dislikes, reactions, polls, or other anonymous write endpoints deployed on serverless platforms.

## Recommended model

- Keep one active vote per signed anonymous browser identity and resource.
- Sign the browser identity with an HMAC secret stored only in the deployment environment; reject tampered tokens using constant-time signature comparison.
- Use `HttpOnly`, `Secure`, `SameSite=Lax`, scoped cookies with an explicit lifetime.
- Validate resource IDs against a server-owned allowlist/catalog and accept only enumerated vote values.
- Layer limits:
  - short identity/resource cooldown;
  - normal per-identity allowance;
  - looser trusted-edge-IP emergency ceiling.
- Do not trust arbitrary client-supplied `x-forwarded-for`/`x-real-ip` headers unless the hosting platform documents that it strips and rewrites them. Treat IP controls as secondary because carrier NAT can group unrelated mobile users.

## Shared-state requirement

In-process maps are acceptable only for an explicitly labeled demo. On serverless deployments they are neither durable nor globally consistent:

- cold starts erase votes;
- parallel instances disagree;
- cooldowns and quotas can be bypassed across instances;
- unbounded identity/window/vote maps can cause memory growth.

For public production use, move votes and limits into a shared datastore such as Redis. Use atomic mutation for vote reversal and totals. Give limiter keys TTLs, bound retention/cardinality, and avoid allocating permanent state for malformed requests.

## Correctness details

- Repeating the same vote should usually be idempotent and return the unchanged snapshot; decide explicitly whether it consumes quota or cooldown.
- Switching sides must atomically decrement the old count and increment the new count.
- Validate/parse before allocating long-lived identity-specific state where practical, while retaining a separate coarse endpoint-abuse ceiling.
- Accessible button names should include or describe current totals; an explicit `aria-label` overrides visible numeric text for screen readers.
- Keep externally sourced social engagement separate from on-site community votes.

## Verification

- Unit tests: first vote, duplicate vote, reversal, voter isolation, resource isolation, signed-token tampering, window expiry.
- Route tests: invalid resource/value, malformed body, first vote, cooldown, cookie flags, cookie tampering, trusted-IP handling.
- Browser tests: selected state, 44px touch targets, live-region feedback, modal/card consistency, no overflow across representative mobile widths.
- Run unit and E2E suites with separate discovery patterns so Vitest/Jest does not collect Playwright specs.
- Verify the deployed canonical alias, not only localhost or an immutable preview URL.
