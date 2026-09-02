# Coding School Curriculum Source of Truth

Last updated: 2026-08-29

## Purpose

This is the canonical curriculum and product-scope spine for the Coding School Platform / Algorithm Academy. It reconciles:

- `AI_ERA_CODING_CURRICULUM.md` — AI-era student philosophy and first 12-week track.
- `LINEAR_SEARCH_TREASURE_HUNT_WORKSHEET.md` — first worksheet format and algorithm lesson style.
- `curriculum/source-algos/BASIC_13_DESCRIPTIONS.txt` — Basic 13 foundations.
- `legacy-src/coders-school/repls/algos/basic13.py` — legacy Python Basic 13 examples.
- `CODERSCHOOL_CRM_RESEARCH_AND_PLAN.md` and `docs/plans/2026-05-26-coding-school-crm.md` — CRM/progress/teacher workflow direction.
- `TEACHER_HIRING_LOCATION_PLAN.md` — teacher role expectations and child-safety dependencies.

The next implementation card should treat this file as product source of truth before adding curriculum, progress, teacher, parent, or student workflows.

## Product promise

A child-safe learning portal where teachers master the curriculum first, then guide students through coding fundamentals, algorithmic thinking, debugging, responsible AI-assisted coding, and portfolio projects. Progress is earned through runnable work, teacher-reviewed evidence, and plain-English accomplishment feedback.

## Non-negotiable principles

1. Teacher mastery comes before student lessons.
2. Students earn progress from evidence, not passive page views.
3. Every lesson uses a small loop: read, predict, run, debug, extend, reflect.
4. AI is a coach, not an answer vending machine.
5. No real student data belongs in the demo; use fixtures only.
6. Parent views translate technical work into wins, gaps, confidence, and next steps.
7. Teacher/admin tools must make check-ins faster, not create more paperwork.

## Teacher mastery track first

Before a teacher can lead Algorithm Academy lessons, the platform should help them prove mastery of the teaching system. This track should be implemented before learner-facing automation.

### Teacher Level T0 — Platform and safety onboarding

Goal: teacher can use the portal safely with minors and demo data.

Teacher must demonstrate:

- Navigate teacher schedule and open a student session.
- Explain the no-real-student-data demo rule.
- Use parent-safe language in notes.
- Avoid secrets, addresses, private school details, account tokens, and personal contact info in AI prompts.
- Know when not to use AI: sensitive student issues, behavior/private family details, credentials, or unsupported legal/medical claims.

Evidence artifacts:

- Completed child-safe note-writing checklist.
- Sample parent note rewritten from a too-technical teacher note.
- AI prompt safety quiz passed.

### Teacher Level T1 — Basic 13 coaching mastery

Goal: teacher can teach loops, counters, arrays/lists, aggregation, mutation, and index/value distinction.

Teacher must demonstrate:

- Explain each Basic 13 challenge in plain language.
- Predict outputs before running code.
- Trace loop variables and array indexes by hand.
- Spot common beginner bugs: off-by-one ranges, wrong accumulator start, returning value instead of index, mutating the wrong slot.
- Convert a Basic 13 task into a student-friendly mini mission.

Evidence artifacts:

- Annotated Basic 13 solution notes.
- One broken Basic 13 exercise plus answer key.
- One student remediation plan for loops/lists confusion.

### Teacher Level T2 — Algorithm Academy coaching mastery

Goal: teacher can teach algorithms as strategies, not memorized solutions.

Teacher must demonstrate:

- Run the Linear Search Treasure Hunt format end to end.
- Compare linear search and binary search using human analogies.
- Teach sort concepts with cards/visual swaps before code.
- Ask students to reason about time/steps without formal Big-O pressure for younger learners.
- Coach a student from trace table to runnable function to challenge extension.

Evidence artifacts:

- Linear search lesson facilitation notes.
- One original algorithm mission card.
- Student misconception map for search/sort lessons.

### Teacher Level T3 — Debugging and learning-to-learn mastery

Goal: teacher can coach students through frustration productively.

