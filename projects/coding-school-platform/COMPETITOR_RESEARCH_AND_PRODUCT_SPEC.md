# Coding School Platform — competitor research and definitive product specification

Last updated: 2026-08-25
Research role: current external research using official/primary sources where accessible.

## 1. Research question

What should THE complete coding-class tool include if it combines the best observable patterns from coding-school CRMs, CS classroom platforms, formative-assessment tools, parent progress portals, and safe child-learning products without copying proprietary branding, UI, curriculum, or implementation?

## 2. Executive answer

The original product should be a child-safe coding-class operating system: schedule/roster management, live class presence, student submissions, teacher review, syntax-only code feedback, structured activity authoring, progress/mastery evidence, parent-safe reporting, and teacher training in one workflow. The main differentiator is not “another online IDE”; it is a teacher-led evidence engine for small coding classes where every class session becomes reviewed progress, every parent report is grounded in teacher-approved evidence, and every learner activity is safe-by-default with no server-side code execution.

This platform should deliberately avoid full runtime execution in the first production version. CodeHS emphasizes full coding environments, autograders, real-time activity, and collaboration.[5][6] Code.org emphasizes teacher dashboards, student work review, feedback, and built-in student labs/IDEs.[10][11] Matching them directly would increase safety, infrastructure, and academic-integrity complexity; our defensible wedge is syntax-only linting, teacher-reviewed evidence, guided coding prompts, offline/demo safety, and parent-visible mastery.

## 3. Source-grounded competitor notes

### theCoderSchool Notes+, Coder Progress, Coder Story, and Code Coaching

Official theCoderSchool pages describe a semi-private 2:1 Code Coaching model with customized, project-based learning instead of one-size-fits-all curriculum.[1][2] Their FAQ says coaches write weekly structured Notes+ notes that track languages, concepts, homework, and session information, email parents after each session, and link to Coder Progress for progress-over-time summaries.[1] Their Code Coaching page adds weekly notes, Coder Points, Coder Story roadmap support, a student portal with accomplishments, App Reviews/app uploads, Coder Fair showcases, CoderGames, Rounds of Code quizzes, AppStream videos, and broad language coverage.[2] Their Coder Story page frames the roadmap as optional activities that open up as students become more proficient, not as a rigid curriculum.[3]

Implication: our product needs a weekly/session notes system, progress-over-time dashboard, points/badges, roadmap/story, app/project evidence, and parent-friendly summaries. It should not copy Notes+, Coder Progress, Coder Points, Coder Story, AppStream, Rounds of Code, or their wording/branding; use original naming and schemas.

Child-safety signal: theCoderSchool privacy page states it keeps student progress information, submitted code/gallery information, Coder Reviews, competition scores, and other progress data, and says it does not knowingly collect/post/distribute under-13 personal information without parent/guardian consent; its Zoom section emphasizes K-12 educational configuration and bans recording/screenshots/social sharing of class video materials.[4] Implication: our product should minimize child PII, keep real-student data out of demos, redact AI inputs, and separate parent consent/legal launch decisions from demo implementation.

### CodeHS

CodeHS positions itself as a complete computer science classroom hub with courses, online IDE, real-time collaboration, classroom management, grading, professional development, quizzes, projects, examples, assessments, badges, lesson plans, and custom assignments.[5] CodeHS Pro details gradebook, Fast Grade, AI grade suggestions, assignment access controls, due dates, progress dashboards, AI hints, real-time activity dashboard/collaboration, plagiarism reports, code replay, time tracking, LMS integrations, and data reports.[6] CodeHS help says progress tools cover assignment, lesson, module, quiz score, and time tracking, with status colors for finalized/reviewed/submitted/not submitted/unopened, and real-time progress updates.[7]

Implication: for older CS classrooms, expectations include assignments, submissions, teacher feedback, gradebook/review states, time/activity signals, progress dimensions, and teacher resources. We should borrow the abstraction of status/state tracking but intentionally avoid first-party code execution, autograding, plagiarism reports, and code replay until safety/infra requirements are explicit.

### Formative

Formative’s teacher-facing page emphasizes unlimited lessons/assessments/practice sets, 20+ tech-enhanced question and multimedia types, real-time live response data, standards tagging, flexible feedback, teacher/student pacing, gamification, shared libraries, district dashboards, and AI-assisted activity creation.[8] Its help article shows participation/open/submitted/late/timed/overlapping-session indicators, color-coded real-time performance cells, live presence indicators, manual scoring, feedback, answer-key details, and close/reopen assignment controls.[9]

