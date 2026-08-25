# RuneLite social-tracking side panel pattern

Use this reference when building OSRS/RuneLite plugins that track friends, clan chat, or friends chat members in a side panel.

## Product defaults

- Start empty by default. Do not add fake/demo players like sample clanmates; users read those as real tracked people.
- Use clear empty/unsupported states per source until live RuneLite scanners populate members.
- Keep source tabs explicit and player-facing: `Friends Chat`, `Clan Chat`, `Friends List`.
- Rescan when the player logs in, on manual refresh, on relevant config changes, and on a configurable interval.
- Expose refresh interval as integer minutes; default to `60`, with a sane bounded range such as `1..1440`.

## State model

Recommended boundaries:

- `TrackedMember`: normalized display name, source tags, status, first/last seen, last world, activity summary.
- `TrackedMemberSource`: friend, clan, friends chat.
- `SocialTrackerState`: immutable panel snapshot.
- `SocialTrackingService`: owns member map, ignored/removed set, source merging, cap enforcement, and serialization.
- Source scanners should produce snapshots/events and feed the service; the panel should render service state rather than talk directly to RuneLite APIs.

## Memory and removal behavior

- Let users remove/untrack members one by one.
- Removed members should be added to a compact ignored set so rescans do not immediately re-add them.
- Cap tracked members with config to avoid unbounded memory/API usage.
- Store compact records only; avoid persisting long event histories in RuneLite config.

## Default RuneLite side-panel width

RuneLite side panels must be usable at default width without forcing users to resize the client.

Practical Swing tips:

- Use small outer padding, e.g. `6px` rather than `8-12px`.
- Prefer compact buttons (`×` with tooltip) over wide labels like `Remove`.
- Use narrow HTML label body widths, e.g. about `170px` for summary text and `110-120px` for row text.
- Disable horizontal scrollbars on the panel scroll pane.
- Use compact tab labels/fonts when three tabs are shown.
- Reduce heatmap/grid gaps and cell sizes.
- Test long display names, empty states, unsupported-source messages, and error/status labels for overflow.

## Verification

Run from the plugin repo with Java 11:

```bash
./gradlew clean test assemble --no-daemon --console=plain
```

For the user's Windows local copy, after pushing the child repo:

```bat
git switch main
git pull origin main
.\gradlew.bat run --no-daemon
```