Teacher must demonstrate:

- Teach bugs as evidence, not failure.
- Use the debugging loop: reproduce, read error, isolate, change one thing, rerun, reflect.
- Help students document what they tried.
- Use hints before answers.
- Assess whether a student understands code they copied or generated.

Evidence artifacts:

- Debugging transcript for a broken mini program.
- Two hint ladders: one for syntax bugs, one for logic bugs.
- Reflection rubric for “I thought __, but the computer did __.”

### Teacher Level T4 — Child-safe AI coding mastery

Goal: teacher can guide AI use without letting it replace thinking.

Teacher must demonstrate:

- Prompt AI for hints, explanations, test cases, and refactoring suggestions.
- Require students to explain AI code in their own words.
- Verify AI answers by running code and checking expected behavior.
- Redact private data and secrets before using AI.
- Identify when AI gives plausible but wrong explanations.

Evidence artifacts:

- AI critique worksheet using an algorithm explanation.
- Before/after AI-assisted bug fix with tests or manual checks.
- Student AI-use agreement in kid-friendly language.

### Teacher Level T5 — Portfolio project coaching mastery

Goal: teacher can help students scope, ship, and present real projects.

Teacher must demonstrate:

- Break a student idea into milestones.
- Keep the first version small and runnable.
- Track evidence: commits, screenshots, live links, tests, demo scripts, reflection notes.
- Coach demos: what it does, how it works, what was hard, what comes next.
- Convert project work into parent-facing progress.

Evidence artifacts:

- One project plan with milestones and risks.
- One review rubric for games, web apps, data apps, or bots.
- One portfolio narrative template.

## Student progression spine

The student track starts only after the teacher track has content/rubrics to support it.

### Stage 0 — Creative sequencing

Best for: ages 6-8 or true beginners.

Core skills:

- Commands, sequence, cause/effect, patterns.
- Scratch-style movement, sprites, mazes, and animation loops.
- Bug language: “the instruction did exactly what we said, not what we meant.”

Accomplishment loop:

- Complete one movement puzzle.
- Explain the sequence aloud.
- Fix one intentionally wrong instruction.
- Earn `Sequence Starter` badge.

### Stage 1 — Python/Scratch fundamentals

Best for: ages 8-10 and older beginners.

Core skills:

- Variables, inputs/outputs, conditions, loops, lists.
- Small games: clicker, quiz, door/key, multiplication trainer, inventory.
- First functions as reusable actions.

Accomplishment loop:

- Finish a runnable mini program.
- Pass a short prediction check.
- Fix one bug.
- Add one feature.
- Earn skill badges such as `Loop Builder`, `Condition Captain`, `List Explorer`.

### Stage 2 — Basic 13 foundations

Best for: students ready to reason through arrays/lists and loops.

Canonical Basic 13 sequence reconciled with the authenticated Algorithm Academy Drive sync:

1. Print 1-255.
2. Odd numbers.
3. Running sum.
4. Traverse array.
5. Max.
6. Average.
7. Odd-number array.
8. Count above Y.
9. Square values.
10. Replace negatives.
11. Min/max/avg.
12. Shift values.
13. Replace negatives with Dojo.

Mastery definition:

- Student can trace the loop.
- Student can name input, process, output.
- Student can predict at least one intermediate value.
- Student can explain whether the task reads, aggregates, filters, or mutates data.
- Student can solve a near-transfer version with different numbers.

Accomplishment loop:

- `Read` existing code.
- `Predict` output or final list.
- `Run` and compare.
- `Fix` a seeded bug.
- `Challenge` with a new rule.
- `Reflect` in one sentence.

### Stage 3 — Algorithm Academy foundations

Best for: students who can handle lists, functions, and trace tables.

Initial modules:

- Linear search: check every item; index vs value.
- Binary search: sorted data and halving the search space.
- Bubble sort: repeated neighbor swaps.
- Insertion sort: sorting cards in hand.
- Merge sort: divide, solve, combine.
- Factorial/recursion: smaller versions of the same problem.
- Linked lists: nodes as treasure-map clues.

