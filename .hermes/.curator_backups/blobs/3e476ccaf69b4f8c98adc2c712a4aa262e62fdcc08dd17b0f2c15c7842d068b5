# Networked RuneLite plugin production-readiness gate

Use this before moving any RuneLite plugin with a custom backend from `in-progress` to `pr-review-pending`.

## Third-party data and consent

- Derive disclosures from actual request builders, registration payloads, telemetry event serialization, and backend persistence—not README claims.
- Separate service calls required for the core feature from optional analytics/telemetry. A required online board does not imply consent to combat/location telemetry.
- Any option that enables transmission must clearly name the destination and payload categories in-client. README disclosure alone is insufficient.
- Default optional telemetry off. Treat consent as a concurrency boundary, not merely a UI/config default. When off:
  1. return from event subscribers before player/opponent attribution work;
  2. do not create periodic heartbeats;
  3. block queue insertion;
  4. block drain/upload;
  5. recheck consent inside already-scheduled worker tasks;
  6. never requeue a failed batch after consent is withdrawn; and
  7. immediately clear buffered events and attribution state.
  A batch drained just before opt-out must be discarded rather than uploaded or restored.
- Keep telemetry consent separate from public-profile visibility. A publication toggle must never silently enable collection. If a publication preference is sent during required registration, refresh/re-register promptly when that preference changes.
- Document operator/contact, retention, deletion, processors/storage, what “private” means, and a stable privacy-policy location before production submission.

## Resilient API parsing

- Parse JSON with typed/validated Gson DTOs or guarded `JsonObject` access. Do not use substring searches for session tokens, arrays, capabilities, or expiry values.
- Reject missing/blank tokens, invalid timestamps, null/wrong-type collections, empty successful bodies, and unknown required shapes as controlled `IOException`/domain failures.
- Treat runtime parser exceptions as network refresh failures at the worker boundary.
- Every in-flight guard and loading indicator must be released on success, checked failure, unchecked parse failure, stale identity, cancellation, and shutdown. Prefer one worker-level completion/finally path that always schedules cleanup.
- Preserve identity-generation checks across async completion; malformed responses must not re-enable stale sessions or state.

## UI semantic and endpoint integrity

- Build an action matrix from visible buttons/links to concrete handler methods, HTTP methods/routes, payloads, and expected state transitions. Search for API client methods with no callers and UI promises with no corresponding fetch/mutation path; dead client methods often reveal phantom functionality.
- Button labels must describe the endpoint/action actually executed. A button labeled “Accept & schedule” must mutate/accept the selected record; pre-filling a new challenge form is not acceptance.
- If the service has no verified accept flow, use an honest label such as “Draft private challenge” or “Challenge this clan,” remove unused action methods, and correct README route tables instead of inventing private response schemas.
- An authenticated route returning `401 invalid_session` proves that the route exists, not that its successful response schema or UI workflow is known. Do not infer authenticated JSON fields from the route name. Implement only from authoritative backend source/docs or a consenting real-session capture.
- Disable submission controls while an action is in flight and show pending/success/failure inline. Retain entered values after failure and prevent double dispatch.

## Safe live-contract verification

- Probe public/read-only health and listing endpoints with bounded timeouts; record HTTP status, content type, and a bounded body sample.
- Verify health semantically with parsed JSON (for example `ok == true`), not substring matching.
- For authenticated endpoints, unauthenticated `401` smoke tests are safe evidence of authentication enforcement only. Do not create synthetic production registrations, fights, or telemetry merely to test a release candidate.
- Compare live public schemas with parser requirements, but keep automated fixtures for malformed, reordered, delayed, and authenticated responses that cannot be exercised safely in production.

## Required tests

Use MockWebServer or an equivalent injected HTTP fixture to cover:

- compact and pretty valid JSON;
- reordered keys and escaped strings;
- malformed JSON and empty successful bodies;
- missing/null/wrong-type arrays and objects;
- invalid expiry values and blank session tokens;
- HTTP 4xx/5xx and delayed/reordered responses;
- loading/in-flight cleanup followed by a successful retry;
- shutdown/cancellation and A→B→A identity changes;
- telemetry disabled versus enabled request capture;
- double-click mutation suppression and control recovery.

A Swing paint smoke test and a green standalone Gradle build are not substitutes for these network/lifecycle tests.

## Submission gate

Before opening the Plugin Hub PR:

1. Run Java 11 `clean test assemble`.
2. Run the network/async matrix above.
3. Capture real requests for each privacy configuration and compare them with docs.
4. Validate leader authorization and acceptance workflow using consenting real clans/accounts; do not create synthetic production records.
5. Confirm metadata consistency, unique approved icon, production-pinned HTTPS endpoint, no developer/role-preview switches, and one immutable marker SHA.
6. Open the PR only at its user-approved position in the one-open-PR release queue.
