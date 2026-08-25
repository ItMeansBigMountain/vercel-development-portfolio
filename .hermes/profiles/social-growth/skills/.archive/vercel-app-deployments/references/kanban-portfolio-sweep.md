# Kanban portfolio sweep for Vercel/project review

Use this pattern when the user asks to review every project in a workspace, test unfinished work, deploy/redeploy apps on Vercel, and browser-smoke-test them continuously with agents.

## Durable setup pattern

1. Inventory the workspace projects and classify each top-level folder as one of:
   - live app / Vercel frontend candidate,
   - app scaffold,
   - backend/API candidate,
   - plan-only MVP/review-shell candidate,
   - script/archive/classification-needed.
2. Create a workspace tracker such as `KANBAN_PROJECT_REVIEW_PBIS.md` listing every project, classification seed, assignee seed, and acceptance criteria.
3. Seed one Kanban PBI per project. Each PBI should require:
   - source/README/product-direction/tracker inspection,
   - local build/test using least-destructive commands,
   - Vercel deploy/redeploy when appropriate,
   - anonymous HTTP verification,
   - browser smoke testing by clicking through the live UI and checking console errors,
   - child fix PBIs for unfinished/broken work,
   - tracker updates (`README.md`, `WORK_QUEUE.md`, `VERCEL_TRIAGE.md`, project-local notes).
4. Create one controller card to promote/decompose project PBIs in small batches rather than stampeding the board.
5. Add a silent dispatcher-nudge cron/script if the gateway dispatcher may not keep up. The script should run `hermes kanban dispatch --max <small N> --json`, append output to a workspace log, and print nothing for routine ticks.
6. Commit the tracker and dispatcher script to the workspace repo, but ignore transient dispatch logs.

## Worker skill-loading pitfall

Kanban worker processes may not have the same skill namespace/config as the parent chat. If a worker exits with `Unknown skill(s): ...`, do not keep retrying the same card. Prefer one of:

- clear optional `--skill` preloads from the affected cards and embed the important instructions directly in the task body;
- use only skill names verified to be available to the worker profile;
- create a no-skill recovery controller card that reads the seeded PBIs and continues orchestration from the task bodies.

The durable lesson is not that a specific skill is broken; it is that bulk portfolio sweeps should be robust even when optional skill preloading differs across profiles.

## Suggested PBI acceptance criteria

For each project PBI, include:

- exact project path and classification seed;
- relevant markers (`package.json`, `vercel.json`, `requirements.txt`, `manage.py`, `pyproject.toml`, `README.md`, `PRODUCT_DIRECTION.md`);
- commands run and summarized results;
- deployment URL(s) and anonymous HTTP status;
- browser-smoke-test notes with issue evidence/screenshots when applicable;
- child fix PBIs created, or exact external blocker;
- tracker/docs files updated;
- explicit secret hygiene: never expose or commit `.env`, `.vercel`, tokens, credentials, `node_modules`, build outputs, local DBs, or logs.

## Concurrency guidance

Keep project sweeps incremental. Start with a controller plus a small batch of inspection/build tasks. Let dependencies promote deploy and browser-test tasks after local validation. This keeps Vercel/API/browser usage observable and avoids many agents editing shared trackers simultaneously.