Implication: the coding product needs classroom presence, opened/in-progress/submitted states, live response streams, flexible activity blocks, manual scoring/feedback, close/reopen controls, and standard/concept tagging. For our domain, “standards” should be conceptTags/skillTags/mastery rubrics rather than generic academic standards only.

### Code.org / CodeAI

Code.org support says the teacher dashboard supports viewing/evaluating work, managing class sections, viewing progress by lessons/levels, checking time spent and last-updated data, reviewing individual coding-level work, leaving feedback on many programming levels, and collecting text responses, assessments, surveys, and projects in one place.[10] Code.org’s current teacher page describes separate teacher and student experiences, a teacher dashboard that keeps classes/lessons/student progress in view, curriculum, AI Teaching Assistant, AI Tutor, professional learning, and student-facing labs for Music, Web, Python, Sprite, and AI activities.[11] Its getting-started guide centers teacher accounts, class sections, adding students, assigning work, progress tracking, viewing code, feedback, professional development, and verified-teacher access for assessments/answer keys.[12]

Implication: we need separate role experiences, class sections/rosters, assignments, project/text-response capture, feedback, verified/teacher-only resources, and professional learning. We should not claim free/open Code.org-scale curriculum breadth; our edge is small-class coaching and parent progress.

### Tynker

Tynker’s school page highlights grade-banded K-12 curriculum, videos, puzzles, hands-on coding modules, automatic grading, student management, privacy/data security, COPPA/FERPA/SOPIPA claims, built-in assessment framework, concept map, grading and metrics dashboards, LMS/rostering integrations, and professional development.[13] Tynker’s parent page emphasizes a parent dashboard with mastery stats, portfolios, certificates, projects, real-world languages, and a moderated/safe community.[14]

Implication: families expect visible progress/mastery stats, portfolio artifacts, certificates/badges, and clear safety messaging. Schools expect rostering/LMS/security language and teacher training.

### Kodable

Kodable describes a K-5 product for teachers with simple sign-on, pre-reader coding activities, game levels that increase in difficulty, creative projects, teacher dashboard, grade-broken activities, teacher-created curriculum/guides, assignable video lessons, and a parent dashboard for student progress.[15] Its dashboard update describes class progress, lessons completed, administrator access, assignments/curriculum resources, and student management.[16] Its dashboard video page says the teacher dashboard covers student login, assigning game levels, coding lesson plans, and teacher resources.[17]

Implication: for younger learners, onboarding must be very simple, activities should support pre-reader/word-bank/fill-in formats, parents need simple progress, and teachers need assignable resources without coding expertise.

### Scratch educator ecosystem

Scratch Foundation says Teacher Accounts let educators create student accounts and manage student projects and participation, and provides activity guides, videos, tutorials, and educator events/resources.[20] Search results for the Scratch educator page also indicate Scratch Teacher Accounts help educators create student accounts and manage projects/comments.[19]

Implication: project management, teacher-created student accounts, comments/participation controls, and creative project artifacts are baseline expectations for child coding tools.

### Inaccessible / lower-confidence source note

Official CodeCombat teacher pages were blocked or failed in extraction during this run. Search results indicate a teacher account allows classroom setup, progress monitoring, license management, and resources, but this finding is lower confidence because the page body was not accessible to verify beyond the search result.[18]

## 4. Original product specification

### 4.1 Product identity

Working name: Coding School Platform / Algorithm Academy.

Promise: a child-safe, teacher-led classroom portal that turns every coding lesson into reviewed evidence, actionable teacher feedback, and parent-readable progress while keeping code execution out of the production backend until explicitly approved.

Design constraints:

- Child-safe by default: no real student data in demo, minimal PII, private notes separated from parent notes, AI input redaction, consent gates before production launch.
- Teacher-led mastery: AI and automation suggest; teachers approve.
- Syntax-only coding assistance: parse/lint source text for likely syntax issues and vocabulary/concept tags; do not execute learner code on the server.
- Evidence before mastery: completion, submission, review, and mastery are separate states.
- Original names/UX: do not reuse competitor product names, visual hierarchy, proprietary curriculum text, or screenshots.

### 4.2 Roles and permissions

Admin / owner:

