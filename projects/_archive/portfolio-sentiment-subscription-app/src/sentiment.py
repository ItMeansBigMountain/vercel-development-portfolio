POSITIVE_WORDS = {
    "beat", "beats", "bullish", "growth", "gain", "gains", "profit", "profits",
    "record", "strong", "upgrade", "surge", "surges", "optimistic", "outperform",
    "expands", "expansion", "recovery", "resilient", "positive"
}

NEGATIVE_WORDS = {
    "miss", "misses", "bearish", "decline", "declines", "loss", "losses", "downgrade",
    "falls", "fall", "drops", "drop", "weak", "lawsuit", "risk", "risks", "cuts",
    "cut", "warning", "slowdown", "negative", "pressure", "concern", "concerns"
}


def score_text(text: str) -> int:
    words = [w.strip(".,:;!?()[]{}\"'").lower() for w in text.split()]
    return sum(1 for w in words if w in POSITIVE_WORDS) - sum(1 for w in words if w in NEGATIVE_WORDS)


def label(score: float) -> str:
    if score > 0.35:
        return "positive"
    if score < -0.35:
        return "negative"
    return "neutral"


def summarize_ticker(ticker: str, headlines: list[dict]) -> dict:
    related = [h for h in headlines if ticker.upper() in [x.upper() for x in h.get("tickers", [])]]
    raw_scores = [score_text(h.get("title", "") + " " + h.get("summary", "")) for h in related]
    avg = round(sum(raw_scores) / len(raw_scores), 2) if raw_scores else 0
    return {
        "ticker": ticker.upper(),
        "headline_count": len(related),
        "sentiment_score": avg,
        "sentiment_label": label(avg),
        "headlines": related[:5],
    }


def build_dashboard_payload(watchlist: list[str], headlines: list[dict]) -> dict:
    rows = [summarize_ticker(t, headlines) for t in watchlist]
    overall = round(sum(r["sentiment_score"] for r in rows) / len(rows), 2) if rows else 0
    return {
        "overall_score": overall,
        "overall_label": label(overall),
        "watchlist": rows,
    }
