# Identity-bound asynchronous state in RuneLite plugins

Use this pattern whenever a RuneLite plugin combines player/clan identity, authenticated sessions, cached private state, background HTTP, retryable telemetry, or asynchronous leader actions.

## Ownership token: context plus monotonic generation

Derive an immutable identity context on `ClientThread` from the local player plus the relevant primary clan/account scope. Pair it with a monotonically increasing generation (epoch) that increments on every logout, hop, player change, clan change, shutdown/invalidation, and later return to the same identity.

A string key alone is unsafe: an A → B → A transition can make old work appear current again. Every identity-sensitive object or request must carry both `(context, generation)`:

- authenticated session and capabilities;
- board/detail snapshot containing private or player-scoped data;
- pending/in-flight mutation;
- telemetry queue and drained batch;
- session-rotation request;
- completion message and post-action refresh.

Store owner generation beside session and cached-state fields. Do not rely on the token, object identity, or current context string alone.

## Transition handling

On logout, world hop, player change, primary-clan change, shutdown, or explicit invalidation, immediately on `ClientThread`:

1. set the new active context and increment generation;
2. clear session, capability, and session-owner fields;
3. clear private/player metrics and selected private details;
4. clear queued telemetry and combat attribution state;
5. render an identity-neutral loading/offline state owned by the new generation;
6. start or coalesce a refresh for that generation.

Do this before rendering or accepting another action. Never leave old leader controls visible while the new identity registers.

## Safe refresh transaction

1. On `ClientThread`, bind the current identity and capture `(context, generation)`, clan snapshot, prior board, and prior board owner tuple.
2. Register/fetch off-thread using a **local** candidate session; never assign it to the plugin field on the executor thread.
3. On failure, retain stale data only when the prior owner tuple exactly equals the captured tuple; otherwise return an empty identity-neutral state.
4. Return completion to `ClientThread`.
5. Re-read current context/generation and install candidate session + board only when both still match.
6. If rejected as stale, clear the in-flight guard and immediately refresh the current identity.

Generation is mandatory, not optional, whenever logout/switch/relogin or A → B → A is possible.

## Safe authenticated mutations

An EDT click-time check is not sufficient because identity can change while the request waits for the executor.

1. Capture candidate session plus `(context, generation)` when the action begins.
2. Acquire the duplicate-action guard.
3. Return to `ClientThread` immediately before executor dispatch and revalidate:
   - plugin still running;
   - captured session is still the installed session;
   - captured owner tuple equals active tuple;
   - required server capability still exists;
   - local RuneLite rank still permits the action when rank is part of authorization.
4. If validation fails, release the guard and do not dispatch.
5. After success/failure, return to `ClientThread` and show completion UI or trigger refresh only if the same session and owner tuple remain current. Suppress old-context messages.
6. Release the guard on every path, including validation failure, IO failure, executor rejection, and shutdown/invalidation.

A request already transmitted before a legitimate identity transition may complete server-side; the client must prevent queued-not-yet-dispatched stale writes and must never present their completion as belonging to the new identity.

## Session rotation

Capture the session object and owner tuple. Install the rotated session only when:

- plugin is still running;
- installed session is still the captured object;
- active tuple equals the captured tuple;
- session-owner tuple equals the captured tuple.

This blocks stale rotation and A → B → A installation.

## Live-observation gap

Cached `(context, generation)` checks are necessary but do not prove RuneLite's live identity is unchanged: the client may have switched player, clan, or rank before the next clan event/fingerprint poll calls the binding routine.

- Immediately before dispatching a leader mutation, re-read `clanAccess()` on `ClientThread`, bind its context, and verify the captured tuple, installed session, required server capability, live clan membership, and configured minimum rank.
- Apply the same live re-read before rendering mutation completion UI or triggering its refresh; suppress results that now belong to another identity/rank.
- Before every telemetry enqueue, re-read live access, bind it, and reject the event if the event's earlier access snapshot differs from the new live context.
- Before every telemetry flush, bind a fresh live context before consulting the session or draining/transmitting the queue.
- On each game tick, bind live identity before session rotation or heartbeat work so delayed clan callbacks cannot create an old-session window.

## Telemetry boundary

Bind both pending and drained telemetry to `(context, generation)`.

- Clear pending buffers on identity transition.
- Revalidate the captured tuple before executor transmission.
- If upload fails, requeue only when captured tuple still equals both active tuple and current session owner.
- Otherwise discard the old-generation batch.
- Guard against a failed old-generation upload repopulating a freshly cleared new-generation queue.

## Thread ownership

- RuneLite client reads, identity changes, final authorization checks, and state installation: `ClientThread`.
- HTTP/JSON: executor thread.
- Swing mutations: EDT.
- EDT action handlers may capture volatile ownership fields but must not read RuneLite `Client` state directly.
- Keep network candidates local until a client-thread ownership check succeeds.

## Tests

Add pure regression tests for:

- same-owner failure retains cached data;
- changed-context failure clears cached/private data;
- same-context/new-generation (A → B → A) failure also clears it;
- old session cannot authorize under a new context or generation;
- stale registration/rotation cannot install;
- queued leader write is rejected before dispatch after generation change;
- old-context action completion UI/refresh is suppressed;
- telemetry clear resets queue/heartbeat state;
- telemetry dispatch/requeue rejects changed context and changed generation;
- duplicate-action guard releases on every abort/failure path.

## Review and publication gate

When an independent/background security or concurrency review is dispatched, do not publish before its result arrives. A passing build does not supersede an outstanding review. Apply findings, add focused regressions, rerun the clean Java build, review the replacement diff, and only then publish and remotely verify both child SHA and parent gitlink. If the review triggers substantial changes, review the final replacement diff again rather than assuming the first review covers it.