- Manage schools/locations, teachers, students, parents, cohorts, class sections, schedules, lesson catalogs, rubrics, safety settings, and AI entitlements.
- View missing check-ins, inactive students, teacher training status, parent-report readiness, and curriculum coverage.
- Export parent-safe reports and CSV/JSON evidence summaries.
- Configure demo/prod mode and real-data launch gates.

Teacher / coach:

- View today/upcoming schedule and assigned students/classes.
- Start/end live class sessions.
- See active student presence, opened activity, draft/submission state, and help-needed flags.
- Assign activities and capture after-class notes.
- Review syntax-only lint results, typed/fill-in/word-bank answers, code text, reflection, screenshots/links, and teacher observations.
- Approve/reject/request-revision for submissions with rubric feedback.
- Paste AI meeting-summary notes only after redaction warning; review extracted keywords before save.
- Complete teacher training/mastery modules before unlocking curriculum-authoring/admin functions.

Student:

- See assigned missions, due dates, prerequisites, concept goals, and safe AI/hint rules.
- Complete activity types: fill-in-the-blank, typed-answer, word-bank, code-text draft, predict-output, debug-explain, reflection, project link/screenshot.
- Submit evidence without public sharing by default.
- Receive teacher feedback and see approved badges/progress after review.
- Ask for help using structured flags, not open messaging in the first slice.

Parent / guardian:

- See child schedule, attendance/check-in summaries, weekly win, current concepts in plain English, confidence trend, blocker/next step, approved project/portfolio evidence, and teacher-approved notes.
- Never see private teacher-only notes, raw sensitive behavior notes, or unreviewed AI output.

### 4.3 Scheduling, rosters, and class sessions

Entities:

- `school_location`, `class_section`, `student_profile`, `guardian_profile`, `teacher_profile`, `teacher_assignment`, `scheduled_session`, `attendance_record`, `session_check_in`.

Required flows:

1. Admin creates/loads demo rosters and assigns students to teacher(s).
2. Teacher dashboard shows today’s sessions, student names/display aliases, class type, activity plan, and last progress signal.
3. Teacher starts session: status becomes `live`; students joining/opening assignments generate presence events.
4. Teacher records attendance: `present`, `late`, `absent`, `makeup_needed`, `excused`.
5. Teacher ends session only after check-in draft is saved or explicit `no_check_in_reason` is set.

### 4.4 Live classroom presence and submissions

Presence states inspired by Formative/CodeHS-style status systems but adapted to coding school needs:

- `not_opened`
- `opened`
- `active_now`
- `idle`
- `help_requested`
- `draft_saved`
- `submitted`
- `returned_for_revision`
- `reviewed`
- `mastery_approved`

Presence data should be low-risk metadata: assignment id, state, timestamp, device class if needed; avoid screen capture, keystroke replay, or raw interaction tracking in the first child-safe slice.

Submission object:

- `submissionId`, `studentId`, `sessionId`, `activityId`, `activityType`, `answerPayload`, `syntaxLintFindings`, `keywordTags`, `studentReflection`, `submittedAt`, `reviewStatus`, `teacherFeedback`, `parentSafeSummary`, `evidenceLinks`.

### 4.5 Syntax-only linting with no code execution

Policy:

- The first production-safe version must not run arbitrary learner code server-side.
- Client-side previews may remain demo/sandbox-only and must be clearly separated from the reviewed submission pipeline.
- Linting should only parse source text and detect syntax/shape issues.

Initial lint targets:

- JavaScript/TypeScript-like snippets: bracket/paren/brace balance, unterminated strings, missing semicolons as warning only, likely assignment-vs-comparison, forbidden APIs list.
- Python-like snippets: indentation consistency, missing colon after `if/for/while/def/class`, unmatched brackets/quotes, likely tabs/spaces mix, forbidden imports/functions.
- Scratch/pseudocode: vocabulary/tag extraction and checklist validation instead of syntax parsing.

Output shape:

```json
{
  "language": "python",
  "executionAttempted": false,
  "findings": [
    {
      "severity": "warning",
      "line": 3,
      "code": "missing-colon",
      "message": "This line looks like it starts a block and may need a colon.",
      "teacherOnly": false
    }
  ],
  "conceptTags": ["loops", "conditions"],
  "safeToDisplayToStudent": true
}
```

### 4.6 Activity types

Common fields:

- `activityId`, `title`, `ageBand`, `track`, `moduleId`, `conceptTags`, `skillTags`, `prompt`, `teacherNotes`, `rubric`, `expectedEvidence`, `parentSummaryTemplate`, `safetyFlags`.

