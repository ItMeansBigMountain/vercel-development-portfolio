# local-meeting-transcriber Development Plan

Last updated: 2026-05-26

## Current role

Private local/free meeting recorder, transcriber, and long-term insight tracker.

## Portfolio priority

High

## Detected context

- Classification: Legacy scripts/archive or docs
- Detected stack: Product direction
- Current tracked URL: https://local-meeting-transcriber.vercel.app
- Tracker note: Wrap reusable scripts in a guided web UI/API; isolate credentials and rate limits

## Existing direction artifacts

- `PRODUCT_DIRECTION.md`

## Development phases

1. Define local audio ingestion/transcription path.
2. Add searchable transcript store and meeting summary schema.
3. Extract decisions/actions/topics over time.
4. Build privacy-first local UI or static demo.

## Vercel / hosting plan

Public Vercel should be docs/demo only; real transcription remains local/private.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.
