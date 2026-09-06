# Codology Development Plan

Last updated: 2026-05-26

## Current role

Learning engine and curriculum/exercise source for coding school platform.

## Portfolio priority

High

## Detected context

- Classification: Node/Express app/API
- Detected stack: Node/package app, Vercel config, Product direction
- Current tracked URL: https://codology-three.vercel.app
- Tracker note: Audit dependencies, add smoke tests, improve mobile UX hierarchy and empty states

## Existing direction artifacts

- `ALGOS_IMPORT_PLAN.md`
- `PRODUCT_DIRECTION.md`

## Development phases

1. Convert algos branch inventory into lesson records.
2. Add runnable examples/practice/assessment rubrics.
3. Expose lesson recommendation API or JSON for coding-school CRM.
4. Decide durable leaderboard/progress storage.

## Vercel / hosting plan

Existing frontend/API on Vercel; verify alias content after each release.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.
