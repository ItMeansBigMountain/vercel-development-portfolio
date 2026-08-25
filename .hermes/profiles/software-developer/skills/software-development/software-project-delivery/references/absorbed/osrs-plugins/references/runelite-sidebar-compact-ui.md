# RuneLite sidebar compact UI notes

Use this when a RuneLite plugin side panel looks too wide or forces horizontal scrolling.

## Problem signals

- User screenshot shows the plugin panel occupying too much horizontal space beside the game/client sidebar.
- Long labels/status strings stretch `PluginPanel` width.
- Equipment grids with fixed cells and padding overflow the standard RuneLite sidebar width.
- A horizontal scrollbar appears in a side panel.

## Compacting pattern

For Swing `PluginPanel` side panels:

1. Keep copy short: use labels like `None`, `Mage`, `Range`, `Melee` instead of descriptive sentences inside controls.
2. Move radio controls into a small 2x2 `GridBagLayout` instead of stacking full-width labels vertically.
3. Reduce panel padding to around `4px` and avoid `Integer.MAX_VALUE` widths on nested panels unless the parent width is constrained.
4. Disable horizontal scrollbars on the main scroll pane:
   ```java
   scrollPane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
   ```
5. Wrap explanatory/status text in bounded HTML divs so labels do not force a wider preferred size:
   ```java
   new JLabel("<html><div style=\"width:198px\">" + escape(text) + "</div></html>");
   ```
6. Shrink equipment grid cells for sidebar use. In BossReadinessScore, `66x50` cells with `1px` grid insets fit much better than `88x58` cells with `4px` insets.
7. Keep arrow buttons tiny (`~12x18`, zero margins) and abbreviate item names (`corrupted` -> `corr.`, `perfected` -> `perf.`, `necklace` -> `neck`) before truncating.
8. Summarize long data-source/status messages (`Live boss data loaded.`, `Using fallback data.`) instead of rendering API/source detail in the main panel.

## Verification

After compacting, run the plugin's Java 11 build/test command, usually:

```bash
JAVA_HOME=/opt/data/jdks/current-java11 ./gradlew test assemble --no-daemon
```

Then ask for/inspect a RuneLite screenshot if possible. Visual fit matters more than just passing compilation for sidebar UI work.
