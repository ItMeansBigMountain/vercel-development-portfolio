# honda-tech-upgrade Development Plan

Last updated: 2026-05-26

## Current role

Plan-only/static review shell needing focused MVP.

2026-06-09 review update: initial inspection found only docs/specs, but the working tree now contains a credential-free Honda maintenance planner scaffold. Local validation passes with `npm run vercel-build` (3/3 Node tests) and local Express HTTP 200; public Vercel still needs redeploy + smoke test before the live URL can be marked as the new MVP.

## Portfolio priority

Medium

## Detected context

- Classification: Plan/spec folder with static review shell
- Detected stack: Docs/static/archive
- Current tracked URL: https://honda-tech-upgrade.vercel.app
- Tracker note: Convert shell into focused MVP with one high-friction user outcome

## Existing direction artifacts

- `HONDABOYZ_API_REPLACEMENT_PLAN.md`

## Development phases

1. Pick one concrete user outcome.
2. Build a no-login static Vercel MVP with seed/demo data.
3. Add one interactive flow and clear CTA.
4. After review, add accounts/payments/API integrations only if needed.

## Vercel / hosting plan

Use existing static Vercel shell; replace placeholder content with real MVP flow.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.
