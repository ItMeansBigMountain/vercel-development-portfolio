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
        self.assertEqual(article["relevance_evidence"], "ticker_mention")
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

    def test_explicit_matching_ticker_is_recorded_as_relevance_evidence(self):
        now = datetime(2026, 8, 25, 16, tzinfo=timezone.utc)
        feed = build_catalyst_feed(
            [{"title": "Company launches product", "symbol": "AAPL", "publishedAt": "2026-08-25T15:00:00Z"}],
            ticker="AAPL",
            now=now,
        )

        self.assertEqual(feed[0]["relevance_evidence"], "explicit_ticker")

    def test_rejects_rss_row_without_requested_ticker_evidence(self):
        xml = b"""<rss><channel><item>
        <title>TSLA recalls 50,000 vehicles</title>
        <link>https://news.example/story</link>
        <pubDate>Tue, 25 Aug 2026 15:00:00 GMT</pubDate>
        </item></channel></rss>"""

        self.assertEqual(parse_rss(xml, ticker="AAPL"), [])

    def test_future_timestamp_beyond_skew_is_invalid_stale_and_non_scoreable(self):
        now = datetime(2026, 8, 25, 16, tzinfo=timezone.utc)
        feed = build_catalyst_feed(
            [{"title": "AAPL wins approval", "publishedAt": "2026-08-27T15:00:00Z"}],
            ticker="AAPL",
            now=now,
        )

        self.assertEqual(len(feed), 1)
        self.assertFalse(feed[0]["timestamp_valid"])
        self.assertTrue(feed[0]["is_stale"])
        self.assertFalse(feed[0]["is_scoreable"])
        self.assertIsNone(feed[0]["catalyst_score"])

    def test_canonical_url_and_normalized_title_suppress_duplicates(self):
        now = datetime(2026, 8, 25, 16, tzinfo=timezone.utc)
        feed = build_catalyst_feed(
            [
                {"title": "AAPL launches product", "url": "https://EXAMPLE.com/story/?utm_source=x#top", "publishedAt": "2026-08-25T15:00:00Z"},
                {"title": "AAPL launches product!", "url": "https://mirror.example/copy", "publishedAt": "2026-08-25T15:10:00Z"},
            ],
            ticker="AAPL",
            now=now,
        )

        self.assertEqual(len(feed), 1)
        self.assertEqual(feed[0]["url"], "https://example.com/story")

    def test_title_deduplication_preserves_materially_different_numbers(self):
        now = datetime(2026, 8, 25, 16, tzinfo=timezone.utc)
        feed = build_catalyst_feed(
            [
                {"title": "AAPL reports Q1 2026 earnings", "url": "https://one.example/story", "publishedAt": "2026-08-25T15:00:00Z"},
                {"title": "AAPL reports Q2 2026 earnings", "url": "https://two.example/story", "publishedAt": "2026-08-25T15:10:00Z"},
            ],
            ticker="AAPL",
            now=now,
        )

        self.assertEqual(len(feed), 2)

    def test_mixed_events_keep_all_tags_and_materiality_evidence(self):
        now = datetime(2026, 8, 25, 16, tzinfo=timezone.utc)
        feed = build_catalyst_feed(
            [{"title": "AAPL faces major lawsuit but wins FDA approval", "publishedAt": "2026-08-25T15:00:00Z"}],
            ticker="AAPL",
            now=now,
        )

        article = feed[0]
        self.assertEqual(article["catalyst_tags"], ["regulatory", "legal"])
        self.assertEqual(article["materiality"]["level"], "high")
        self.assertIn("lawsuit", article["materiality"]["matched_terms"])
        self.assertIn("approval", article["materiality"]["matched_terms"])

    def test_macro_and_company_event_tags_are_not_collapsed(self):
        now = datetime(2026, 8, 25, 16, tzinfo=timezone.utc)
        feed = build_catalyst_feed(
            [{"title": "AAPL earnings beat as Fed cuts rates", "publishedAt": "2026-08-25T15:00:00Z"}],
            ticker="AAPL",
            now=now,
        )

        self.assertEqual(feed[0]["catalyst_tags"], ["earnings", "macro"])

    def test_exposes_actual_publisher_domain_and_unverified_source_fields(self):
        now = datetime(2026, 8, 25, 16, tzinfo=timezone.utc)
        feed = build_catalyst_feed(
            [{
                "title": "AAPL launches product",
                "url": "https://www.reuters.com/technology/story?utm_campaign=x",
                "publisher": "Reuters",
                "publishedAt": "2026-08-25T15:00:00Z",
            }],
            ticker="AAPL",
            source="Yahoo Finance",
            now=now,
        )

        article = feed[0]
        self.assertEqual(article["aggregator"], "Yahoo Finance")
        self.assertEqual(article["publisher"], "Reuters")
        self.assertEqual(article["publisher_domain"], "reuters.com")
        self.assertEqual(article["source_quality"], "unverified")
        self.assertEqual(article["corroboration_count"], 0)

    def test_old_or_invalid_timestamp_cannot_retain_a_score(self):
        now = datetime(2026, 8, 25, 16, tzinfo=timezone.utc)
        feed = build_catalyst_feed(
            [
                {"title": "AAPL faces lawsuit", "publishedAt": "not-a-date"},
                {"title": "AAPL launches product", "publishedAt": "2026-08-22T12:00:00Z"},
            ],
            ticker="AAPL",
            now=now,
        )

        self.assertTrue(all(not item["is_scoreable"] for item in feed))
        self.assertTrue(all(item["catalyst_score"] is None for item in feed))


if __name__ == "__main__":
    unittest.main()
