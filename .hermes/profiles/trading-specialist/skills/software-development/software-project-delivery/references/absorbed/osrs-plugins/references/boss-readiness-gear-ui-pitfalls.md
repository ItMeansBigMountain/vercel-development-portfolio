# Boss Readiness gear/UI pitfalls

Use this when maintaining BossReadinessScore-style RuneLite side panels and gear recommendation engines.

## Gear recommendation accuracy

- Treat live gear APIs as helpful but incomplete. Merge live/API items with a local OSRS-backed fallback list instead of letting live data fully replace local data. This protects against stale APIs missing current OSRS megarares or newer gear.
- When merging live/API items with local fallback items, let the curated local OSRS-backed row override a same-name live row. Live rows may be missing durable metadata such as `twoHanded`, may be stale/mis-scored, or may include odd source notes/icons; use live data as additive, not authoritative.
- Filter temporary/minigame-only gear before it enters recommendation candidates. In particular, exclude Corrupted Gauntlet/Gauntlet placeholders such as `corrupted ...`, `attuned ...`, `perfected ...`, `basic bow/staff/halberd`, and names/forms containing `(perfected)`, `(attuned)`, `(basic)`, or Gauntlet markers. The user does not want corrupted gauntlet or other minigame-specific items recommended for general boss setups.
- Explicitly include/test high-end OSRS weapons in local fallback data, especially:
  - `tumeken's shadow`
  - `twisted bow`
  - `scythe of vitur`
  - `bow of faerdhinen`
  - `toxic blowpipe`
  - current high-end melee options such as `osmumten's fang` and `noxious halberd`
- Add regression tests asserting fallback item IDs for high-value items and asserting stale live data still gets filled by local fallback items.
- Keep OSRS-only source hygiene: generated wiki links must start with `https://oldschool.runescape.wiki/w/`; never use RuneScape 3 wiki/data for OSRS plugin item pages.

## Two-handed weapon behavior

- Model whether a weapon is two-handed on the gear item or item metadata layer.
- When a selected weapon is two-handed, remove/omit the shield slot from the selected setup and its alternatives. Do not recommend a shield alongside Shadow/Tbow/Bowfa/Blowpipe/Scythe/halberds.
- In equipment panels with slot-cycling arrows, compute shield suppression from the currently displayed/cycled weapon alternative, not only from the recommendation's initially selected weapon. Otherwise cycling to a 2H weapon can still leave a shield visible.
- In the equipment panel, render the shield cell as a disabled/blank explanation such as `2H weapon` rather than showing an unrelated shield.
- Add tests that a two-handed recommended weapon causes `GearSlot.SHIELD` to be absent, and tests that stale live/API data plus minigame-only rows still yields OSRS megarares such as Shadow/Tbow from local fallback.

## RuneLite sidebar compactness

- Verify the post-analysis state, not just the empty controls state. Summary titles, boss names, status lines, and equipment cells can widen the panel after analysis.
- Wrap all title/summary labels in fixed-width HTML divs, not just muted body text.
- Use sidebar-safe constants for narrow panels: cap content width, combo boxes, buttons, radio labels, grid wrappers, equipment cells, and tiny cycle buttons.
- Shorten labels in cramped controls (`Mag`, `Rng`, `Mel`) and compact long item names before rendering.
- Never rely on `setHorizontalScrollBarPolicy(HORIZONTAL_SCROLLBAR_NEVER)` alone; oversized child preferred sizes can still make the sidebar appear to drag right or clip.

## Parent/submodule commit hygiene

- Commit and push the child plugin repo first.
- In the parent workspace, stage only the submodule pointer (`git add projects/osrs-plugins/<PluginName>`). Use `git status --short --untracked-files=no` before committing.
- If a parent push is rejected because unrelated backup/cache files were already committed ahead of origin, reset the parent back to `origin/main`, then recommit only the submodule pointer. Do not push `.hermes`, Gradle caches, JDK tarballs, or backup artifacts as part of a plugin pointer update.