Mastery definition:

- Student can explain the strategy without code.
- Student can trace it on paper.
- Student can run a starter implementation.
- Student can modify the implementation safely.
- Student can compare when one strategy is better than another.

Accomplishment loop:

- Earn mission badges, Codewars/SoloLearn-style, from verified tasks:
  - `Trace Passed`
  - `Bug Fixed`
  - `Variation Solved`
  - `Explanation Approved`
  - `Challenge Extension`
- Unlock next mission after teacher-reviewed evidence, not just clicking next.

### Stage 4 — Documentation and debugging fluency

Best for: students building larger programs.

Core skills:

- Read filenames/comments first.
- Identify inputs, outputs, state, and side effects.
- Write clear variable names and comments.
- Keep a debug journal.
- Use print/log statements and small tests.
- Explain expected vs actual behavior.

Mastery definition:

- Student can receive unfamiliar code and make a safe change.
- Student can document a function in one paragraph.
- Student can write a minimal bug report.
- Student can reproduce and fix a seeded bug.

Accomplishment loop:

- `Doc Detective` badge for explaining unfamiliar code.
- `Bug Hunter` badge for reproducing and fixing a bug.
- `Test Pilot` badge for adding examples/checks.

### Stage 5 — Child-safe AI-assisted coding

Best for: students who can already read and run code.

Core skills:

- Ask AI for hints before answers.
- Ask for examples, edge cases, and explanations.
- Never share private information, tokens, addresses, school details, or real account data.
- Run and inspect AI code before trusting it.
- Compare AI output with teacher rubric.

Mastery definition:

- Student can explain what AI generated.
- Student can identify one limitation or risk in the AI answer.
- Student can test the AI suggestion.
- Student can revise the prompt to ask for a better learning-focused hint.

Accomplishment loop:

- `AI Skeptic` badge for finding a flawed explanation.
- `Prompt Helper` badge for improving a prompt.
- `Verified Fix` badge for testing an AI-suggested change.

### Stage 6 — Portfolio projects

Best for: students ready to combine multiple skills.

Tracks:

- Games: quiz, dodge, platformer logic, snake-style remake.
- Web: personal page, project gallery, leaderboard.
- Data: survey charts, sports stats, public sample-data dashboards.
- Bots/automation: reminders, file organization, safe Discord-style command demos.
- Creative AI: prompt-and-verify tools, not unsupervised chatbots for minors.

Mastery definition:

- Student ships a runnable artifact.
- Student can demo the project.
- Student can explain code structure.
- Student documents known bugs and next improvements.
- Teacher converts project evidence into progress events and parent-safe summary.

Accomplishment loop:

- Milestone badges: `Idea Scoped`, `First Run`, `Core Feature`, `Bug Fixed`, `Demo Ready`, `Reflection Complete`.
- Portfolio card stores title, description, skills, screenshots/link, teacher review, student reflection, and next iteration.

## Algorithm Academy MVP scope

### In scope for the first implementation slice

1. Source-of-truth curriculum data from this document.
2. Teacher mastery modules T0-T2 with rubrics and evidence items.
3. Student Basic 13 module list with accomplishment requirements.
4. Linear Search Treasure Hunt as the first algorithm lesson.
5. Progress/accomplishment engine that supports:
   - badge id
   - evidence type
   - teacher review status
   - concept tags
   - mastery level
   - parent-safe summary
6. Teacher check-in flow connected to curriculum tags.
7. Parent dashboard showing wins/gaps/next steps in plain English.

### Explicitly out of scope for the first slice

- Real billing.
- Real student production data.
- Public social features or student-to-student messaging.
- Ungated AI calls.
- Fully automated grading without teacher review.
- Large LMS features before teacher check-in and progress evidence are working.

## Implementation model for curriculum data

Represent every curriculum item as structured data rather than hardcoded page text.

Recommended fields:

