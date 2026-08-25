# Plan-only app reframes for Vercel demos

Use this when a folder in `/opt/data/HeRmEz/projects` is only a README/SCOPE/PROJECT scaffold and the user changes the product direction midstream.

## Pattern

1. Treat the user's latest product direction as authoritative. Do not preserve the old concept in the UI just because the folder name or imported scope says so.
2. Rename the project directory if the old folder name is misleading and no external deployment link depends on it yet.
3. Build the smallest static Vercel-ready MVP first when the product can be reviewed without auth/backends/databases.
4. Update all three project-local docs after the reframe:
   - `README.md` — what it is now, commands, constraints.
   - `SCOPE.md` — new MVP goal/features/constraints/next steps.
   - `PROJECT.md` — reframe note, path, primary next action.
5. Update workspace trackers immediately:
   - `/opt/data/HeRmEz/projects/README.md`
   - `/opt/data/HeRmEz/projects/VERCEL_TRIAGE.md`
   - `/opt/data/HeRmEz/projects/WORK_QUEUE.md` if present.
6. Verify after any rename from the new path: install/build/preview and any public API probe needed for the MVP.

## Good MVP choices

- Prefer public/no-key APIs and browser-only logic for first review loops.
- For scanner/search/aggregator concepts, combine upload/manual correction with external source links rather than overbuilding a backend first.
- If using browser OCR, label it as assistive and keep manual correction visible.
- For market-price apps, distinguish numeric source prices from reality-check links such as eBay sold comps; do not present a single price as truth.

## Pitfalls

- Do not leave stale README/SCOPE content that describes the abandoned concept.
- Do not keep an old product name in trackers after a reframe; it causes the next session to resurrect the wrong idea.
- Do not add accounts, inventory storage, or paid API keys before the user has reviewed the core demo flow.
- Do not encode missing Vercel credentials as a durable limitation; just record that deployment is pending auth for the current workspace state.
