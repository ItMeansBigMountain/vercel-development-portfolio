# Jupyter.Notebooks Development Plan

Last updated: 2026-05-26

## Current role

Data science restart lab for technical analysis, bots, stats, plotting.

## Portfolio priority

High

## Detected context

- Classification: Legacy scripts/archive or docs
- Detected stack: Docs/static/archive
- Current tracked URL: https://jupyter-notebooks-green.vercel.app
- Tracker note: Wrap reusable scripts in a guided web UI/API; isolate credentials and rate limits

## Existing direction artifacts

- `DATA_SCIENCE_RESTART_PLAN.md`

## Development phases

1. Create notebook index by domain: market data, TA, stats, bot research. *(README index added.)*
2. Add reproducible environment files and sample datasets. *(`requirements.txt`, `.env.example`, and offline fixture helpers added.)*
3. Write first notebooks for trend plotting/backtest skeletons.
4. Optionally publish a static dashboard from notebooks.

## Vercel / hosting plan

Not direct Vercel app unless exporting dashboard/docs.

## Review checklist

- [x] Local build/test or deterministic script check passes.
- [x] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [x] README / workspace trackers updated with live URL and blockers.
