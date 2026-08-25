# Post-Morning Scan: Gap-Mover Review Discipline

Use this note when a scheduled Agentic post-morning scan finds a liquid daily mover that technically fits the autonomous policy but is already extended intraday.

## Pattern observed

- Account state and autonomous policy can be clean: Agentic account readable, value above kill switch, buying power known, candidate tradable/fractional, and risk within the ~$2 target.
- A `review_equity_order` preview may return no broker alerts for a small starter order.
- That still does **not** mean the scan should place the order. Strategy quality remains separate from broker acceptability.

## Recommended handling

1. Treat order review as a sizing/compliance check, not an execution obligation.
2. For same-day gap leaders, check whether the entry is a chase:
   - price already far above prior close or breakout base,
   - invalidation requires a wide stop relative to account risk,
   - no clean retest/pullback/support hold yet,
   - catalyst is broad/news-derived rather than a confirmed company-specific catalyst.
3. If the math is acceptable but entry quality is poor, journal the reviewed setup and explicitly choose **no trade / wait for retest**.
4. Include the required market-data disclosure from the review verbatim in both the report and journal.
5. Keep existing positions on hold/management rules rather than adding exposure just because buying power remains.

## Report language

Use concise wording such as:

- `Reviewed but not placed: setup fits policy math, but entry is extended after a same-day gap; wait for pullback/retest.`
- `Broker review passed; strategy gate failed on chase risk.`

This preserves autonomous authority while preventing the cron job from forcing trades in momentum gaps.