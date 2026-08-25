"""Normalize RSS/news records into research-only catalyst signals.

This module does not access brokerage accounts or make execution decisions. Scores
are deterministic headline heuristics intended as one input to human/policy-gated
research.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
import json
import re
from typing import Any, Iterable, Mapping
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

BULLISH_WORDS = frozenset(
    {"approval", "approved", "beat", "beats", "growth", "launch", "launches", "partnership", "record", "upgrade", "upgraded", "win", "wins"}
)
BEARISH_WORDS = frozenset(
    {"cut", "cuts", "downgrade", "downgraded", "investigation", "lawsuit", "layoff", "layoffs", "miss", "misses", "probe", "recall", "recalls", "warning"}
)
CATALYST_PATTERNS = (
    ("earnings", frozenset({"earnings", "revenue", "guidance", "quarter", "eps", "beat", "beats", "miss", "misses"})),
    ("regulatory", frozenset({"fda", "approval", "approved", "regulator", "regulatory", "sec", "antitrust"})),
    ("legal", frozenset({"lawsuit", "probe", "investigation", "settlement", "court"})),
    ("analyst_rating", frozenset({"upgrade", "upgraded", "downgrade", "downgraded", "price", "target"})),
    ("leadership", frozenset({"ceo", "cfo", "resigns", "appointed", "leadership"})),
    ("product", frozenset({"launch", "launches", "product", "partnership", "contract"})),
    ("supply_chain", frozenset({"supply", "shortage", "factory", "shipment", "recall", "recalls"})),
    ("macro", frozenset({"fed", "inflation", "rates", "tariff", "gdp", "jobs"})),
)
MATERIALITY_TERMS = frozenset(
    {"approval", "bankruptcy", "fraud", "investigation", "lawsuit", "merger", "recall", "recalls", "settlement"}
)
TRACKING_QUERY_KEYS = frozenset({"fbclid", "gclid", "mc_cid", "mc_eid"})
_TAG_RE = re.compile(r"<[^>]+>")
_WORD_RE = re.compile(r"[a-zA-Z]+")
_TITLE_TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")
_TICKER_RE = re.compile(r"^[A-Z][A-Z0-9.\-]{0,9}$")


def _clean_text(value: Any) -> str:
    return " ".join(unescape(_TAG_RE.sub(" ", str(value or ""))).split())


def _parse_datetime(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = parsedate_to_datetime(text)
        except (TypeError, ValueError, OverflowError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _ticker(value: Any) -> str:
    ticker = str(value or "").strip().upper()
    return ticker if _TICKER_RE.fullmatch(ticker) else ""


def _classify(text: str) -> tuple[list[str], str, float]:
    words = _WORD_RE.findall(text.lower())
    word_set = set(words)
    bullish = sum(word in BULLISH_WORDS for word in words)
    bearish = sum(word in BEARISH_WORDS for word in words)
    raw = bullish - bearish
    score = round(max(-1.0, min(1.0, raw / 4)), 3)
    direction = "bullish" if score > 0.08 else "bearish" if score < -0.08 else "neutral"
    catalyst_tags = [name for name, keys in CATALYST_PATTERNS if word_set & keys] or ["other"]
    return catalyst_tags, direction, score


def _canonical_url(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    try:
        parts = urlsplit(text)
        host = (parts.hostname or "").lower()
        if not parts.scheme or not host:
            return text
        if host.startswith("www."):
            host = host[4:]
        port = f":{parts.port}" if parts.port else ""
    except ValueError:
        return text
    query = urlencode(
        [
            (key, val)
            for key, val in parse_qsl(parts.query, keep_blank_values=True)
            if key.lower() not in TRACKING_QUERY_KEYS and not key.lower().startswith("utm_")
        ]
    )
    return urlunsplit((parts.scheme.lower(), host + port, parts.path.rstrip("/"), query, ""))


def _normalized_title(title: str) -> str:
    return " ".join(_TITLE_TOKEN_RE.findall(title.casefold()))


def _publisher_domain(url: str) -> str:
    try:
        host = (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def _ticker_evidence(item: Mapping[str, Any], ticker: str, text: str) -> str | None:
    explicit = _ticker(item.get("ticker") or item.get("symbol"))
    if explicit:
        return "explicit_ticker" if explicit == ticker else None
    if re.search(rf"(?<![A-Z0-9]){re.escape(ticker)}(?![A-Z0-9])", text.upper()):
        return "ticker_mention"
    return None


def _materiality(text: str) -> dict[str, Any]:
    matched = sorted(set(_WORD_RE.findall(text.lower())) & MATERIALITY_TERMS)
    return {
        "level": "high" if matched else "unassessed",
        "matched_terms": matched,
        "basis": "headline_keyword_evidence" if matched else "no_materiality_keyword_evidence",
    }


def build_catalyst_feed(
    items: Iterable[Mapping[str, Any] | None] | None,
    *,
    ticker: str,
    source: str = "unknown",
    now: datetime | None = None,
    stale_after_hours: float = 48.0,
    future_skew_minutes: float = 5.0,
) -> list[dict[str, Any]]:
    """Normalize, classify, and deduplicate records for one requested ticker."""
    requested_ticker = _ticker(ticker)
    if not requested_ticker:
        return []
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    current = current.astimezone(timezone.utc)
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    normalized: list[dict[str, Any]] = []

    for item in items or ():
        if not isinstance(item, Mapping):
            continue
        title = _clean_text(item.get("title") or item.get("headline"))
        if not title:
            continue
        summary = _clean_text(item.get("description") or item.get("summary"))
        relevance_evidence = _ticker_evidence(item, requested_ticker, f"{title} {summary}")
        if relevance_evidence is None:
            continue
        url = _canonical_url(item.get("url") or item.get("link"))
        normalized_title = _normalized_title(title)
        if (url and url in seen_urls) or normalized_title in seen_titles:
            continue
        if url:
            seen_urls.add(url)
        seen_titles.add(normalized_title)

        published = _parse_datetime(item.get("published_at") or item.get("publishedAt") or item.get("pubDate"))
        seconds_old = (current - published).total_seconds() if published else None
        timestamp_valid = published is not None and seconds_old is not None and seconds_old >= -(future_skew_minutes * 60)
        age_hours = round(max(0.0, seconds_old / 3600), 2) if timestamp_valid and seconds_old is not None else None
        is_stale = not timestamp_valid or age_hours is None or age_hours > stale_after_hours
        catalyst_tags, direction, score = _classify(f"{title} {summary}")
        is_scoreable = not is_stale
        aggregator = str(source).strip() or "unknown"
        publisher = _clean_text(item.get("publisher") or item.get("creator")) or "unknown"
        normalized.append(
            {
                "ticker": requested_ticker,
                "relevance_evidence": relevance_evidence,
                "title": title,
                "summary": summary,
                "url": url,
                "source": publisher if publisher != "unknown" else aggregator,
                "aggregator": aggregator,
                "publisher": publisher,
                "publisher_domain": _publisher_domain(url),
                "source_quality": "unverified",
                "corroboration_count": 0,
                "published_at": published.isoformat() if published else None,
                "age_hours": age_hours,
                "timestamp_valid": timestamp_valid,
                "is_stale": is_stale,
                "is_scoreable": is_scoreable,
                "catalyst_type": catalyst_tags[0],
                "catalyst_tags": catalyst_tags,
                "direction": direction,
                "catalyst_score": score if is_scoreable else None,
                "materiality": _materiality(f"{title} {summary}"),
                "research_only": True,
            }
        )
    return normalized


def parse_rss(xml_body: bytes | str, *, ticker: str, source: str = "Yahoo Finance") -> list[dict[str, Any]]:
    """Parse RSS XML and return normalized records; malformed XML returns no signals."""
    if not xml_body:
        return []
    try:
        root = ET.fromstring(xml_body)
    except (ET.ParseError, TypeError, ValueError):
        return []
    raw_items = []
    for item in root.findall("./channel/item"):
        creator = next((child.text for child in item if child.tag.rsplit("}", 1)[-1] == "creator"), None)
        raw_items.append(
            {
                "title": item.findtext("title"),
                "description": item.findtext("description"),
                "url": item.findtext("link"),
                "pubDate": item.findtext("pubDate"),
                "publisher": creator,
            }
        )
    return build_catalyst_feed(raw_items, ticker=ticker, source=source)


def fetch_yahoo_feed(ticker: str, *, timeout: float = 12.0, limit: int = 8) -> list[dict[str, Any]]:
    """Fetch Yahoo Finance RSS for a ticker without brokerage/API credentials."""
    normalized_ticker = _ticker(ticker)
    if not normalized_ticker:
        return []
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={quote(normalized_ticker)}&region=US&lang=en-US"
    request = Request(url, headers={"User-Agent": "hermes-trading-journal/1.0"})
    with urlopen(request, timeout=timeout) as response:
        body = response.read()
    return parse_rss(body, ticker=normalized_ticker)[: max(0, limit)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch research-only news catalysts for a ticker")
    parser.add_argument("ticker")
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()
    print(json.dumps(fetch_yahoo_feed(args.ticker, timeout=args.timeout, limit=args.limit), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
