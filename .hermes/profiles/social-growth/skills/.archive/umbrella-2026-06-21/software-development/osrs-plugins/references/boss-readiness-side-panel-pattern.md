# Boss readiness side-panel + gear engine pattern

Use this when implementing or extending RuneLite plugins that need a persistent right-side dashboard with recommendations rather than one-off chat messages.

## Why this pattern exists

The user wants Boss Readiness Score to feel like a simplified in-client GearScape: select a boss/style/budget, then see readiness, recommended gear, alternatives, and missing requirements in a RuneLite side panel. Treat chat messages as secondary summaries only.

## Model classes that worked well

Create small Java DTO/enums before wiring UI:

- `CombatStyle`: `STAB`, `SLASH`, `CRUSH`, `RANGED`, `MAGIC`, `AUTO`.
- `BudgetTier`: budget caps such as `BUDGET`, `MIDGAME`, `RICH`, `NO_LIMIT`.
- `GearSlot`: OSRS equipment slots.
- `BossProfile`: boss label plus target/mechanic assumptions.
- `PlayerStats`: Attack, Strength, Defence, Ranged, Magic, Hitpoints, Prayer.
- `GearItem`: item id/name, slot, combat bonuses, requirements, price, style tags, and optional embedded icon data such as `iconBase64`. Keep an explicit RuneLite/OSRS item id on each item so side panels can render `ItemManager` sprites; for live data, check common id fields such as `item_id`, `osrs_id`, then `id`, preserve any API-provided base64 item icon, and give fallback fixture gear known-good item ids.
- `SetupRecommendation`: score, estimated DPS, hit chance, max hit, warnings, and selected items.

Keep the first implementation testable with a local high-impact item dataset; later replace/expand it with generated OSRS Wiki/RuneLite JSON resources.

## Recommendation engine approach

Start with a deterministic local `GearRecommendationEngine`:

1. Read current player skill levels from RuneLite client state.
2. Filter gear by level requirements, style compatibility, budget tier, and slot legality.
3. Score candidate setups with a DPS-ish heuristic: offensive bonuses, max-hit proxy, hit chance proxy, weapon/style relevance, and boss-specific target-pressure multipliers.
4. For `AUTO`, evaluate styles and choose the highest-scoring setup.
5. Return both style alternatives and per-slot item alternatives. The panel needs per-slot ordered lists so the `<`/`>` controls can cycle through second-best, third-best, etc. without recomputing.
6. Treat `MELEE` as a high-level user choice and map/display it to the best concrete melee weakness (`STAB`, `SLASH`, or `CRUSH`) after target defences are known.

Avoid relying on GearScape private runtime endpoints. Use GearScape research only as UX/algorithm inspiration unless stable public API terms are published. GearScape/Wiki fetches must degrade gracefully: seed a useful local fallback boss list before network refresh so the dropdown is not empty or sparse while APIs are still loading/offline.

## RuneLite side-panel integration

A working panel integration uses:

- `ClientToolbar` and a `NavigationButton` in the plugin startup/shutdown lifecycle. Prefer a packaged resource icon over drawing a placeholder in code: put the PNG under `src/main/resources/<package>/icon.png`, load it with `PluginClass.class.getResourceAsStream("icon.png")` + `ImageIO.read`, and keep a tiny generated fallback so toolbar startup never breaks. For this user's boss/readiness-style plugins, a readable OSRS-like pixel-art icon is preferred over flat placeholder letters.
- A Swing panel class (for example `BossReadinessScorePanel`) that renders readiness score, selected boss/style/budget, recommended items by slot, warnings, and alternative style DPS.
- Keep Boss Readiness settings minimal: avoid putting boss/style controls in RuneLite config. Boss selection, combat-style choice, and Analyze action belong in the side panel.
- Do not send routine chat messages for this plugin. The user expects the plugin's work to live in the side panel, not chat.
- Side-panel UX target: boss dropdown/search at top, compact Auto/Mage/Range/Melee controls, a RuneLite equipment-layout grid, per-slot left/right arrows for cycling second/third-best items, then a prominent Analyze button.
- RuneLite sidebar space is narrow: avoid wide strings and multi-column controls that force horizontal expansion. Use short labels (`None`, `Mage`, `Range`, `Melee`), small padding, no horizontal scroll bar, compact item names, and equipment cells around 60-70 px wide so the panel fits from the sides.
- Center equipment-layout grids explicitly. Do not add a `GridBagLayout` equipment panel directly to a `BoxLayout.Y_AXIS` content panel with `LEFT_ALIGNMENT`; wrap the grid in an opaque-false `JPanel(new GridBagLayout())`, set the wrapper to `Component.CENTER_ALIGNMENT`, cap wrapper width to the panel text width, then add the grid inside with default `GridBagConstraints`. If the right column clips or the grid looks left-biased, shrink cells/buttons before widening the panel (for example 60x54 cells, 10 px arrow buttons, 22 px icons).
- Equipment slots should show actual OSRS item images, not just text. When a live gear API response includes an embedded item icon (for example a base64 PNG from GearScape), store it on the DTO and apply it directly to the slot label before falling back to RuneLite sprites. This avoids blank labels when live API items do not map cleanly to a static RuneLite item id or when async sprite loading lags.
- Inject `ItemManager`, pass an item-image provider into the Swing panel, and keep a `?`/dash fallback when an item id is missing. **Important:** `ItemManager#getImage(...)` returns RuneLite `AsyncBufferedImage`; do not treat it as a normal `BufferedImage` and manually scale it, because labels can stay blank before the async sprite load completes. Type the provider as `Function<GearItem, AsyncBufferedImage>` or equivalent and call `asyncImage.addTo(jLabel)` after sizing the label/cell. Give icon cells enough vertical room (about 60x68 with a 32px icon) so sprites and compact item text both remain visible in the sidebar.
- For external gear data, normalize item-name fallback lookups with `toLowerCase(Locale.ROOT)` and add name-based fallback ids for high-value items observed in live responses when API id fields are absent or ambiguous. Keep these fallbacks small and covered by focused unit tests rather than treating them as the primary item database.
- Include a `None`/best-overall boss option: when no boss is selected, recommend the strongest wearable gear for the player's stats; when a boss is selected, bias ranking toward the boss weakness/defensive profile.
- Config can still carry durable/simple preferences such as budget tier, but keep tactical boss/style state inside the panel unless persistence is explicitly requested.
- `@Subscribe ConfigChanged` handler that refreshes the panel when relevant config keys change.
- Logged-out and partial-data states instead of failing silently.

## Verification loop

For this user's OSRS plugin repos, verify before pushing:

```bash
JAVA_HOME=/opt/data/jdks/current-java11 ./gradlew test --no-daemon -q
JAVA_HOME=/opt/data/jdks/current-java11 ./gradlew assemble --no-daemon -q
```

Add focused unit tests for the engine, especially:

- best affordable gear for selected boss/style/stats
- blocking items when requirements are missing
- `AUTO` choosing the expected style for representative bosses

If a boss-specific tuning change is made, test the scenario that motivated it (for example Zulrah's magic/ranged bias).