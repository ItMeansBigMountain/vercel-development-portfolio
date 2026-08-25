# Comparative Plugin Hub Source Audits

Use this when the user points to an existing RuneLite Plugin Hub plugin and asks another plugin to work or look similarly.

## Evidence chain

1. Resolve the Plugin Hub slug through the authoritative `runelite/plugin-hub` marker file, not search-result repository guesses.
2. Read the marker's `repository`, `commit`, and `version` fields.
3. Clone into a disposable research directory and check out the exact pinned commit. Do not analyze only the upstream default branch; it may be ahead of what RuneLite reviewed.
4. Inspect source evidence across these dimensions:
   - top-level panel/navigation and state-dependent views;
   - reusable cards, filters, detail/back behavior, loading/empty/error states;
   - discovery/network protocol, reconnects, deltas, fallback/capability negotiation;
   - host/member authority, identity, admission, and roster semantics;
   - privacy projection and what client state leaves the machine;
   - persistence/history;
   - client-thread, background-executor, socket-callback, and Swing EDT boundaries;
   - startup/shutdown lifecycle and resource cleanup;
   - RuneLite API usage and Plugin Hub review risks.
5. Inspect promotional video frames separately when possible. Treat the video as UX evidence, never as proof of implementation.

## Safe adaptation rule

Extract interaction patterns, not source code or incompatible trust assumptions. Before editing, write down:

- patterns to adopt (for example compact icon navigation, count badges, cards, dedicated history, explicit connection states, passive discovery refresh);
- patterns to reject (for example sharing inventory/equipment, P2P cooperative authority, party passphrases, user-configurable production endpoints, or identity fields inappropriate to the target product);
- target-product invariants that must remain unchanged (server authority, privacy, uncertainty labels, role gates, sanitized public projections).

Do not claim interoperability merely because products have similar panels. Compare protocols, identifiers, data ownership, and authentication explicitly.

## Narrow Swing visual QA

A clean build is insufficient for RuneLite side-panel work.

1. Add a headless render smoke test with representative open, scheduled, completed, offline, and leader/member states.
2. Render at `PluginPanel.PANEL_WIDTH` and a realistic height.
3. For undisplayed Swing trees, recursively call `doLayout()` on child `Container`s before painting; root-only `doLayout()` can produce a misleading blank screenshot with only fixed border components visible.
4. Emit the PNG under `build/reports/` and visually inspect:
   - top controls rendered as labels/icons rather than ellipses;
   - scrollbar does not cover card text;
   - long status labels wrap or use shorter truthful wording;
   - footer remains readable;
   - no horizontal scroll or large blank gutter.
5. If fixed-width `JButton`s collapse to `...`, reduce button margins (`Insets(0,0,0,0)`), set a compact font, and use tooltips for full labels.
6. Correct shared content-width calculations rather than special-casing individual sentences. Still shorten verbose labels when the compact wording is clearer.

## Live discovery without copying protocols

A product can approximate a live board without adopting another plugin's WebSocket/P2P implementation. A bounded periodic refresh is appropriate when:

- HTTP reads already run off-thread;
- RuneLite state access is marshalled to `ClientThread`;
- a single-flight guard prevents overlap;
- shutdown cancels the scheduled task;
- manual/login/post-action refreshes remain available;
- cadence has a regression test.

## Publishing with a dirty parent repo

Push and remotely verify the child plugin first. Stage only the gitlink in the parent.

If parent `main` has advanced and the primary parent worktree contains unrelated tracked/untracked changes, do not stash, reset, or pull through that worktree. Use a disposable authenticated clone of latest remote `main`, fetch the local parent branch into a temporary ref, cherry-pick only the gitlink commit, push the clean fast-forward, and verify through the GitHub API that:

- child remote `main` equals the intended child SHA;
- parent remote `main` advanced;
- parent path type is `submodule`;
- parent gitlink equals the child SHA.

Use a temporary environment-backed `GIT_ASKPASS` helper when `gh` is unavailable. Never store the token in the remote URL or repository config, and remove the helper after use.

## Example findings from OS Party

At Plugin Hub-pinned OS Party revision `a6f5d6d57182c37e1cb84dc4cf38e2d9b13c30a1` (version `1.0.50`):

- discovery uses a session-long WebSocket with jittered reconnect, revision-based delta resubscription, and endpoint fallback;
- live party is migration-capable: server capabilities choose once at startup between legacy RuneLite relay and a server-authoritative V2 backend;
- privacy flags strip inventory/equipment before sending and are reapplied after incremental-state merge;
- concurrent collections/volatile state cover socket callbacks, client reads are client-thread aware, and Swing callbacks marshal to EDT;
- the reusable UX patterns are compact navigation, cards, counts, dedicated history, structured creation, and persistent connection state—not its party roster, inventory sharing, or passphrase protocol.
