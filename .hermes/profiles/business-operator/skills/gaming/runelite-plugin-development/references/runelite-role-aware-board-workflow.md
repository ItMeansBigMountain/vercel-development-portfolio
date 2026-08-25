# RuneLite role-aware board workflow and threading

Use this reference when a RuneLite plugin combines clan authority, a narrow multi-page panel, and a remote board/service.

## Product placement

- Put operational workflows in the plugin panel, not RuneLite configuration. Config is for durable preferences; creating/editing domain records belongs in role-aware panel pages.
- Pin production service endpoints in code. Do not expose backend URL overrides in production settings.
- Remove obsolete config methods, enums, branches, README instructions, and tests together; scan active source before declaring the surface gone.

## Narrow panel navigation

A robust board layout uses fixed top-level tabs and nested detail state:

1. Clan overview: local roster count, server-installed count, history/scheduled/open counts, next fight.
2. Public board: secondary filters for unopposed posts and scheduled fights.
3. Private setup: leader-only publish/direct-challenge workflow.

- Preserve the active top-level tab and secondary filter when opening details.
- Back navigation should pop only the nested detail page, not reset the whole panel.
- Members may read unopposed cards but must not be able to open/accept them. Scheduled details may remain readable.
- Put a compact `+` create action directly in the public Board tab header for authorized leaders; do not force leaders to discover creation only through a separate setup tab. Hide it entirely for ordinary members, and still enforce server-side capability checks.
- The `+` action may navigate into the existing setup workflow with a blank opponent rather than duplicating the form.
- UI hiding is not authorization: backend capabilities and participant/resource checks remain mandatory.
- Render truthful empty states; never add fake fights to make the layout look populated.

## Clan counts and authority

- Read the complete roster from `Client.getClanSettings()` / `ClanSettings.getMembers()`.
- Treat clan settings as late-loading state: an initial `LOGGED_IN` snapshot may still be `null` or empty even while the in-game clan UI populates moments later.
- Re-snapshot when a non-guest `ClanChannelChanged` arrives and use a lightweight, change-detected fallback poll for a few game ticks. Compare a fingerprint such as clan name + local rank + roster size; only refresh the panel/service when it changes.
- Overlay the newest local roster count onto panel state immediately instead of waiting for another HTTP response. This turns stale `0/0` into truthful `registered/roster` as soon as RuneLite exposes the roster.
- Resolve the local member and rank from `ClanSettings.findMember(playerName)`. Use `ClanSettings.titleForRank(member.getRank())` for clan-defined display titles such as `General`; raw numeric fallback labels like `Member rank 0` are misleading when a title exists.
- Use `ClanChannel` only as a brief pre-settings fallback and for online channel presence, not total membership or final rank authority.
- Ignore guest-clan events when refreshing primary-clan identity or authority.
- Snapshot client objects on `ClientThread` into immutable strings/numbers/DTOs before background HTTP or Swing work.
- Display plugin coverage as `registered installations / roster members`. The denominator is available from RuneLite, but RuneLite cannot reveal which roster members have the plugin installed; the numerator must come from installation registration and may not represent unique humans.

## Thread boundaries

- RuneLite `Client`, clan settings/channel, player state, and chat writes belong on `ClientThread`.
- Swing component mutation belongs on the EDT via `SwingUtilities.invokeLater`.
- Network and JSON work stays off both threads.
- A network completion should return through `ClientThread`, update immutable state and chat, then schedule panel rendering on the EDT.
- Never call a method that reads `Client` from an executor merely because its final operation updates Swing.

## Login/status messaging

- Wait for the asynchronous board refresh before reporting counts or the next scheduled fight.
- Build messages from the refreshed state, not stale config values.
- Use explicit RuneLite color tags for visibility rather than inheriting a potentially unreadable default.
- Keep login text concise: open count plus next scheduled fight or a truthful no-future-war state.

## Public service projection

Return separate sanitized collections such as:

- `availability`: open posts;
- `scheduled`: confirmed challenges;
- `history`: completed challenges.

Public scheduled/history rows may include clan IDs, start time, duration, combat range, and status. Exclude private world, location, rules, credentials, installation IDs, and internal audit data.

## Stack-trace ownership triage

Before changing the active plugin, identify the first non-RuneLite frame in the stack trace. A package/class such as `com.vendor.OtherOverlay` indicates another plugin. State that clearly, recommend disabling/updating that plugin to stop render-loop spam, and do not attribute or patch it as part of the current project unless its source is actually in scope.

## Verification sequence

1. Add regression tests for removed config methods, member/leader interaction, login state, and public privacy.
2. Run Java 11 `clean test assemble`.
3. Run service unit tests and syntax checks.
4. Scan source for removed config/development names.
5. Deploy service first and verify the live JSON schema.
6. Push the plugin against the deployed contract.
7. Push child repos before updating exact parent gitlinks.
