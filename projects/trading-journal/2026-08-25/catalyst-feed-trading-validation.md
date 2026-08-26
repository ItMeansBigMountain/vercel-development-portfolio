# Catalyst Feed Trading Validation — 2026-08-25

## Revalidation after remediation — 2026-08-25T20:00:56Z

**Disposition: PASS for retirement readiness as a strict, low-trust discovery feed; NOT approved as a direct autonomous-policy candidate score, order-preview trigger, or execution trigger.** No brokerage tools, previews, orders, or live trades were used.

Independent commands executed from `/opt/data/HeRmEz/projects/trading-journal`:

- `python3 -m unittest tests.test_catalyst_feed -v` — PASS, 13/13.
- `python3 -m compileall -q scanner tests/test_catalyst_feed.py` — PASS/no output.
- Representative in-memory policy fixtures — PASS: four accepted records; unrelated TSLA-for-AAPL row and normalized-title mirror duplicate rejected; mixed regulatory/legal and earnings/macro tags preserved; materially future record invalid, stale, non-scoreable, and score removed; publisher/domain exposed while source quality remained explicitly unverified with zero corroboration.
- `git diff --check -- projects/trading-journal` — PASS/no output.

Valid remediated examples:

- Ordinary RSS rows without a standalone requested-ticker mention are rejected; an explicit mismatched structured ticker is also rejected.
- Canonical URL cleanup removes tracking parameters/fragments, and normalized-title deduplication suppresses punctuation-only mirror headlines while preserving materially different numeric events.
- Publication times beyond the five-minute skew tolerance have `timestamp_valid=false`, `is_stale=true`, `is_scoreable=false`, and `catalyst_score=null`; stale or malformed dates cannot retain ranking scores.
- Multi-label `catalyst_tags` preserve mixed company/legal/regulatory/macro evidence. `materiality` exposes only transparent keyword evidence rather than invented confidence.
- Aggregator, publisher, and publisher domain are distinct. `source_quality=unverified` and `corroboration_count=0` honestly prevent inferred authority.
- Every accepted record remains `research_only=true`; the module has no broker, order-review, or execution path.

Residual limitations are explicit and policy-safe: ticker text matching is not company-name entity resolution; materiality and direction remain headline heuristics; source authority and corroboration are not verified; and broad-market regime, sector/relative-strength flows, technicals, fundamentals, volume, liquidity, live account/open-order state, invalidation, sizing, and reward/risk are absent. Therefore consumers may use this output only to discover leads. They must independently verify the entity and source and run every external autonomous-policy gate before candidate scoring, preview, or execution. A catalyst record or `catalyst_score` alone must never cause broker action.

Policy-gate result after remediation:

- Research-only isolation and no implied execution: **PASS**.
- Ticker relevance evidence, future/stale handling, conservative deduplication, multi-label categorization, and non-scoreable invalid data: **PASS for discovery semantics**.
- Source quality/corroboration: **PASS as explicit unknown/unverified metadata**, not as verified evidence.
- Broad-market/sector, technical, fundamental, liquidity, account, and risk gates: **EXTERNAL AND MANDATORY**; absence is acceptable only because the README consumer contract forbids direct scoring/execution.
- Direct autonomous-policy scorecard or broker trigger: **PROHIBITED**.
- Migration/retirement dependency: **PASS**, provided the downstream operations task preserves the documented research-only contract and recoverable archive.

The original failed validation is retained below as historical evidence of the defects that prompted remediation.

## Scope and disposition

Validated `scanner/catalyst_feed.py`, its focused tests, README claims, and compatibility with `playbook/autonomous-policy.md`. No brokerage tools, previews, orders, or live trades were used.

**Disposition: FAIL for autonomous-policy candidate scoring or retirement readiness.**

The module passes its four focused software tests and is appropriately isolated as `research_only`, but the current semantics are not reliable enough to supply the policy scorecard's catalyst/revisions dimension without an additional verification layer. It may remain a low-trust discovery input only. The standalone stockNews system should not be retired on the strength of this validation until the blocking defects below are remediated and revalidated.

## Commands and results

Executed from `/opt/data/HeRmEz/projects/trading-journal` at `2026-08-25T19:39:05Z`:

