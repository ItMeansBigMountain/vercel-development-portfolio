# coding-school-platform Development Plan

Last updated: 2026-08-25

## Current role

Coding school CRM + learning portal.

## Portfolio priority

High

## Detected context

- Classification: Coding-school CRM + learning portal
- Detected stack: Product direction
- Current tracked URL: https://coding-school-platform.vercel.app
- Tracker note: Queued CRM plan: functional parity with teacher schedule, student check-ins, AI Zoom-note tag extraction, progress graphs, parent dashboard, and Codology lesson linkage.

## Existing direction artifacts

- `COMPETITOR_RESEARCH_AND_PRODUCT_SPEC.md`
- `IMPLEMENTATION_BACKLOG.md`
- `CURRICULUM_SOURCE_OF_TRUTH.md`
- `CODERSCHOOL_CRM_RESEARCH_AND_PLAN.md`
- `PRODUCT_DIRECTION.md`
- `TEACHER_HIRING_LOCATION_PLAN.md`
- `docs/plans/2026-05-26-coding-school-crm.md`

## Development phases

1. Implement P0.1-P0.3 from `IMPLEMENTATION_BACKLOG.md`: role/demo/child-safety foundations, rosters/schedules/attendance, and structured activity schemas.
2. Implement P0.4-P0.6: syntax-only linting with no arbitrary code execution, live classroom presence/submission states, and teacher review/feedback.
3. Implement P0.7-P0.8: progress/mastery dashboards and AI-summary paste with entitlement gate, redaction warning, local fallback, and teacher confirmation.
4. Implement P0.9: teacher training gates and versioned curriculum authoring before mastery approval/publishing.
5. Keep P1/P2 work deferred until P0 proves child-safe parent reporting and teacher-reviewed progress evidence.

## Non-negotiable P0 constraints

- No real student data in demo mode.
- No arbitrary learner code execution; P0 uses syntax-only linting and teacher review.
- No unreviewed AI output in parent/student views.
- Parent dashboards update only from teacher-reviewed evidence.
- Public galleries, billing, production student records, and LMS/rostering integrations are deferred.

## Vercel / hosting plan

Keep Vercel demo public; first MVP should be no-real-student-data demo mode.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.