Required activity types:

1. Fill-in-the-blank
   - Prompt text with blanks.
   - Accepted answers per blank plus optional synonym/regex rules.
   - Teacher can override correctness.
2. Typed answer
   - Short text, paragraph, or reflection.
   - Teacher rubric and keyword suggestions.
3. Word bank
   - Draggable/tappable terms for sequencing, vocabulary, trace tables, and code-line ordering.
   - Supports pre-reader/younger-learner mode with icons/audio labels later.
4. Code text / syntax-only lint
   - Student enters or pastes code text.
   - System returns syntax-only findings and concept keyword extraction.
   - Teacher reviews for logic/mastery.
5. Predict-output
   - Student predicts what code should print/do without execution.
6. Debug-explain
   - Student explains bug and proposed fix.
7. Project evidence
   - Link, screenshot, file metadata, demo script, or teacher observation.

### 4.7 Teacher review and feedback

Review states:

- `unsubmitted`, `submitted`, `needs_teacher_review`, `returned_for_revision`, `reviewed_not_mastered`, `mastery_approved`, `parent_ready`, `archived`.

Feedback components:

- Rubric ratings by concept/skill.
- Inline comment anchors for text/code lines (no code execution needed).
- Strength, next step, misconception, homework, and parent-safe note fields.
- One-click “convert to parent summary” from approved feedback.
- Required teacher approval before mastery, badges, or parent reports update.

### 4.8 Progress and mastery metrics

Track by evidence, not clicks:

- Concept exposure count.
- Teacher-reviewed mastery level: `introduced`, `practicing`, `developing`, `proficient`, `mentor-ready`.
- Skill tags: reading-code, predicting-output, tracing, debugging, documentation, decomposition, testing mindset, explaining-code, safe-AI-use.
- Activity/submission states over time.
- Confidence trend from teacher rating and optional student self-check.
- Parent-safe weekly win and next step.
- Portfolio milestones and approved artifacts.
- Teacher training/mastery status.

Dashboards:

- Teacher: class live state, review queue, missing check-ins, concept heatmap, students needing reinforcement.
- Student: current mission, approved badges, feedback, next recommended action.
- Parent: weekly progress, concepts in plain English, confidence/blockers, approved project evidence.
- Admin: teacher onboarding, roster/schedule health, stale sessions, curriculum coverage, AI quota usage.

### 4.9 AI-summary paste and keyword extraction

Input types:

- Pasted Zoom after-meeting summary, teacher freeform note, transcript excerpt, lesson summary.

Safety rules:

- AI parsing disabled by default unless account entitlement permits it.
- Prompt user to redact student PII, family/private details, addresses, school details, contact info, credentials, and health/legal/behavior-sensitive content.
- Store original paste only if product owner explicitly chooses retention; default should store derived teacher-reviewed fields and discard raw paste.
- AI output never goes to parents or students until teacher reviewed.
- Local deterministic parser always available.

Output fields:

- `sessionSummary`, `conceptTags`, `skillTags`, `languageTags`, `projectTags`, `strengths`, `blockers`, `homework`, `confidence`, `masterySignals`, `recommendedActivities`, `parentSafeDraft`, `redactionWarnings`.

Local fallback:

- One tag per line, comma-separated, semicolon-separated, hashtag-style, and keyword extraction from configured vocabulary.
- Confidence score indicates parser source: `manual`, `local_keyword`, `ai_suggested`, `teacher_confirmed`.

### 4.10 Teacher training and curriculum authoring

Teacher training modules:

- T0: platform safety and parent-safe notes.
- T1: Basic 13 coaching mastery.
- T2: Algorithm Academy coaching mastery.
- T3: debugging and hint ladders.
- T4: child-safe AI-assisted coding.
- T5: portfolio coaching.

Training gates:

- Teachers can record notes immediately.
- Teachers can review beginner work after T0.
- Teachers can approve mastery for a module only after passing that module’s teacher mastery artifact.
- Teachers can author curriculum only after curriculum-authoring training and admin approval.

Curriculum authoring:

- Structured module/activity builder with preview as teacher/student/parent.
- Versioned curriculum items.
- Teacher-only solution/debug notes separated from student prompts.
- Required metadata: ageBand, concepts, skills, prerequisites, safety policy, rubric, parent summary template, expected evidence, activity type.
- Publish flow: draft → internal review → active → archived.

