# Wilderness multi-zone geometry research

Use when implementing Clan War Board Wilderness venue validation, random multi-only locations, or boundary overlays.

## Authoritative revisions inspected

- RuneLite Plugin Hub marker `plugins/wilderness-multi-lines` resolves to `Nightfirecat/plugin-hub-plugins` commit `d81bb4c444c3772b1563be8a8fcc2252c84a0a4f`.
- Marker `plugins/multi-lines` resolves to `tsbreuer/Multi-Lines` commit `858246aa7381584c81b1a9a94c67af595a75a51a`.
- Both projects use BSD-2-Clause; preserve notices and disclaimers when adapting source or coordinate data.

## Geometry model

- Multi zones are unions of axis-aligned world-tile rectangles `(x, y, width, height)` represented with `java.awt.Rectangle` and `Area`.
- Multi-Lines JSON groups rectangles under named areas with `Enabled`, `Removed`, `Wilderness`, `Notes`, and `Tiles` metadata.
- Surface and underground Wilderness coordinates coexist; caves use Y values around 10000. Plane is not encoded in rectangles, so application models should explicitly track plane/layer or enforce surface-only policy.
- Tiny islands and corrective strips (`1x1`, `1x2`, `2x1`) are real. Region IDs or coarse bounding boxes are not sufficient.

## Validation and random venues

- Compile rectangles into a deduplicated tile-membership set or bitset. Validate exact tiles against the union, then apply enabled/world-mode/plane/exception policy.
- Sample uniformly from deduplicated valid tiles, not rectangles; rectangle sampling biases by overlap and rectangle partitioning.
- For venue centers requiring clearance, erode the union by the match radius and sample from the remaining tiles.
- Keep authoritative containment separate from clipped/simplified display paths.

## Boundary extraction

A deterministic tile algorithm is preferable for board logic: for each valid tile, emit only edges whose neighbor is invalid, then merge collinear runs. It naturally handles overlaps, disconnected islands, holes, and thin corrections.

The reference plugins instead union rectangles into `Area`, convert to `GeneralPath`, clip to the loaded scene, split into one-tile segments, and transform world coordinates to local/canvas coordinates. Multi-Lines' slope-tolerance simplifier is display-only and should not determine membership.

## Runtime edge cases

Wilderness Lines verifies map membership against RuneLite's `MULTIWAY_INDICATOR` using XOR on the prior tick. It ignores moves over two tiles (teleport-like) and suppresses known forced-movement exceptions: Wilderness agility bridge, north Lava Maze shortcut, and seed-pod transition tile.

## Source links

- Geometry/data and special rectangles: https://github.com/Nightfirecat/plugin-hub-plugins/blob/d81bb4c444c3772b1563be8a8fcc2252c84a0a4f/src/main/java/at/nightfirec/wildernesslines/WildernessLinesPlugin.java#L74-L165
- Runtime mismatch checks: https://github.com/Nightfirecat/plugin-hub-plugins/blob/d81bb4c444c3772b1563be8a8fcc2252c84a0a4f/src/main/java/at/nightfirec/wildernesslines/WildernessLinesPlugin.java#L241-L283
- World/local boundary pipeline: https://github.com/Nightfirecat/plugin-hub-plugins/blob/d81bb4c444c3772b1563be8a8fcc2252c84a0a4f/src/main/java/at/nightfirec/wildernesslines/WildernessLinesPlugin.java#L324-L383
- Overlay projection: https://github.com/Nightfirecat/plugin-hub-plugins/blob/d81bb4c444c3772b1563be8a8fcc2252c84a0a4f/src/main/java/at/nightfirec/wildernesslines/WildernessLinesOverlay.java#L52-L116
- Multi-Lines JSON loader: https://github.com/tsbreuer/Multi-Lines/blob/858246aa7381584c81b1a9a94c67af595a75a51a/src/main/java/com/tsbreuer/multilines/MultiLinesPlugin.java#L137-L226
- Multi-Lines path simplification: https://github.com/tsbreuer/Multi-Lines/blob/858246aa7381584c81b1a9a94c67af595a75a51a/src/main/java/com/tsbreuer/multilines/MultiLinesOverlay.java#L77-L181
