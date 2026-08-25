import unittest
from datetime import datetime, timezone

from scanner.catalyst_feed import build_catalyst_feed, parse_rss


class CatalystFeedTests(unittest.TestCase):
    def test_parses_rss_and_scores_relevant_catalysts(self):
        xml = b"""<?xml version='1.0'?><rss><channel>
        <item><title>AAPL wins FDA approval for health feature</title>
        <description><![CDATA[<p>Apple launches the approved feature.</p>]]></description>
        <link>https://example.com/aapl</link><pubDate>Tue, 25 Aug 2026 15:00:00 GMT</pubDate></item>
        </channel></rss>"""

        articles = parse_rss(xml, ticker="aapl", source="Yahoo Finance")

        self.assertEqual(len(articles), 1)
        article = articles[0]
        self.assertEqual(article["ticker"], "AAPL")
        self.assertEqual(article["catalyst_type"], "regulatory")
        self.assertEqual(article["direction"], "bullish")
        self.assertGreater(article["catalyst_score"], 0)
        self.assertEqual(article["published_at"], "2026-08-25T15:00:00+00:00")
        self.assertNotIn("<p>", article["summary"])

    def test_normalizes_deduplicates_and_rejects_malformed_items(self):
        now = datetime(2026, 8, 25, 16, tzinfo=timezone.utc)
        raw = [
            {"title": "MSFT beats earnings estimates", "url": "https://example.com/1", "publishedAt": "2026-08-25T15:00:00Z"},
            {"title": "MSFT beats earnings estimates", "url": "https://example.com/1", "publishedAt": "2026-08-25T15:00:00Z"},
            {"title": "", "url": "https://example.com/bad"},
            None,
        ]

        feed = build_catalyst_feed(raw, ticker="msft", source="fixture", now=now)

        self.assertEqual(len(feed), 1)
        self.assertEqual(feed[0]["catalyst_type"], "earnings")
        self.assertEqual(feed[0]["age_hours"], 1.0)
        self.assertFalse(feed[0]["is_stale"])

    def test_handles_empty_input_and_marks_old_or_invalid_dates_stale(self):
        now = datetime(2026, 8, 25, 16, tzinfo=timezone.utc)
        self.assertEqual(build_catalyst_feed([], ticker="AAPL", now=now), [])
        self.assertEqual(parse_rss(b"<rss><broken>", ticker="AAPL"), [])
        feed = build_catalyst_feed(
            [
                {"title": "AAPL faces lawsuit", "publishedAt": "not-a-date"},
                {"title": "AAPL launches product", "publishedAt": "2026-08-22T12:00:00Z"},
            ],
            ticker="AAPL",
            now=now,
        )
        self.assertEqual(len(feed), 2)
        self.assertTrue(all(item["is_stale"] for item in feed))
        self.assertIsNone(feed[0]["published_at"])

    def test_filters_explicitly_unrelated_tickers(self):
        feed = build_catalyst_feed(
            [{"title": "TSLA recalls vehicles", "symbol": "TSLA"}],
            ticker="AAPL",
        )
        self.assertEqual(feed, [])


if __name__ == "__main__":
    unittest.main()
