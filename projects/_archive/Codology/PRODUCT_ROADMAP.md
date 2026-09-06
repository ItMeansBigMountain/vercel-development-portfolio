# Codology Product Roadmap

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Turn Codology into a modern, fun, competitive coding-learning website inspired by Duolingo and SoloLearn, focused on coding concepts that transfer across Python, JavaScript, and future languages.

**Architecture:** Keep the current no-login demo flow for low friction, then add durable score/progress storage when competition needs to persist. Build the product around curriculum paths, bite-sized lessons, interactive coding challenges, XP/streaks, and leaderboards.

**Tech Stack:** Expo React Native Web frontend, Vercel static hosting, existing Node/Vercel API for highscores, future optional durable store for progress/leaderboards.

---

## Product Positioning

Codology should feel like:

- **Duolingo for coding habits:** short daily lessons, streaks, XP, levels, encouraging feedback.
- **SoloLearn for curriculum:** structured tracks, language examples, code reading, quiz practice, challenge explanations.
- **A game, not school:** fast rounds, bright visuals, progress bars, badges, rival scores, unlockable levels.

The emotional promise:

> “Learn how code thinks, then use that thinking in any language.”

The product should teach patterns that transfer between languages:

- loops
- variables
- conditionals
- arrays/lists
- functions
- objects/dictionaries
- debugging
- algorithms
- reading code
- writing code
- converting logic between Python and JavaScript

---

## Core Learning Loop

1. **Pick a path**
   - Beginner Logic
   - Basic 13
   - Arrays + Loops
   - Python Basics
   - JavaScript Basics
   - Web Basics

2. **Do a short lesson**
   - 3-7 minutes
   - one concept
   - friendly explanation
   - visual code card

3. **Answer interactive questions**
   - multiple choice
   - fill in missing code
   - predict output
   - reorder code blocks
   - spot the bug
   - translate Python ↔ JavaScript

4. **Get instant feedback**
   - correct answer highlight
   - kid-friendly explanation
   - “why this works” note
   - retry wrong answers

5. **Earn progress**
   - XP
   - streak
   - badges
   - lesson completion
   - leaderboard placement

6. **Compete**
   - daily leaderboard
   - weekly leaderboard
   - class/group leaderboard later
   - challenge friends later

---

## Curriculum Shape

### Track 1: Basic 13 Foundations

Already started. This should become the first complete course.

Units:

1. Counting with loops
2. Odd/even logic
3. Running totals
4. Arrays/lists
5. Maximum/minimum
6. Average
7. Building arrays
8. Squaring values
9. Filtering values
10. Replacing values
11. Combining max/min/average
12. Moving items in arrays
13. Replacing negative values

Each unit should include:

- Python example
- JavaScript example
- “explain it like I’m 10” paragraph
- quiz cards
- one final challenge

### Track 2: Code Thinking

Teaches concepts independent of language.

Lessons:

- What is a variable?
- What is a loop?
- What is a condition?
- What is an array/list?
- What is an index?
- What is a function?
- What is a return value?
- What is debugging?

### Track 3: Python Path

- print
- variables
- strings
- numbers
- lists
- loops
- if statements
- functions
- dictionaries

### Track 4: JavaScript Path

- console.log
- let/const
- strings
- numbers
- arrays
- loops
- if statements
- functions
- objects
- DOM/web intro later

### Track 5: Translation Challenges

The most unique part of Codology:

- “This Python code does X. Which JavaScript code matches it?”
- “This JavaScript loop prints odds. Which Python loop matches?”
- “Same logic, different syntax.”

This reinforces the idea that coding is mostly logic, not memorizing one language.

---

## Competitive Features

Start simple; avoid overbuilding.

### MVP Competition

- Score after each game
- Time taken
- Name entry after game
- Leaderboard sorted by score then fastest time

### Next Competition Layer

