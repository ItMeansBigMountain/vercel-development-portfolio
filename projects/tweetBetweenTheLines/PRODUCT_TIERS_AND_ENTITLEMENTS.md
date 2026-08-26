# tweetBetweenTheLines — Product Tiers and Entitlements

Status: implementation handoff; pricing is a hypothesis, not validated demand. Privacy, security, legal, accessibility, and qualified clinical review remain launch gates.

## Customer pain, audience, and promise

Primary early audience: privacy-conscious individuals who have official social-platform archives and want to understand their own attention, interests, language, and behavior without surrendering control of the underlying data.

Pain: platform exports are difficult to inspect, opaque analysis asks users to trust unexplained conclusions, and many “AI personality” products overstate incomplete behavioral data.

Promise: validate the user's archive, calculate useful metrics deterministically, show coverage and derivation, and let the user export or delete everything. Payment buys continuity, comparisons, automation, and optional narrative convenience—not truth, safety, or control over personal data.

Next revenue action: recruit 10–15 consented design partners for archive-import interviews and test willingness to pay against the two Premium price points below before enabling public billing.

## Tier definitions

| Capability | Free | Premium | Premium + AI |
| --- | --- | --- | --- |
| Price hypothesis | $0 | Test $7.99/month or $59.99/year | Test $14.99/month or $119.99/year |
| Official archive import | 2 successful imports per rolling 30 days | 20 successful imports per rolling 30 days | 20 successful imports per rolling 30 days |
| Upload size | 250 MB compressed/import | 2 GB compressed/import | 2 GB compressed/import |
| Sources/accounts in a workspace | 1 account, 1 platform at a time | 10 accounts across supported platforms | 10 accounts across supported platforms |
| Deterministic import validation | Full: format/platform/version detection, accepted/rejected counts, warnings, duplicate handling | Same | Same |
| Core deterministic metrics | Full current-snapshot metrics | Full plus history and comparisons | Same as Premium |
| Coverage/confidence | Full source/date/category coverage, missing-data warnings, formula version, confidence/abstention | Same | Same |
| Explainability | Formula, numerator/denominator, filters, evidence aggregates, provenance and limitations for every metric | Same | Same, including AI evidence/provenance |
| Saved history | Current snapshot plus latest prior snapshot; 30-day derived-data retention by default | Up to 24 monthly snapshots; user-selectable 30-day, 1-year, or until-deleted retention | Same as Premium |
| Reports | 1 on-demand deterministic summary per rolling 7 days; in-app + JSON | Unlimited deterministic reports, trend and account/platform comparisons | Same plus limited AI narratives |
| Exports | Complete personal-data export and deletion manifest always available; JSON | Same plus CSV/PDF report bundles and comparison exports | Same as Premium; AI provenance included |
| Scheduled refresh | None | Up to weekly per account where official APIs, scopes, quotas, and review permit | Same as Premium |
| AI narrative analysis | None; no AI upsell blocks deterministic results | None | 10 successful narrative generations per billing month |
| Priority processing/support | Standard queue | Priority queue and email support | Priority queue and email support |

Annual equivalents are $5.00/month for Premium (37.4% below twelve monthly payments) and $10.00/month for Premium + AI (33.3% below twelve monthly payments). These are deliberately aggressive hypotheses for validation, not launch commitments or financial guarantees.

## Non-paywalled rights and safety

The following are entitlements for every authenticated user, including canceled or delinquent accounts:

- View consent receipts, source status, coverage, confidence, formulas, limitations, and analyzer/model provenance.
- Revoke a source, stop future jobs, correct derived information, export all user data, and request account/source deletion.
- See deletion progress and completion/failure receipts. Export/delete may require step-up authentication but never an active subscription.
- Access non-diagnostic safety language, abstention, and emergency-resource links where applicable.
- Receive accurate billing, renewal, cancellation, and data-retention information.

Cancellation immediately stops renewal and scheduled/AI jobs at period end. Read-only access to existing results continues through the paid period. After downgrade, over-limit accounts remain visible and exportable; the product does not delete or lock data to force an upgrade. Users choose which accounts/history to keep active for new processing.

## Canonical entitlement rules

The backend is authoritative. Clients may hide controls for usability but cannot grant access. Every limit check uses server time and an atomic counter. A “successful import” is charged only after sandbox validation recognizes a supported platform/schema and promotes at least one record; rejected, malicious, duplicate, canceled, or platform-unsupported uploads do not consume quota.

