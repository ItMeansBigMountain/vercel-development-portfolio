# HeRmEz Portfolio Roadmapping Example — May 2026

This reference captures a reusable pattern from a session where the user actively reshaped a large workspace of legacy apps.

## Actions performed

- Removed an obsolete project (`bitcoin-bike-startup`) after explicit user instruction.
- Updated workspace trackers after removal: project review sheet, CSV, deployment URL list, and README.
- Imported algorithm/example candidates for Codology from all `algos` remote branches, not only default branch.
- Wrote merge/product direction docs for overlapping projects:
  - `journal-ai` absorbs `sleep-dream-app`.
  - `MusicAI` absorbs `music-mood-app`.
  - `social-media-analysis` absorbs `tweetBetweenTheLines` and `twitter-therapy-app`.
- Created direction docs for data science notebooks, meeting transcription, networking/pentesting lab, Policy Pit, RTS chat rooms, and data-freedom concepts.
- Reviewed an existing `az204` Function App lab before scaffolding a new `robinhood-daily-portfolio-report` repo.
- Added nested standalone repos to the parent workspace `.gitignore` so the parent repo does not swallow child Git history.

## Reusable patterns

### Project retirement

1. Confirm the user explicitly wants removal.
2. Remove folder from git/workspace.
3. Remove stale rows from all trackers.
4. Commit deletion with tracker edits in the same commit.

### Project merge/consolidation

1. Choose the primary surviving app.
2. Add `PRODUCT_DIRECTION.md` to the primary app.
3. Add `MERGE_INTO_<TARGET>.md` to each absorbed app.
4. Update trackers so future inventory reports say “merge source/archive,” not “needs triage.”

### New repo after source review

1. Inspect the reference repo/source first.
2. Document reusable source ideas in the new repo.
3. Scaffold a minimal runnable/tested baseline.
4. Initialize, commit, create/push remote.
5. Add nested repo to parent `.gitignore` if it lives under a larger workspace.

## Product safety notes from this session

- Social-media analysis and Twitter-therapy-style features should use non-diagnostic language: “stress markers,” “negative language increased,” “communication style shifted,” not clinical diagnoses.
- Portfolio/news projects should say they explain possible relevance and uncertainty, not investment advice.
- Pentesting/networking projects should emphasize authorized own-device/lab testing, detection, reporting, and remediation.