```text
id
track: teacher | student
stage
module
lesson
ageBand
conceptTags
skillTags
prerequisites
studentFacingGoal
teacherFacingGoal
readPredictRunFixChallengePrompt
rubric
badges
safeAiPolicy
portfolioEvidence
parentSummaryTemplate
sourceFiles
```

Teacher mastery records should be first-class data:

```text
teacherId
masteryLevel
moduleId
evidenceArtifacts
reviewStatus
reviewedBy
reviewedAt
notes
```

Student accomplishment records should distinguish completion from mastery:

```text
studentId
lessonId
badgeId
evidenceText
artifactUrlOrPath
teacherReviewStatus
masteryLevel: introduced | practicing | developing | proficient | mentor-ready
confidenceScore
createdAt
```

## Progress taxonomy

Use these tag families consistently across teacher notes, student work, badges, and parent summaries.

### Concept tags

- sequence
- variables
- conditions
- loops
- lists
- functions
- indexing
- aggregation
- filtering
- mutation
- search
- sorting
- recursion
- data-structures
- APIs
- files
- web
- games
- AI-assisted-coding

### Skill tags

- reading-code
- predicting-output
- tracing
- debugging
- documentation
- problem-decomposition
- testing
- explaining-code
- safe-AI-use
- portfolio-demo

### Evidence types

- worksheet-response
- runnable-code
- trace-table
- bug-fix
- teacher-observation
- AI-critique
- project-link
- screenshot
- demo-script
- reflection

### Mastery levels

- `introduced` — saw it with teacher support.
- `practicing` — can complete guided steps.
- `developing` — can solve variations with hints.
- `proficient` — can solve and explain independently.
- `mentor-ready` — can help another student or create a new challenge.

## Required user journeys

### Teacher journey

1. Teacher logs in or demo-switches role.
2. Teacher sees today’s assigned sessions.
3. Teacher opens a session.
4. Teacher selects curriculum module/lesson or tags it manually.
5. Teacher records notes, confidence, blockers, homework, and evidence.
6. Teacher reviews any AI/local parser suggestions.
7. Teacher saves progress/accomplishment events.
8. Teacher sees what unlocked next for the student.

### Student journey

1. Student sees current mission, prerequisites, and why it matters.
2. Student completes read/predict/run/fix/challenge/reflection steps.
3. Student submits evidence or the teacher records evidence during class.
4. Student sees badges/accomplishments after teacher review.
5. Student sees the next recommended mission.
6. Student builds toward a portfolio project.

### Parent journey

1. Parent sees a weekly win.
2. Parent sees current concepts in plain English.
3. Parent sees confidence trend and blocker/next step.
4. Parent sees the current project or portfolio milestone.
5. Parent sees teacher notes without overwhelming implementation details.

### Admin journey

1. Admin sees teachers with incomplete mastery onboarding.
2. Admin sees missing lesson check-ins.
3. Admin sees students without recent evidence.
4. Admin sees curriculum modules with weak outcomes.
5. Admin exports parent-safe progress reports.

## Acceptance gates for the next implementation card

The downstream implementation card (`t_aac0495d`) should be considered complete only when it can show:

1. Teacher mastery track appears before student track in navigation/data.
2. Basic 13 and Linear Search are represented as runnable/demoable curriculum items.
3. A teacher can record evidence against a curriculum item.
4. The accomplishment/badge system differentiates attempted, completed, teacher-reviewed, and mastered.
5. Parent dashboard uses progress evidence to render at least one weekly win and one next step.
6. AI-assisted features are gated, review-first, and safe-by-default with local fallback.
7. Tests or deterministic checks prove curriculum data integrity and progress event links.

## Open product choices for later

These should not block the first implementation slice:

- Whether the public brand is `Coding School Platform`, `Codology`, or `Algorithm Academy`.
- Whether teacher mastery badges are visible to parents.
- Whether students can self-submit code artifacts before account/auth is production-ready.
- Whether Codewars/SoloLearn-style progress becomes points, streaks, levels, or all three.
- Whether lesson content ships as markdown, JSON, MDX, or database-seeded fixtures.
