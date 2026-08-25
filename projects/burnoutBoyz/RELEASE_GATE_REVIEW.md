# BurnoutBoyz independent release-gate review

Reviewed 2026-08-25 against task `t_738ed6e0`.

## Verdict

**FAIL — not eligible for production or closed beta.** The universal client compiles, lints, exports web, and generates Android/iOS configuration, but the automotive, authorization, privacy, and platform evidence required by the gate is incomplete.

## Executed evidence

- `python3 -m unittest discover -s tests -v`: 3/3 tests passed, all limited to UX view models.
- Fresh SQLite migration/schema check: migrations 1–4, 32 tables.
- Universal client: TypeScript check passed; Expo lint passed; static web export passed (4 routes); Android prebuild passed; iOS public config generation passed.
- No production web, TestFlight, or Play internal-track verification was performed or claimed here.

## Release-blocking findings

1. **Authorization / tenant isolation is not enforced at service boundaries (critical).** Multiple methods accept only globally addressable IDs and do not bind operations to the authenticated owner. Examples include `MaintenanceService.export_vehicle(vehicle_id)`, `delete_vehicle(vehicle_id, requested_by_user_id=...)`, record mutations, `OwnersManualUXService.vehicle_manual(vehicle_id)`, garage mutation methods, connected refresh/link operations, and manual mileage writes. In particular, `requested_by_user_id` is recorded by deletion but is not checked against vehicle ownership. An API wrapper must not be relied upon as the sole undocumented control; ownership-aware queries and negative cross-tenant tests are required.

2. **Automotive accuracy evidence is insufficient (high).** The repository has only three UX tests. There is no executable matrix for repeating, one-time, mileage-only, time-only, whichever-first, severe/normal/unknown use, tolerance, schedule-version changes, make/trim applicability, VIN ambiguity, recall refresh failure, or confirmation matching. The README describes these behaviors, but this review cannot accept untested claims. Bundled intervals remain synthetic and cannot establish real-world automotive accuracy.

3. **Privacy/deletion and upload abuse evidence is insufficient (high).** There are no tests proving VIN ciphertext/fingerprint behavior, token isolation/revocation, receipt path traversal and size/type limits, complete deletion across all related rows/files, orphan cleanup, or export redaction. The client says files are not uploaded because no authenticated upload API exists; therefore upload security and deletion cannot pass production review.

4. **Notification abuse and rate controls are incomplete (high).** Permission UX exists, but there is no verified server-side deduplication/rate limiting, tenant authorization, quiet-hours policy, cancellation/deletion behavior, or abuse test suite for reminders/push.

5. **Accessibility and misleading-safety validation is partial (medium/high).** Fear-free and source caveat copy is unit-tested in one fixture, but there is no automated accessibility scan, keyboard/screen-reader/device validation, contrast evidence, or systematic assertion that every schedule/recall/DTC surface retains provenance and non-diagnostic caveats.

6. **Release matrix remains external-gated.** Exact production web, installable iOS/TestFlight, and installable Android/internal-track URLs are absent. `apps/universal/RELEASE.md` correctly lists owner-account, signing, hardware, authenticated API, hosting, monitoring, and association-file gates.

## Required closure

- Add an authenticated service/API boundary with ownership-scoped queries for every read/write/delete/export operation and cross-tenant denial tests.
- Add deterministic schedule and recall fixture suites covering all interval modes, severities, ambiguity/failure states, and version transitions; use licensed/provider fixtures before asserting automotive accuracy.
- Implement and adversarially test receipt upload constraints, token handling/revocation, complete deletion, export privacy, and notification abuse controls.
- Run accessibility automation plus physical iOS/Android and assistive-technology checks.
- Re-run this independent gate only after the above and the exact three-platform release URLs exist.

## Implementation handoff for re-review (2026-08-25)

The P0 implementation pass now provides an authenticated principal on the onboarding,
maintenance, owner-manual UX, recall, and connected-vehicle service boundaries. Vehicle,
garage, service-record, and connected-account operations verify ownership before reads or
writes and return the same `resource not found` authorization failure across tenants.
Deletion derives its requester from the authenticated principal rather than accepting a
caller-supplied audit identity.

Adversarial backend checks now cover cross-tenant read/write/export/delete denial, receipt
size/type constraints and filename containment, export removal of receipt storage paths and
VIN ciphertext/fingerprints, bounded notification output and per-run deduplication, and a
deterministic interval/severity/applicability/tolerance/version matrix. All automotive matrix
values are explicitly **synthetic test fixtures** (`synthetic_test_fixture`); they are not
licensed production schedule data and do not establish real-world automotive accuracy.

Executed after implementation:

- `python3 -m unittest discover -s tests -v`: 8/8 passed.
- `python3 -m compileall -q burnoutboyz tests`: passed.
- Fresh SQLite migration/schema check: migrations 1–4, 32 tables.
- Universal client: TypeScript, Expo lint, static web export (4 routes), Android prebuild,
  and iOS public config generation passed.

This handoff does **not** claim independent gate approval, licensed production automotive
accuracy, automated/physical assistive-technology coverage, physical iOS/Android execution,
store review, or production web/TestFlight/Play URLs. Those evidence items remain for the
pre-created independent reviewer/release lanes.