### 4.11 Data model additions

Minimum tables/collections to implement next:

- `users`, `role_profiles`, `student_guardian_links`, `teacher_student_assignments`.
- `class_sections`, `scheduled_sessions`, `attendance_records`.
- `curriculum_modules`, `activities`, `activity_versions`, `rubrics`.
- `presence_events`, `submissions`, `teacher_reviews`, `feedback_comments`.
- `progress_events`, `mastery_records`, `badges`, `portfolio_artifacts`.
- `teacher_training_modules`, `teacher_training_evidence`.
- `ai_entitlements`, `ai_parse_jobs`, `local_parse_results`, `redaction_warnings`.

### 4.12 Non-goals / explicit exclusions

- No real billing in the first product slice.
- No full code execution/autograding of arbitrary learner code.
- No open student-to-student messaging/social network.
- No public gallery for minors until consent/moderation/legal review is complete.
- No unreviewed AI-generated parent reports.
- No claims of CodeHS/Code.org/Formative/Tynker/Kodable parity; use them as market references only.

## 5. Product opportunities and contradictions

Opportunities:

- Competitors either emphasize coding IDE/autograding (CodeHS/Code.org), general formative assessment (Formative), self-paced/gamified coding curricula (Tynker/Kodable), or small-school human coaching/progress notes (theCoderSchool). The gap is a small coding-school classroom operating system with parent reporting and teacher-approved evidence.
- Syntax-only linting avoids the hardest runtime sandbox/security problems while still giving learners useful immediate feedback.
- Teacher training as a first-class product feature is a trust differentiator for schools/franchises.

Contradictions / tradeoffs:

- CodeHS shows market demand for full coding environments, real-time activity, and code-history tooling.[5][6] Code.org shows market demand for class progress dashboards, code review, feedback, and student labs.[10][11] Child-safe MVP constraints argue against arbitrary code execution and keystroke/code replay in the first release.
- Formative-style live presence is useful, but high-resolution activity tracking can become privacy-sensitive; keep presence low-risk and purpose-limited.[9]
- Parent dashboards are attractive, but parent-visible output must lag behind teacher review to avoid leaking raw AI or sensitive class notes.

Confidence: High for the core competitor observations from extracted official pages. Medium for CodeCombat due extraction failures. Medium-high for product recommendations because they are reasoned implications from multiple official sources and existing project direction, not direct market validation.

## Sources

[1] Best place for kids coding is at theCoderSchool — https://www.thecoderschool.com/faq
[2] Coding Classes and Camps for Kids Near You | theCoderSchool Code-coaching — https://www.thecoderschool.com/code-coaching
[3] Our Coder Story — https://www.thecoderschool.com/coderstory
[4] Privacy Policy — https://www.thecoderschool.com/privacy
[5] Teacher Use Cases — https://codehs.com/teachers
[6] CodeHS Pro | CodeHS — https://codehs.com/pro
[7] Tracking Student Progress | CodeHS Knowledge Base — http://help.codehs.com/en/articles/71219-tracking-student-progress
[8] For Teachers — https://www.formative.com/teachers
[9] View and Score Responses — https://help.formative.com/en/articles/6198532-view-and-score-responses
[10] Viewing student progress - Code.org Support — https://support.code.org/hc/en-us/articles/115000693231-Viewing-student-progress
[11] Teach Computer Science and Artificial Intelligence with CodeAI - Code.org — https://code.org/en-US/teachers
[12] I'd like to start using CodeAI in my classroom. How should I start? — https://support.code.org/hc/en-us/articles/228116468-I-d-like-to-start-using-CodeAI-in-my-classroom-How-should-I-start
[13] Coding for School: Teach K-12 Students to Code — https://www.tynker.com/school
[14] A Parents Guide on Coding — https://www.tynker.com/parents
[15] What is Kodable? — https://www.kodable.com/videos/what-is-kodable
[16] New Kodable Dashboard is Live | Kodable — https://www.kodable.com/learn/kodable-dashboard
[17] How to Use The Kodable Teacher Dashboard | Kodable — https://www.kodable.com/videos/how-to-use-the-kodable-teacher-dashboard
[18] What's a Teacher Account? — https://codecombat.com/teachers
[19] Educators - Scratch — https://scratch.mit.edu/educators
[20] For Educators | Scratch Foundation — https://scratchfoundation.org/learn/for-educators
