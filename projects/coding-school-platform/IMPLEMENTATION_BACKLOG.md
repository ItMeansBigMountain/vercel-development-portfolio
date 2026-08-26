# Coding School Platform — prioritized implementation backlog

Last updated: 2026-08-25
Source spec: `COMPETITOR_RESEARCH_AND_PRODUCT_SPEC.md`

## Priority model

- P0 = required to make the product a complete, child-safe coding-class tool rather than a demo.
- P1 = important differentiators after P0 workflows are coherent.
- P2 = scale/integration features after safety, review, and evidence loops are stable.

## P0 backlog — definitive MVP foundation

### P0.1 Role, demo-mode, and child-safety foundations

Acceptance criteria:

- Admin, teacher, student, and parent role shells exist with explicit route/view boundaries.
- Demo mode is visibly enabled and blocks real student/guardian PII entry by default.
- Parent-visible data is generated only from reviewed/approved fields.
- AI parsing UI includes redaction warning before paste.
- Tests prove private teacher notes and raw AI drafts do not appear in parent/student views.

Implementation notes:

- Build from existing demo-only data conventions.
- Add `privacyMode: demo | production_locked | production_enabled` to app/domain config.
- Keep production_enabled behind explicit owner/legal follow-up, not default code.

### P0.2 Roster, class section, schedule, and attendance data

Acceptance criteria:

- Seed demo rosters include teachers, students, guardians, class sections, scheduled sessions, and assignments.
- Teacher dashboard lists today/upcoming sessions for assigned students/classes.
- Teacher can mark attendance and save a `session_check_in` draft.
- Admin dashboard shows missing check-ins and stale sessions.
- Tests cover teacher/student assignment visibility and parent-child scoping.

Suggested data entities:

- `role_profiles`, `student_guardian_links`, `teacher_student_assignments`, `class_sections`, `scheduled_sessions`, `attendance_records`, `session_check_ins`.

### P0.3 Activity model with required activity types

Acceptance criteria:

- Structured activity schema supports fill-in-the-blank, typed-answer, word-bank, code-text/syntax-lint, predict-output, debug-explain, and project evidence.
- Existing Basic 13 / Linear Search content can be represented as activities.
- Activity metadata includes `conceptTags`, `skillTags`, `ageBand`, `rubric`, `expectedEvidence`, `parentSummaryTemplate`, and `teacherNotes`.
- Teacher-only solution/debug notes never render in student view.
- Tests validate every activity has required tags/rubric/evidence fields.

### P0.4 Syntax-only linting and keyword extraction

Acceptance criteria:

- Lint service returns `executionAttempted: false` for all code-text activities.
- JavaScript and Python syntax-only checks catch bracket/quote balance, likely Python missing colon/indent issues, and forbidden API/import names.
- Lint output uses child-friendly messages and teacher-facing severity.
- Keyword extraction returns concepts/skills from configured curriculum vocabulary.
- Tests prove no subprocess/eval/runtime execution path is called.

Non-goal:

- Do not add arbitrary code execution, autograding, container sandboxes, or server-side run buttons in P0.

### P0.5 Live classroom presence and submission states

Acceptance criteria:

- Student activity state transitions through `not_opened`, `opened`, `active_now`, `idle`, `help_requested`, `draft_saved`, `submitted`, `returned_for_revision`, `reviewed`, `mastery_approved`.
- Teacher view can see current classroom/session state and review queue.
- Presence events store purpose-limited metadata only: user id, session/activity id, state, timestamps.
- Parent view does not expose live presence or idle/help details.
- Tests cover state transition validity and role visibility.

### P0.6 Teacher review and feedback loop

Acceptance criteria:

- Teacher can review any submission, set rubric results, add feedback, request revision, or approve mastery.
- Completion, submission, review, and mastery are separate states.
- Mastery approval creates progress events and badge/accomplishment records.
- Parent-safe summary is a separate approved field, not raw teacher/private note text.
- Tests prove parent dashboard updates only after review/approval.

### P0.7 Progress/mastery engine and dashboards

Acceptance criteria:

- Progress events aggregate by concept, skill, language, activity type, mastery level, and time.
- Student dashboard shows assigned mission, feedback, and approved accomplishments.
- Parent dashboard shows weekly win, current concepts in plain English, confidence/blocker/next step, and approved project evidence.
- Teacher dashboard shows class concept heatmap, review queue, missing check-ins, and students needing reinforcement.
- Admin dashboard shows teacher onboarding, stale sessions, curriculum coverage, and AI usage/quota placeholders.

### P0.8 AI-summary paste and local parser fallback

Acceptance criteria:

