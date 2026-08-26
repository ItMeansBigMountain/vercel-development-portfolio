# RuneLite Plugin Hub lifecycle + hiscores fallback notes

## OSRS plugin workspace lifecycle folders

Use these class-level buckets under `/opt/data/HeRmEz/projects/osrs-plugins/`, alongside `_templates/`:

- `completed/` — only for plugins whose official `runelite/plugin-hub` PR has been approved/merged and the plugin is shareable through the official RuneLite Plugin Hub.
- `pr-review-pending/` — for plugins that are locally complete and ready for, or already waiting on, official Plugin Hub submission/review.
- `in-progress/` — active plugins still being built, consolidated, tested, or polished.

When moving plugin repos between these folders, treat them as submodules/worktrees:

1. Move with `git mv` from the HeRmEz parent repo so gitlinks are renamed correctly.
2. Update `.gitmodules` paths in the same parent commit.
3. Keep a README in each lifecycle folder so empty buckets remain documented/tracked.
4. Re-run a targeted build from the plugin's new path.
5. Verify `git submodule status -- <new-path>` and that a fresh clone path will match the new layout.
6. Push the parent repo and verify remote `main` equals local `HEAD`.

## Plugin Hub submission checklist

Official Plugin Hub flow from RuneLite docs:

1. Plugin repo must be public.
2. Verify Java 11-compatible build and passing tests.
3. Fill `runelite-plugin.properties`, especially `displayName`, `author`, `description`, `tags`, `plugins=<fqcn>`, optional `version`, and `build=standard`.
4. Include a useful README. For plugins sending player names to WOM/Temple/official hiscores, explicitly disclose third-party data/API use.
5. Optional root `icon.png`, max 48x72 px.
6. Push the plugin repo and record the full 40-character commit hash.
7. Fork/clone `runelite/plugin-hub`.
8. Add one manifest under `plugins/`:

```properties
repository=https://github.com/<owner>/<plugin-repo>.git
commit=<40-character commit hash>
```

9. Open PR against `runelite/plugin-hub` and handle CI/reviewer feedback.
10. Only after merge/availability on official Plugin Hub should the project move to `completed/`.

## Who's Grinding-style tracker fallback pattern

For selected-period grinding summaries:

1. Use Wise Old Man gained data first because it has real period gains.
2. If WOM fails or has no useful gains, fetch official OSRS hiscores current totals.
3. Store a local snapshot under the user's RuneLite/user cache (e.g. `~/.runelite/whos-grinding-hiscores/<player>.csv`).
4. Compare current official totals against the closest old local snapshot for the chosen period.
5. If no old snapshot exists, save baseline and show a clear baseline-needed message. Never fabricate gains.
6. Snapshot comparison can cover skills XP, boss KC, and activity/minigame score if the official `index_lite` rows are parsed beyond skills.

Useful user-facing baseline copy for narrow RuneLite cards:

```text
Official hiscores
baseline saved.
Gains show after
the next scan for
this period.
```

Pitfalls:

- Official OSRS hiscores expose current totals, not historical gains; the historical part is the local snapshot cache.
- The official hiscores snapshot and local cache are the same failover idea in two phases: fetch current totals, then compare to saved totals.
- Do not collapse WOM and official hiscores into one vague “tracker” source in the UI; keep internal source semantics clear even if the card stays concise.
- Avoid polling every visible social member; keep click-to-fetch, explicit refresh, and caching behavior for third-party lookups.