```ts
type PlanId = "free" | "premium" | "premium_ai";

type Entitlements = {
  importSuccessesPerRolling30Days: 2 | 20;
  maxCompressedImportBytes: 262_144_000 | 2_147_483_648;
  maxActiveAccounts: 1 | 10;
  retainedSnapshots: 2 | 24;
  deterministicReportsPerRolling7Days: 1 | null;
  comparisonReports: boolean;
  richExportFormats: readonly ("csv" | "pdf")[];
  scheduledRefreshMinIntervalHours: null | 168;
  aiNarrativesPerBillingMonth: 0 | 10;
  priorityQueue: boolean;
};
```

Canonical plan map:

| Rule | `free` | `premium` | `premium_ai` |
| --- | ---: | ---: | ---: |
| `importSuccessesPerRolling30Days` | 2 | 20 | 20 |
| `maxCompressedImportBytes` | 262144000 | 2147483648 | 2147483648 |
| `maxActiveAccounts` | 1 | 10 | 10 |
| `retainedSnapshots` | 2 | 24 | 24 |
| `deterministicReportsPerRolling7Days` | 1 | unlimited (`null`) | unlimited (`null`) |
| `comparisonReports` | false | true | true |
| `richExportFormats` | none | CSV, PDF | CSV, PDF |
| `scheduledRefreshMinIntervalHours` | disabled (`null`) | 168 | 168 |
| `aiNarrativesPerBillingMonth` | 0 | 0 | 10 |
| `priorityQueue` | false | true | true |

Additional enforcement rules:

1. `scheduledRefresh` also requires connector state `supported_api`, valid source consent for refresh, required official scopes, valid token, available platform quota, and enabled connector kill switch. Plan access never overrides platform restrictions.
2. A user may always run a deterministic analysis after a successful import; report quota limits a formatted summary, not metrics, validation, coverage, provenance, correction, export, revoke, or delete.
3. Cross-account comparison requires at least two separately consented active accounts and displays source/date coverage differences. It must not imply that unequal archives are directly comparable.
4. A snapshot version is immutable. Reprocessing creates a new snapshot with analyzer/formula version. Revocation removes descendants from future views and rebuilds affected snapshots.
5. Downgrade does not destroy excess sources or history automatically. New import, refresh, and snapshot creation remain paused until active usage fits the new tier or the user deletes/selects data.
6. Billing webhooks update a versioned subscription state idempotently. If billing state is unavailable, preserve privacy controls and existing read access while denying new paid-cost jobs until reconciled.
7. Admin/support roles cannot bypass consent, tenant, retention, AI, export, or delete policy. Complimentary access is represented as a dated subscription grant and audited.

## AI analysis contract

AI is a labeled optional narrative layer over deterministic aggregates. It is never required to validate an import, calculate metrics, explain formulas, assess coverage, export data, or delete data.

Before the first AI job per source/purpose/policy version, require a separate opt-in receipt that states:

- which selected sources/categories and minimized aggregate evidence will be sent;
- provider/model identity when known, purpose, retention/training posture, and known limitations;
- that provider tokens, credentials, raw archives, direct messages, and unselected raw text are excluded;
- that output may be inaccurate or culturally biased and is reflection, not diagnosis or professional advice;
- that consent can be withdrawn without losing deterministic features.

Each generation screen shows “AI-generated narrative,” source/date coverage, evidence aggregate links, provider/model/prompt/analyzer versions, generated time, limitations, and correction/delete controls. Do not silently regenerate or overwrite a narrative.

A generation consumes one credit only when validated output is stored and displayed. Provider failures, safety-validation failures, timeouts, user cancellation before completion, and internal retries consume no user credit. Regeneration consumes one credit after explicit confirmation. Unused credits do not roll over and cannot be purchased à la carte in the initial release.

Required output boundary: observational patterns may use language such as “in this selected slice.” Output must not diagnose, assign a mental-health/crisis/personality-risk score, claim causation, infer protected traits, or make employment, insurance, credit, policing, eligibility, treatment, or crisis decisions. Unsupported or unsafe output is blocked, logged without raw content, and does not consume credit.

## Cost controls and economics hypotheses

Variable-cost ceilings, excluding fixed engineering, support, taxes, refunds, app-store fees, and payment fees:

- Premium: target no more than $0.75 per active subscriber/month across storage, parsing, scheduled sync, exports, and transactional operations. At $7.99 monthly this is a 90.6% contribution margin before excluded costs.
- Premium + AI: target no more than $3.00 per active subscriber/month total variable cost. At $14.99 monthly this is an 80.0% contribution margin before excluded costs.
- These margins are scenario arithmetic, not measured economics. Instrument real cost per successful import, GB-month, sync, report, and AI generation before setting final prices.

Controls:

- Hard per-user, per-source, per-plan, and global daily/monthly budgets; queued work fails closed when caps are reached.
- Cache deterministic outputs by normalized input digest + analyzer version. Cache AI output only for the same user, consent scope, input digest, provider/model/prompt version; never share across users.
- Minimize AI payloads, cap evidence size/output tokens, allow one internal retry, and use an approved zero-retention/no-training configuration.
- Global kill switches for import parsing, connector refresh, exports, and model generation; provider spend alerts at 50%, 75%, 90%, and 100% of budget.
- No background AI generation. Scheduled refresh recalculates deterministic features only; the user explicitly requests each paid AI narrative.
- Retention caps are enforced separately for quarantine/raw, normalized, derived, exports, and AI records. Failed quarantine files follow the declared short deletion schedule.

## Consent, deletion, and retention behavior

Consent is granular by person, tenant, source, category, purpose, acquisition path, retention choice, policy-copy version, locale, and time. Optional AI and sensitive-insight consent default off. Import consent cannot be bundled with marketing, AI, scheduled refresh, or cross-account comparison.

Deletion order follows the product privacy architecture: stop jobs/revoke token; hide and invalidate insights/caches; remove features; remove normalized events; remove raw objects; crypto-erase source keys; reconcile exports, queues, vendors, and backups/key retention; retain only a non-personal audit tombstone. The user receives pending, failed, and completed states. Do not claim completion until reconciliation succeeds.

Marketing consent is independent, unchecked by default, and revocable. Product telemetry must be content-free and cannot be required for basic functionality beyond strictly necessary security/operations events.

## Honest conversion and billing UX

- Show the Free result before presenting an upgrade. Never blur, fabricate, or withhold calculated metrics to create anxiety.
- Upgrade copy names the concrete limit and benefit (for example, “Compare a second account”) rather than implying that the user's free profile is incomplete or unsafe.
- No countdown timers, preselected annual plan, disguised ads, forced AI consent, confirm-shaming, hidden fees, or cancellation mazes.
- Display monthly and total annual price with renewal cadence before purchase. Trials, if later tested, require explicit opt-in and a reminder before conversion; no default trial in the initial release.
- Cancellation is available in the same product surface as upgrade, subject to app-store billing rules, and requires no support contact.
- A failed payment never blocks export, revoke, correction, deletion, consent history, or safety information.

## Instrumentation and validation gates

Track only content-free product events: import attempted/succeeded/rejected with reason class, metrics viewed, formula/coverage opened, report generated, limit encountered, upgrade started/completed, AI consent accepted/withdrawn, AI generation succeeded/failed, downgrade/cancel/refund, export requested/completed, and deletion requested/reconciled. Do not log filenames, raw text, archive contents, prompts, model outputs, or sensitive answers.

Validate with design partners before public billing:

- Import-to-useful-result completion rate.
- Percentage opening coverage/formula explanations.
- Limit encounter to upgrade-start conversion by capability.
- Paid conversion and 30/90-day retention by tier.
- AI consent acceptance, generation success, correction/delete rate, and cost per successful narrative.
- Refund/cancellation reasons and deletion/export completion time.

Pricing decision rule: do not treat interview enthusiasm as traction. Keep the price that produces paid conversions with sustainable measured variable cost and low regret/refund signals; otherwise change package/limit before discounting.

## Acceptance tests for downstream implementation

1. Free user completes two recognized imports in 30 days; third successful promotion is denied, while rejected upload, metrics view, JSON export, revoke, and delete remain available.
2. Free user can inspect every deterministic formula, provenance link, coverage warning, and confidence/abstention state without an upgrade.
3. Free user's second active account is blocked before processing with clear limit copy; first account remains usable and exportable.
4. Premium user can compare two separately consented accounts, and the report displays unequal coverage warnings.
5. Scheduled refresh does not run for unsupported/restricted connectors, missing scopes, revoked consent, expired token, quota exhaustion, disabled kill switch, or intervals under 168 hours.
6. Premium without AI cannot submit an AI job; all deterministic functionality remains identical to Premium + AI.
7. Premium + AI's eleventh successful narrative in a billing month is denied before provider invocation. Failed/unsafe generations do not decrement quota.
8. AI job cannot start without current source/category/purpose-specific opt-in and a minimized validated aggregate payload.
9. Downgraded or payment-failed user retains read/export/revoke/delete/correction access; new over-limit imports, syncs, comparisons, and AI jobs are denied.
10. Source revocation prevents refresh/analysis immediately and removes descendants through the reconciliation workflow; re-consent does not resurrect deleted data.
11. Billing webhook replay does not double-apply plan changes or reset counters.
12. Client-side plan tampering cannot grant backend capabilities.
13. All tiers can cancel without support contact and see effective date, data-retention choice, and renewal state.
14. No diagnostic, crisis-prediction, protected-trait, causal, or professional-decision language passes narrative validation.
