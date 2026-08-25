# HeRmEz Project Consolidation Patterns — 2026-05

Session-derived examples for managing a multi-project workspace where the user repeatedly clarifies project ownership, merges, retirements, and new repo direction.

## Project merge pattern

When the user says two apps are “the same project” or “can go together”:

1. Choose and document the active target app/codebase.
2. In the target project, create or update `PRODUCT_DIRECTION.md` with the unified vision, inputs, core flows, MVP screens, and safety boundaries.
3. In the source/archive project, create `MERGE_INTO_<TARGET>.md` explaining what to preserve and what not to migrate blindly.
4. Update project trackers (`PROJECT_REVIEW_SHEET.md`, `PROJECT_REVIEW_SHEET.csv`, workspace README/index, aggregate direction log).
5. Update durable memory only for stable identity/merge facts that will matter later.
6. Commit and push.

Concrete examples:

- `stockNews` + `wutHappened`: `stockNews` is active deployed codebase; `wutHappened` is merge/source archive for “what happened today?” portfolio-news framing and generated recap ideas.
- `social-media-analysis` + `tweetBetweenTheLines` + `twitter-therapy-app`: social-media-analysis is the target; source apps become import/analysis/reflection modules.
- `journal-ai` + `sleep-dream-app`: journal-ai absorbs dream analysis.
- `MusicAI` + `music-mood-app`: MusicAI absorbs mood/playlist emotion analysis.

## Project retirement pattern

When the user says a project is no longer needed:

- Remove the folder with git-aware deletion.
- Remove rows/links from trackers and URL inventories.
- Do not leave stale active-project rows that will confuse future portfolio scans.

Example: `bitcoin-bike-startup` was removed and trackers were cleaned.

## New standalone repo from workspace source

When the user asks to create a new repo after reviewing another repo:

- Inspect the source repo/lab first.
- Scaffold a minimal tested baseline.
- Publish as a standalone GitHub repo.
- Ignore the nested child worktree from the parent workspace unless intentionally submoduled/bundled.
- Update parent trackers separately.

Example: `robinhood-daily-portfolio-report` was created after reviewing `az204` Function App patterns.

## Research-backed product plan pattern

For competitor-inspired portals:

- Capture public source URLs and extracted feature claims in a research doc.
- Keep user-provided operational knowledge separate from public research.
- Replicate functional workflows, not proprietary names, copy, branding, or private implementation.
- Write the first vertical slice so future builders know where to start.

Example: coding-school CRM plan used public The Coder School/Pike13 pages plus user-provided teacher check-in workflow to define schedule → check-in → AI note tagging → progress graph → parent dashboard.
