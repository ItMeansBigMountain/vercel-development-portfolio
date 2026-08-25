# Robinhood Historical Response Normalization

Use this when building compact post-morning or portfolio scanners through the direct MCP registry.

## Durable normalization pattern

`get_equity_historicals` may return `results` as either:

- A dictionary keyed by symbol, or
- A list of per-symbol records.

Do not assume one shape. Normalize before computing indicators:

1. Decode the outer MCP wrapper (`structuredContent.data` or JSON nested under `result`).
2. Inspect `results`.
3. If it is a dictionary, iterate key/value pairs.
4. If it is a list, derive the symbol defensively from `record.symbol`, `record.instrument.symbol`, or another documented symbol field; skip and log records whose symbol cannot be resolved.
5. Resolve candles from the documented candle/bar field and validate that OHLC arrays contain enough observations before calculating SMA, ATR, highs/lows, or average volume.
6. Persist a compact `data_gaps` list rather than silently returning an empty indicator map.

## Failure-handling rule

If candidate historical normalization fails but account, position, order, and live quote calls succeeded, broker state can still be certain. However, do not place a new trade whose risk plan depends on missing historical structure. Continue reporting live account/market data, label candidate technicals as incomplete, and default to no trade unless another verified data source supplies the required levels.

## Scanner verification

Before trusting a scanner run, assert:

- At least one requested benchmark produced candles.
- Every reported SMA/ATR value identifies its source symbol and sample length.
- Missing symbols appear in `data_gaps`.
- An empty indicator map is treated as a scanner failure, not as evidence that no candidates exist.
