# algos Development Plan

Last updated: 2026-05-26

## Current role

Script/archive folder; productize only if useful.

## Portfolio priority

Low

## Detected context

- Classification: Legacy scripts/archive or docs
- Detected stack: Docs/static/archive
- Current tracked URL: https://algos-beta.vercel.app
- Tracker note: Wrap reusable scripts in a guided web UI/API; isolate credentials and rate limits

## Existing direction artifacts

- None yet.

## Development phases

1. Inventory reusable scripts and secrets/env assumptions.
2. Separate safe examples from private credentials.
3. Wrap highest-value script in CLI/docs or small dashboard.
4. Keep as archive if no product use emerges.

## Vercel / hosting plan

Static review shell okay for documentation; do not expose privileged tools.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.
