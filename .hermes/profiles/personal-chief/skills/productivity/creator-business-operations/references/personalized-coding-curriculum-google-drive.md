# Personalized Coding Curriculum Launch via Google Workspace

Use this reference when turning the user's kids/teens coding tutoring into a concrete curriculum and customer-delivery system.

## Offer and Delivery Model

- Default to premium **1:1 instruction**. Optional **2:1** sessions are offered only at the instructor's discretion.
- Initial core audience: curious, motivated children and teens; a practical first cohort is ages 10–14.
- Position the offer around independent problem-solving, debugging, documentation literacy, responsible AI use, and showcase projects—not merely completing algorithms quickly.
- Avoid customer-facing language that frames students as "easy to teach." Describe them as curious, motivated, or challenge-oriented.

## Curriculum Spine

A strong first program is an eight-session JavaScript sequence built from Coding Dojo-style Basic 13 exercises:

1. Problem comprehension, inputs/outputs, examples, and pseudocode.
2. Loops, boundaries, counters, and running totals.
3. Array traversal, maximum, and average.
4. Filtering and counting.
5. Data transformation and mutation.
6. Tracking multiple values and shifting arrays.
7. Documentation reading and AI-as-coach practice.
8. Timed mastery check plus personalized showcase project.

Teach speed as pattern recognition + planning + debugging efficiency, never typing speed. Require the loop: understand → example → pseudocode → simplest correct implementation → normal/edge tests → debug → explain.

## Teacher-First Track

The user is learning before teaching. Build a parallel teacher packet with:

- straightforward solutions rather than code-golf;
- hand traces and test cases;
- common wrong solutions and likely student misconceptions;
- hints that do not reveal the answer;
- age-appropriate explanations;
- project connections;
- a mock lesson/rehearsal step.

The teacher should be able to explain state changes during each iteration and intentionally diagnose broken versions before delivering a lesson.

## Child-Friendly AI Standard

Use the **Explain–Test–Change** rule. A learner may keep AI-assisted code only if they can:

1. Explain the important parts in their own words.
2. Test normal and edge cases.
3. Change behavior or add a feature.

Encourage AI for hints, error explanations, test generation, documentation guidance, and Socratic questions. Reject answer-copying, unexplainable code, unverified output, private-data sharing, and bypassing class/platform rules.

## Google Drive Production Pattern

After explicit approval for Workspace writes:

1. Verify the exact Google profile, live identity, required scopes, and Drive access.
2. Search for an existing root folder first to avoid duplicates.
3. Create a private root folder with numbered sections such as Start Here, Teacher Bootcamp, Curriculum, Worksheets, Assessments, Projects, Marketing, Customer Delivery, and Operations.
4. Prefer native Google Docs for curriculum/worksheets/policies and Google Sheets for progress, session notes, and kata logs.
5. Create a separate customer-delivery folder; do not expose teacher solutions or internal operations.
6. Produce a designed flier as an actual visual artifact in addition to editable native flier copy.
7. Visually inspect the flier for clipping, overlap, contrast, and mobile legibility.
8. Verify by API read-back: root children, representative Doc body, Sheet range, flier metadata/parent, and expected account ownership.
9. Keep everything private by default. Ask separately before enabling anyone-with-link or customer-specific sharing.

## Minimum Launch Package

- Program overview
- Eight-session scope and sequence
- Teacher self-study roadmap
- Student Basic 13 workbook
- Teacher solutions/debugging guide
- Starting diagnostic and final mastery assessment
- Young-developer AI agreement
- Personalized showcase-project brief
- Parent-facing editable flier copy
- Designed promotional flier
- Student progress/session/kata tracker

## 1:1 and 2:1 Adaptation

For 1:1, personalize pacing, examples, interests, hints, practice, and the showcase project. Fast learners get alternate solutions and extensions; stuck learners get smaller examples and visual tracing.

For 2:1, rotate driver/navigator roles, require both students to predict before running code, compare approaches, and collect an individual explanation or test from each learner. Never allow one student to become the permanent driver or be labeled as the "smart one."

## Verification Checklist

- [ ] Teacher and student assets are separated.
- [ ] Core lessons include debugging, documentation, and AI judgment—not only solutions.
- [ ] Native Docs/Sheets were actually created and read back.
- [ ] Visual flier was rendered and inspected.
- [ ] Customer delivery remains private until sharing is explicitly approved.
- [ ] 1:1 is the default offer; 2:1 remains instructor-controlled.
