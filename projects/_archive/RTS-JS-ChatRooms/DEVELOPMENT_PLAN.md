# RTS-JS-ChatRooms Development Plan

Last updated: 2026-05-26

## Current role

Backend/API candidate.

## Portfolio priority

Medium

## Detected context

- Classification: Python/Flask/scripts
- Detected stack: Python, Product direction
- Current tracked URL: https://rts-js-chatrooms.vercel.app
- Tracker note: Harden OAuth callbacks, add public health/demo mode, durable token storage; Wrap reusable scripts in a guided web UI/API; isolate credentials and rate limits

## Existing direction artifacts

- `PRODUCT_DIRECTION.md`

## Development phases

1. Add health endpoint and production settings.
2. Template required env vars without secrets.
3. Add smoke tests for public endpoints.
4. Choose Vercel serverless vs Render/Railway/Fly based on durable storage needs.

## Vercel / hosting plan

Verify public health endpoint; avoid SQLite-on-Vercel for durable writes.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.
