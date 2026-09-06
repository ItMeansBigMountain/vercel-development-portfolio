# OSRS RuneLite Plugin Portfolio

This directory tracks the user's RuneLite/OSRS plugin work by shipping state.

## Directories

- `_templates/` — reusable scaffolds, examples, and starter materials.
- `in-progress/` — plugins still being designed, implemented, or actively debugged.
- `pr-review-pending/` — plugins we consider code-complete locally and ready for RuneLite Plugin Hub PR/review, but not yet approved/listed on the Plugin Hub.
- `completed/` — plugins whose Plugin Hub PR has been approved and are shareable/installable from RuneLite's official Plugin Hub.

## Promotion rules

1. Keep active development in `in-progress/` until the plugin has a passing local build, tests, screenshots, and user-approved UI.
2. Move to `pr-review-pending/` after local release criteria pass and a Plugin Hub submission branch/manifest entry is ready or opened.
3. Move to `completed/` only after the RuneLite Plugin Hub PR is approved/merged and the plugin is visible/shareable from the official Plugin Hub.

## RuneLite Plugin Hub submission flow

Based on RuneLite's Plugin Hub documentation:

1. Keep the plugin repository public.
2. Use Java 11 and the standard RuneLite external plugin template/build style unless a custom build is justified.
3. Ensure `runelite-plugin.properties` includes display name, author, support URL, description, tags, plugin class, and version where required by current tooling.
4. Include a README and optional `icon.png`.
5. For every plugin that makes runtime network calls, add an `External APIs` or `API reach-out guide` section to its README. Derive it from source and document each service/host, relevant route and HTTP method, purpose, data sent and received, authentication, failure/fallback behavior, and privacy/telemetry. Clearly distinguish browser links and local RuneLite APIs from outbound requests; never include credentials. If the plugin makes no runtime requests, state that explicitly.
6. Add a clear plugin/config warning for third-party calls that transmit player-derived data. For Who's Grinding Panel, selected player names are sent to Wise Old Man and official OSRS hiscores when lookups are enabled.
7. Push the plugin repo and get the exact commit hash to submit.
8. Fork/branch `runelite/plugin-hub`.
9. Add/update the Plugin Hub manifest entry with the plugin repository URL and commit hash.
10. Open a PR to `runelite/plugin-hub`.
11. Watch GitHub Actions / RuneLite Plugin Hub checks and push fixes until CI passes.
12. After approval/merge and Plugin Hub visibility, promote the plugin from `pr-review-pending/` to `completed/`.

Useful docs:

- https://github.com/runelite/plugin-hub
- https://github.com/runelite/runelite/wiki/Information-about-the-Plugin-Hub
- https://github.com/runelite/example-plugin
- https://github.com/runelite/plugin-hub-tooling

## Current status

- `completed/BisLoadouts` — officially merged as Plugin Hub PR #14682. Icon-only marker update PR #16153 is the single currently open submission.
- `completed/DeadmanBreachTimer` — officially merged as Plugin Hub PR #10567. Its approved icon update is queued after BIS Loadouts.
- `completed/WhosGrindingClanPanel` — officially merged as Plugin Hub PR #13917. The official-hiscores snapshot fallback repair is pushed in the child repository; its marker update waits behind the icon release train.
- `in-progress/ClanWarBoard` — active product development. PR #16152 was closed unmerged and must not be resubmitted until development and testing are complete.
- `services/clan-war-board-service` — active backend supporting Clan War Board; it follows the product's in-progress lifecycle but remains separated from plugin source.
- `_templates/osrs-plugins-boilerplate` — reusable starter only, never a shipping plugin.
- `pr-review-pending/` — currently empty. Nothing is both locally complete and waiting for an initial Plugin Hub review.

## Submission queue

RuneLite allows one open Plugin Hub PR per author. Current order:

1. BIS Loadouts icon update — open: https://github.com/runelite/plugin-hub/pull/16153
2. Deadman Breach Timer icon update — queued after BIS closes or merges
3. Who's Grinding Panel maintenance marker — queued after the approved icon updates
4. Clan War Board initial submission — excluded until product development is explicitly complete
