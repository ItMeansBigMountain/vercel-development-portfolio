# Coding School Platform Direction

Codology becomes the learning engine inside the broader school platform.

## Product goal

A parent/student/teacher learning portal where students practice coding, parents track progress, and teachers record lesson notes/test outcomes.

The definitive P0 product specification is `COMPETITOR_RESEARCH_AND_PRODUCT_SPEC.md`, backed by official competitor/source research. The prioritized build sequence is `IMPLEMENTATION_BACKLOG.md`.

The product wedge is a child-safe coding-class operating system: rosters/schedules, live classroom presence, teacher-reviewed submissions, syntax-only linting with no arbitrary code execution, structured activities, progress/mastery evidence, AI-summary paste with local fallback, parent-safe reports, teacher training, and curriculum authoring.

The current curriculum/product source of truth is `CURRICULUM_SOURCE_OF_TRUTH.md`. It supersedes scattered curriculum notes for implementation sequencing and requires the teacher mastery track before learner-facing Algorithm Academy workflows.

## Core roles

- Students: lessons, examples, practice, quizzes, streaks, confidence checks.
- Parents: child progress, strengths, gaps, upcoming lessons, teacher notes.
- Teachers: lesson notes, test results, attendance, assignments, progress updates.
- Admins/owners: rosters, schedules, role access, teacher training gates, curriculum publishing, AI entitlements, demo/production safety controls, and report/export oversight.

## Safety/product constraints

- No real student data in demo mode.
- No arbitrary learner code execution in the P0 production-safe workflow; use syntax-only linting and teacher review first.
- No unreviewed AI output in parent/student views.
- No public student gallery, billing, or LMS/rostering integration until privacy/legal launch choices are made.
- Completion, submission, review, mastery, and parent-ready reporting are separate states.

## Codology integration

- Import `algos` examples from all branches as lessons and code exercises.
- Convert each algorithm into explanation, runnable example, practice task, and assessment rubric.
- Store progress by concept, language, difficulty, and mastery state.
- Start with Basic 13 and Linear Search as the first concrete Algorithm Academy content, using teacher-reviewed evidence and accomplishment badges rather than click-through completion.

## Coding-school CRM direction

Build functional parity with the useful parts of a coding-school customer/teacher portal:

- Teacher login and schedule view.
- Students already assigned to teachers.
- After-class check-in from each scheduled student session.
- Teacher notes, attendance, homework, concepts, blockers, and confidence ratings.
- AI parser for pasted Zoom after-meeting notes, gated to entitled accounts/quotas to save API tokens.
- Non-AI tag parser for accounts without AI access: one tag per line, comma-separated, space-separated, and local keyword extraction.
- Human-reviewed AI/local tags for languages, concepts, skills, projects, blockers, and mastery evidence.
- Parent dashboard with weekly notes and plain-English progress.
- Student dashboard with accomplishments, learning journey, projects, and Codology practice.
- Progress graph powered by tags and evidence over time.

Research and implementation plan: `CODERSCHOOL_CRM_RESEARCH_AND_PLAN.md` and `docs/plans/2026-05-26-coding-school-crm.md`.