- XP per question
- Bonus XP for streaks
- Accuracy percentage
- “Perfect Round” badge
- “Fast Finisher” badge
- “Comeback” badge for improving score

### Later Competition Layer

- Daily challenge
- Weekly leaderboard
- Course-specific leaderboard
- Class codes / group leaderboards
- Friend challenges
- Ghost scores: “Beat Ava’s 22/26 in 3:12”

---

## Motivation System

Use psychology-driven UX:

- Progress bars make learning feel finite and winnable.
- Small wins after every question keep momentum.
- Streaks create habit.
- Badges create identity.
- Leaderboards create social comparison.
- Friendly feedback lowers fear of being wrong.
- Short lessons reduce overwhelm.

Tone should be:

- playful
- encouraging
- clear
- never condescending
- not school-ish

Example feedback:

- “Nice! You spotted the loop pattern.”
- “Almost — remember, range stops before the last number.”
- “Great debugging eye.”
- “That’s the same logic, just JavaScript syntax.”

---

## Website Structure

### Home Screen

Purpose: make the app feel like a game/course hub, not a single quiz.

Sections:

- Hero: “Learn coding logic like a game.”
- Current course card: “Basic 13 Foundations”
- Progress: “0/13 units complete” initially local/demo
- CTA: “Continue Learning”
- Secondary CTA: “View Leaderboard”
- Language chips: Python, JavaScript

### Course Map Screen

Duolingo-like path.

- Unit nodes 1-13
- Locked/unlocked visual states
- Completed checkmarks
- Current lesson highlight

### Lesson Screen

- Lesson title
- Short explanation
- Python/JS code cards
- “Start Challenge” button

### Challenge Screen

Current quiz behavior, upgraded:

- Code card visual
- Question
- Options
- Feedback after answer
- Continue button instead of automatic jump

### Results Screen

- Score
- Time
- XP earned
- Badge if earned
- Name input for leaderboard

### Leaderboard Screen

- Current leaderboard
- Best score callout
- Filter tabs later: Today / Week / All Time

---

## Implementation Plan

### Phase 1: Make Current Game Feel Like a Learning Product

1. Replace the start screen with a modern course hub.
2. Add a Basic 13 course map screen.
3. Split questions by Basic 13 unit instead of one long 26-question marathon.
4. Add feedback explanations after each answer.
5. Add XP and badges locally for the current session.
6. Polish mobile-first layout and colors.

### Phase 2: Add Real Curriculum Depth

1. Add lesson intro content for each Basic 13 unit.
2. Add question types beyond multiple choice:
   - predict output
   - choose matching code
   - spot the bug
   - fill missing line
3. Add Python ↔ JavaScript translation questions.
4. Add review mode for missed questions.

### Phase 3: Add Durable Competition

1. Add a durable score/progress store.
2. Keep name-only accounts at first, no password/login.
3. Store:
   - display name
   - best score
   - XP
   - streak count
   - completed units
4. Add daily/weekly leaderboards.

### Phase 4: Add Real Coding Interaction

1. Add simple code runner/sandbox later.
2. Start with safe client-side validation for small exercises.
3. Later support backend-run tests if needed.

---

## Next Recommended Build Step

Build **Phase 1: Course Hub + Course Map + Unit-based Basic 13 rounds**.

This is the best next step because it changes the feel from “single quiz” to “modern learning platform” without needing accounts or a database yet.

Acceptance criteria:

- User lands on a polished course hub.
- Basic 13 appears as a curriculum path.
- User can pick Unit 1-13.
- Each unit has Python + JavaScript practice cards.
- Results show XP-style reward language.
- Leaderboard still works.

---

## Open Product Decisions

These can be decided later; do not block Phase 1.

- Should users eventually have accounts, or only display names?
- Should this be for one classroom/group or public learners?
- Should the main target be kids, teens, bootcamp students, or all beginners?
- Should code execution be real, or mostly guided quizzes at first?
- Should Python and JavaScript be equal from the start, or should students choose a main language?
