# Order-History Counterfactual Review

Use this when the user asks whether prior Robinhood orders were good decisions given today's price.

## Evidence collection

1. Verify the intended account; never mix accounts.
2. Fetch complete equity order history covering the review period, including buys and sells—not only current positions or recent fills.
3. Fetch live quotes for every symbol in the reconstructed history plus current positions.
4. Check open-ish states (`new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled`) separately so pending exposure is not mistaken for a completed decision.
5. Prefer broker realized-P&L/tax-lot tools when available; use order reconstruction as an independently checkable approximation.
6. Record quote timestamps and clearly label whether the comparison uses intraday live prices or an official close.

## Reconstruction math

For each symbol over the chosen review window:

```text
buy_cost = Σ(buy execution_price × buy execution_quantity) + buy fees
sell_proceeds = Σ(sell execution_price × sell execution_quantity) - sell fees
remaining_quantity = total_bought_quantity - total_sold_quantity
actual_total_pnl = sell_proceeds + remaining_quantity × current_price - buy_cost
hold_all_pnl = total_bought_quantity × current_price - buy_cost
counterfactual_gap = actual_total_pnl - hold_all_pnl
```

A positive `counterfactual_gap` means the actual sells outperformed holding every purchased share to today's mark. A negative value means holding would have produced a better marked result.

For current open lots, report mark-to-market P&L separately:

```text
open_pnl = current_quantity × (current_price - current_average_price)
```

Do not add current open P&L to `actual_total_pnl`; it is already represented by `remaining_quantity × current_price`.

## Interpretation discipline

- A hold-all comparison is hindsight, not proof that an exit was irrational when made.
- Judge process separately: Was the original thesis invalidated? Was a documented stop breached? Did fundamentals/catalysts change? Was the replacement materially better after correlation and entry-extension risk?
- Separate **selection quality**, **entry quality**, **exit quality**, **sizing**, and **churn**. A stock recovering later does not automatically make the exit bad.
- Look for repeated patterns across trades rather than overfitting one winner or loser: selling ordinary volatility, repurchasing higher, rotating without a superior confirmed setup, or widening/ignoring invalidations.
- Compare against relevant benchmarks over the same holding interval when historical data is available; raw positive P&L can still represent poor opportunity cost.
- State assumptions and limitations: incomplete start dates, transfers, splits, mergers, dividends, partial fills, fees, wash sales, and missing tax lots can invalidate simple order arithmetic.
- Never imply the counterfactual was knowable in advance or guaranteed.

## Recommended output

1. Current account and open-order state.
2. Current holdings with entry, live mark, dollar and percentage P&L.
3. Largest unfavorable and favorable counterfactual gaps.
4. Process diagnosis supported by repeated evidence.
5. Concrete playbook changes (confirmation rules, invalidation handling, rotation threshold, re-entry rule).
6. Explicit note that the comparison is hindsight and not financial advice.