- Teacher can paste lesson/Zoom summary into an AI-assisted parser only when entitlement is enabled.
- Non-entitled accounts get deterministic local parser only.
- Parser outputs `sessionSummary`, `conceptTags`, `skillTags`, `languageTags`, `projectTags`, `strengths`, `blockers`, `homework`, `confidence`, `masterySignals`, `recommendedActivities`, `parentSafeDraft`, and `redactionWarnings`.
- Teacher must review/confirm parser suggestions before they affect progress or parent reports.
- Tests cover AI disabled, local fallback, entitlement enabled with mocked parser, and redaction warnings.

### P0.9 Teacher training and curriculum-authoring gates

Acceptance criteria:

- T0-T5 teacher training modules exist as first-class data.
- Teacher can record notes after T0 but cannot approve module mastery without passing the relevant training evidence.
- Curriculum authoring is draft/versioned and requires admin approval to publish.
- Student prompts and teacher-only solution/debug notes are stored/rendered separately.
- Tests cover permission gates and activity version status transitions.

### P0.10 Durable documentation and tracker updates

Acceptance criteria:

- README links to the definitive competitor/spec doc and backlog.
- Product direction states the new no-code-execution-first principle.
- Development plan is updated from the 2026-05-26 CRM backlog to the P0 complete-tool backlog.
- Release docs continue to clearly distinguish demo/local-only status from production launch.

## P1 backlog — differentiators after P0

### P1.1 Portfolio and project evidence center

- Approved project cards with title, description, concepts, screenshots/links, teacher review, student reflection, and next iteration.
- Exportable parent-friendly portfolio report.

### P1.2 Parent report generator

- Weekly/monthly report preview with teacher approval.
- AI/local draft suggestions grounded only in reviewed evidence.
- Export to PDF/HTML/CSV.

### P1.3 Curriculum library and reusable templates

- Activity templates for Basic 13, algorithms, Scratch-style sequencing, debugging, and AI-safety reflection.
- Version comparison for curriculum revisions.

### P1.4 Teacher professional learning dashboard

- Admin view of teacher training progress and recertification needs.
- Teacher evidence review flow.

### P1.5 Accessibility and younger-learner modes

- Word-bank icon/audio labels.
- Pre-reader flows modeled after K-5 coding products without copying their content.
- Keyboard-only and screen-reader pass.

## P2 backlog — integrations and scale

### P2.1 LMS/rostering integrations

- CSV import/export first.
- Google Classroom/Clever/ClassLink/Canvas only after production privacy decisions.

### P2.2 Secure runtime exploration spike

- Only after P0 proves product value.
- Research options for isolated execution if the owner explicitly wants run/autograde features.
- Must include threat model, cost model, logging/privacy plan, and child-data review.

### P2.3 District/multi-location analytics

- Cross-location curriculum outcomes.
- Teacher training dashboards.
- Retention and progress health without exposing unnecessary student data.

### P2.4 Public showcase/gallery

- Deferred until consent, moderation, privacy, and public-sharing legal policy are approved.

## Dependency map

1. P0.1 child-safety foundations must precede all parent/AI/report work.
2. P0.2 rosters/schedules must precede live sessions and attendance.
3. P0.3 activity model must precede submissions, linting, and progress.
4. P0.4 linting can run in parallel with P0.5 presence after activity schema stabilizes.
5. P0.6 teacher review must precede P0.7 dashboards and P0.8 report generation.
6. P0.9 teacher training gates should be implemented before production curriculum authoring.

## Suggested next implementation cards

1. Software-developer: implement P0.1-P0.3 data/schema/fixtures and route guards.
2. Software-developer: implement P0.4 syntax-only lint service and tests.
3. Software-developer: implement P0.5-P0.6 classroom presence, submissions, and teacher review queue.
4. Software-developer: implement P0.7 parent/student/teacher/admin dashboards from reviewed progress events.
5. Researcher/reviewer: review child-safety/privacy copy before any production launch.
6. Reviewer: independent acceptance review after each implementation card, with explicit checks for no code execution and no raw AI/private notes in parent views.

## Non-negotiable acceptance checklist for the P0 product

- [ ] Teacher/student/parent/admin role boundaries tested.
- [ ] No real student data in demo fixtures.
- [ ] No arbitrary learner code execution.
- [ ] Fill-in-the-blank, typed-answer, word-bank, and code-text activity types exist.
- [ ] Syntax-only lint reports `executionAttempted: false`.
- [ ] Teacher review is required for mastery and parent report updates.
- [ ] Parent dashboard uses plain English and reviewed evidence only.
- [ ] AI-summary paste has entitlement gate, redaction warning, local fallback, and teacher review.
- [ ] Teacher training gates exist before curriculum authoring/mastery approval.
- [ ] README, product direction, and release notes distinguish demo/local status from production.
