# RuneLite plugin icon uniqueness and review workflow

Use this when creating, finalizing, restoring, or submitting any RuneLite plugin in the user's OSRS portfolio.

## Icon surfaces to audit

A plugin can expose more than one icon surface:

1. Root `icon.png` — Plugin Hub listing icon; maximum 48x72 px.
2. Embedded toolbar/navigation resource — loaded by `NavigationButton`, `ImageUtil`, `getResourceAsStream`, or similar code.
3. Template icon — must be neutral and must not accidentally become another plugin's production identity.

Do not assume matching filenames or a root-only search finds every displayed image. Search each child repository independently because parent-level searches can skip nested Git/submodule worktrees.

## Portfolio-wide audit

For every active lifecycle lane (`in-progress`, `pr-review-pending`, `completed`, `_templates`):

1. Inventory root and embedded PNG/SVG resources in each child repo.
2. Inspect navigation-button construction to identify the image RuneLite actually displays.
3. Compute hashes for all icon assets. Identical hashes across unrelated plugins are a blocking identity defect even when filenames differ.
4. Read image dimensions/mode and enforce Plugin Hub limits on root `icon.png`.
5. Build a labeled contact sheet showing each candidate enlarged with nearest-neighbor scaling and at actual 48x48 size.
6. Visually inspect silhouette, relevance, contrast, clipping, transparency, and tiny-size legibility.
7. Send the review sheet, then individual 48x48 assets when requested. Do not apply, commit, update a Plugin Hub marker, or publish generated designs until the user approves them.

## Design standard

- Every plugin must have a unique, product-relevant silhouette and dominant palette.
- Prefer simple OSRS-inspired pixel art that remains readable at 32-48 px.
- Avoid text, tiny detail, reused logos, copyrighted interface frames, and generic duplicate shields/skulls.
- Root Plugin Hub and embedded toolbar icons may use the same approved product identity within one plugin, but unrelated plugins must not share it.
- Completed plugins still need correction when identity is wrong, but prioritize pending-review and future submissions first. A merged Plugin Hub plugin requires a new child commit and marker-update PR for a root-icon correction; do not pretend editing the repository alone changes the already-pinned official version.
- The boilerplate/template receives its own neutral construction identity and must never ship unchanged as a production plugin icon.

## Generation fallback

If the configured image-generation provider is unavailable, create an original deterministic vector or pixel-art asset locally rather than stopping at a prompt. Render a real PNG, verify its hash/dimensions, and visually review it. Capture the successful fallback technique, not transient provider setup failure.

## Verification before publication

- All portfolio icon hashes are unique across unrelated plugins.
- Root `icon.png` is within 48x72 px and opens as a valid PNG.
- Embedded resource paths resolve and match the approved product identity.
- Build/tests pass after replacement.
- Pending Plugin Hub PR still changes one marker and points to the tested immutable child SHA.
- User approved the exact visual asset being published.
