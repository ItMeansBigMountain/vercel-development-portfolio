# BIS Loadouts README screenshot assets

Use when the user asks to add, rerun, or recreate README screenshots for the BIS Loadouts RuneLite plugin.

## What happened

Raw screenshot reuse and naive headless Swing rendering produced poor README assets:

- copied Discord screenshots were narrow/cropped and did not clearly explain the plugin flow;
- rendering `BisLoadoutsPanel` directly from a test produced mostly blank light-gray images because Swing components were not realized/laid out like a live RuneLite panel;
- cropping/upscaling the raw Swing output made text/icons visible but caused clipped labels and cut-off panel content.

The successful README assets were clear explanatory images that preserve the plugin's visual language while showing the workflow at high resolution.

## Preferred README screenshot shape

For BIS Loadouts README assets, prefer two clean explanatory screenshots over raw cramped sidebar captures:

1. `docs/assets/bis-loadouts-side-panel.png`
   - boss selection
   - setup style controls
   - Analyze button
   - selected boss setup summary
   - loadout fit / estimated DPS / hit chance
   - recommended equipment grid
   - basic gear cycling / 1H-2H note

2. `docs/assets/bis-loadouts-recommendations.png`
   - gear controls bullets
   - boss attack style guide from weakest to strongest
   - DPS per style bars
   - public data/fallback note

Use readable README-scale dimensions around 700 px wide and a dark RuneLite-like palette. Prioritize clarity over exact pixel-perfect RuneLite capture when the goal is explaining the plugin in GitHub.

## Slogan and explanatory SVG pattern

When the audience wants a plainspoken, non-technical opening, put a one-line selection rule immediately below the title rather than burying it in formula documentation. A useful shape is:

```text
Outcome slogan.
Pick the boss's weakest style -> get enough accuracy to land hits -> add damage -> account for attack speed.
For Magic, explicitly match the elemental weakness.
```

Keep it accurate but conversational. Blue-collar/pub humour can work when appropriate, but keep it non-hostile and avoid jokes that obscure the gear rule.

For architecture and formula graphics, prefer repository-owned SVGs under `assets/readme/`:

- use a fixed `viewBox`, large text, high contrast, and a dark RuneLite/OSRS-inspired palette;
- include `<title>`, `<desc>`, `role="img"`, and descriptive Markdown alt text;
- use system fonts and no remote scripts, fonts, trackers, or image dependencies;
- make the simple formula conceptual rather than falsely exact: `accuracy x damage / attack time = DPS`;
- make the architecture explain inputs -> combat rules -> ranked loadout, not internal class names;
- render each SVG in a browser and visually inspect clipping, overlap, contrast, spacing, and README-scale readability.

If support copy mentions both real-money donations and in-game GP, keep them explicitly separate. Never imply GP-for-cash or an exchange. A voluntary coffee link and a separate voluntary in-game tip can share a joke, but add a short no-swap clarification.

## Verification checklist

Before committing README visual updates:

- open/analyze every generated PNG or SVG and confirm it is not blank;
- confirm text is readable at GitHub README scale;
- confirm no major label is clipped on the right edge;
- validate SVG XML and confirm every local Markdown image target exists;
- confirm the graphics communicate how to use the plugin, not just what a tiny sidebar looks like;
- after pushing, inspect the live GitHub README and verify each image is complete with non-zero natural dimensions, the slogan is present, and donation links resolve to the intended URL;
- run `./gradlew clean test assemble --no-daemon --console=plain` after code/doc asset changes;
- commit/push the child repo first, then advance the immutable Plugin Hub marker or parent pointer as applicable;
- re-verify the Plugin Hub PR still changes only its one marker and that the official `build` check succeeds.

## Pitfalls

- Do not claim README visuals are fixed after only generating files. A non-empty asset can still be blank, cropped, illegible, or fail to render on GitHub.
- Do not invent a donation handle. Search maintained project metadata for the verified public URL.
- Do not flatten OSRS selection into “highest strength wins.” Accuracy, defence style, max hit, attack speed, elemental eligibility, budget, and encounter restrictions remain separate inputs.