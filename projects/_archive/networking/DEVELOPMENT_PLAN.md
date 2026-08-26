# networking Development Plan

Last updated: 2026-05-26

## Current role

Authorized own-device pentesting/red-team learning lab.

## Portfolio priority

High

## Detected context

- Classification: Legacy scripts/archive or docs
- Detected stack: Python
- Current tracked URL: https://networking-ebon.vercel.app
- Tracker note: Wrap reusable scripts in a guided web UI/API; isolate credentials and rate limits

## Existing direction artifacts

- None yet.

## Development phases

1. Organize tools by local LAN, WAN self-test, recon, reporting, and lab safety.
2. Add legal/authorization guardrails and target allowlist config.
3. Create runnable notebooks/scripts for device inventory and safe scans.
4. Generate reports with remediation checklists.

## Vercel / hosting plan

Do not expose attack tooling as public Vercel app; deploy docs/demo only.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.
