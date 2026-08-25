# Coding School CRM / Portal Research Pattern — 2026-05

Session-specific reference from planning a coding-school CRM inspired by publicly visible The Coder School North Shore/Pike13 workflows plus user-provided experience.

## Public sources checked

- The Coder School North Shore location page: `https://www.thecoderschool.com/locations/northshore/`
- Client login destination from that page: `https://tcs-northshore.pike13.com/welcome`
- The Coder School Code Coaching page: `https://www.thecoderschool.com/code-coaching/`
- After-school coding classes page: `https://www.thecoderschool.com/after-school-coding-classes/`
- Pike13 public product page: `https://www.pike13.com/`

## Publicly advertised capabilities worth modeling functionally

- Code Coaching / individualized project-based teaching.
- Small-ratio coaching.
- Weekly notes to parents.
- Parent progress visibility.
- Custom progress tracking / points.
- Student accomplishment portal.
- Student roadmap/story.
- Skill assessments, app/project reviews, quizzes.
- Scheduling, attendance, reminders, billing, client communication, reporting, mobile staff/client access.

## User-provided operational workflow to encode

- Teacher logs in and sees assigned schedule/students.
- Teacher clicks scheduled student after class.
- Teacher records an after-class check-in.
- Keywords/tags from the check-in feed progress graphs.
- Graph shows what the student is learning and getting good at.
- With AI, teacher can paste/upload Zoom after-meeting notes and receive suggested tags, concepts, homework, blockers, confidence, and parent-ready notes.

## Durable implementation guidance

- Replicate functional patterns, not branding/copy/proprietary names.
- Create original names: Progress Points, Learning Journey, Lesson Notes, Project Reviews.
- Source-of-truth artifacts should include both research notes and implementation plan.
- First vertical slice: teacher login → schedule → student check-in → paste Zoom note → AI suggests tags → teacher reviews/saves → progress graph updates → parent dashboard summary.
- Include child-data privacy boundaries and human review before AI suggestions affect official records.