- `python3 -m unittest tests.test_catalyst_feed -v` — PASS, 4/4.
- Representative in-memory fixtures through `build_catalyst_feed(...)` — exposed relevance, duplicate, mixed-event, and future-timestamp failures described below.
- `python3 -m scanner.catalyst_feed AAPL --limit 3` — PASS as a local-only outbound Yahoo RSS probe; returned three normalized records. This is not a deployed URL or broker-integrated service.

## Valid examples

- Exact duplicate `{same URL, same normalized title}` is suppressed.
- Explicit symbol mismatch (`symbol=TSLA`, requested `AAPL`) is rejected.
- Missing/invalid dates are marked stale.
- A 1-hour-old `MSFT beats earnings estimates` fixture is categorized as earnings and fresh.
- Malformed XML and empty inputs return no fabricated signals.
- Every output record includes `research_only=true`; the module contains no broker/order path.

## Blocking invalid examples

1. **Ticker relevance is not established for ordinary RSS rows.** A title `TSLA recalls 50,000 vehicles` with no explicit symbol was emitted as an AAPL bearish supply-chain catalyst. Yahoo RSS rows parsed by this module never carry an explicit ticker, so feed membership is being treated as proof of relevance.
2. **Future timestamps are accepted as fresh.** An item dated 47 hours in the future was assigned `age_hours=0.0` and `is_stale=false`. Clock-skew tolerance and a future-date rejection/invalid flag are required.
3. **Duplicate handling is too narrow.** The same `AAPL launches product` headline at two mirror URLs produced two signals. Conversely, the same URL with materially different titles is retained twice. Canonical URL normalization and title/content similarity rules are required.
4. **Direction and category can misrepresent mixed events.** `AAPL faces major lawsuit but wins approval` became bullish/regulatory because category precedence and word counts discard the legal conflict. `AAPL earnings beat as Fed cuts rates` became neutral/earnings, conflating company and macro catalysts.
5. **No severity/materiality field exists.** The task requires categorization/severity, but output provides only direction and a bounded word-count score. A routine product mention and a material approval can receive the same `0.25` score.
6. **Source quality is unmodeled.** `source` is always the aggregator label (`Yahoo Finance`) even when the actual publisher differs. There is no publisher/domain extraction, primary-source flag, corroboration count, or trust tier. The live sample included syndicated/commentary publishers, which should not be weighted like SEC filings, issuer releases, or confirmed wire reporting.
7. **No broad-market or sector context exists.** The policy requires SPY/QQQ/IWM regime, relevant sector ETF, relative strength, and sector-flow context. The feed cannot provide or attest to those gates.
8. **Staleness is informational only.** Stale records still retain nonzero `catalyst_score`; downstream consumers could rank them unless they independently enforce `is_stale=false`.

## Policy-gate assessment

- Research-only / no implied execution: **PASS**.
- No fabricated fallback signals: **PASS**.
- Timestamp normalization and stale detection: **PARTIAL / FAIL** because future dates are treated as fresh.
- Ticker relevance: **FAIL**.
- Duplicate resistance: **PARTIAL / FAIL**.
- Catalyst category, direction, and severity: **FAIL** for decision-grade use.
- Source quality and corroboration: **FAIL**.
- Broad-market/sector context: **FAIL**.
- Supports autonomous-policy scorecard directly: **FAIL**.

A safe downstream contract must treat these records as unverified discovery leads, exclude stale/invalid/future-dated items, require ticker/entity relevance and source verification, and combine them with live technicals, fundamentals, market regime, sector-relative strength, volume, liquidity, invalidation, and reward/risk before candidate scoring. A feed score alone must never trigger an order preview or execution.

## Required remediation before revalidation

1. Add explicit relevance evidence and reject or downgrade rows without verified symbol/entity linkage.
2. Reject/flag publication times beyond a documented clock-skew tolerance.
3. Canonicalize tracking URLs and add conservative normalized-title duplicate suppression.
4. Separate catalyst tags from direction; support multi-label events and materiality/severity with transparent evidence.
5. Extract actual publisher/domain and expose source-quality/corroboration metadata without inventing trust.
6. Make stale/invalid records non-scoreable for downstream candidate ranking.
7. Document a strict consumer contract: discovery only; broad-market, sector, technical, fundamental, liquidity, risk, and live broker gates remain mandatory and external.
8. Add focused fixtures for every invalid example above.
