# Clan War Board: CWA-first dual mode and post-fight replay

Use when extending Clan War Board across its RuneLite plugin, service, and website.

## Product model

- Make Clan Wars Arena (CWA) the primary/default lane and Wilderness (`Wildy`) secondary.
- Preserve separate fight lists, histories, clan ratings, player ratings, and formulas. Never mix CWA and Wildy records.
- Put one full-width `CWA | Wildy` switch at the top of the narrow RuneLite panel. The active mode controls board counts, history, creation defaults, visible stats, and submitted terms.
- Lock `mode` and `returnsAllowed` into canonical mutually accepted terms. CWA no-return is enforced even if a client submits `returnsAllowed=true`; Wildy may allow returns.
- Clan profiles expose both `rankings.cwa` and `rankings.wildy`. Public leaderboard accepts `?mode=cwa|wildy` and falls back to CWA.

## CWA scoring

CWA is normally no-return/last-team-standing. Use result first, then confidence-labelled damage pressure, tank survival, pile participation, transition speed, binds/freezes, off-pile activity, and survivor curve. Team success must outweigh damage farming.

Wildy separately uses result, kills/deaths, returns, location control, damage pressure, and third-party adjustment.

Only mutually accepted, completed, non-disputed fights above roster/telemetry coverage thresholds affect ratings. Version formulas and retain rating-change inputs.

## Roster and outsiders

- Snapshot both accepted clans' registered rosters for the fight window.
- Classify accepted-roster names to their side.
- Preserve observed non-roster players as `outsider/non-clan`; never silently assign them.
- RuneLite client rank/roster is observed evidence, not cryptographic identity proof.

## Replay

Every completed fight review must render a replay section, including an honest empty state when no usable positions exist.

The feasible replay is reconstructed telemetry, not video:

1. Align deduplicated POV events by timestamp/tick.
2. Store world/region/WorldPoint, player privacy identity, clan, type, amount, evidence, and confidence.
3. Render a canvas/minimap-like view with play/pause, timeline scrubber, colored clan markers, movement trails, damage/death labels, tick/event clock, and legend.
4. Missing actors/frames stay unknown; do not interpolate them as fact.
5. RuneLite minimap pixels are drawing coordinates. Persist WorldPoint/world-view/tick instead.

A single client sees only its loaded scene. Multi-client corroboration improves coverage but is not perfect proof.

## RuneLite observation boundary

Useful events include `GameTick`, `InteractingChanged`, `HitsplatApplied`, `AnimationChanged`, `ProjectileMoved`, `ActorDeath`, player spawn/despawn/change, game-state/world-view resets, and clan member/channel changes. Useful actor data includes name, world/local location, interacting target, animation, orientation, visible overhead, and coarse health ratio.

Hitsplats do not always prove attacker identity. Kill/assist, attack style, bind land, and prayer effectiveness must remain correlated/inferred with confidence.

Do not ship live enemy-prayer aggregation, prayer recommendations, weakness callouts, or scouting dashboards. Tactical prayer analysis must be delayed post-fight, consented, and policy-safe.

## Verification and publishing

- Java 11: `./gradlew clean test assemble --no-daemon --console=plain`.
- Service: run Python unit tests, extract inline website JavaScript and run `node --check`, then `git diff --check`.
- Push plugin and service child repos independently and verify remote SHA equality.
- Verify GitHub deployment completion and live replay markup/API mode contracts.
- Parent control repo may be dirty/divergent: stage only the two gitlinks. Do not force/push a divergent parent merely to publish pointers; report the local pointer commit separately.
