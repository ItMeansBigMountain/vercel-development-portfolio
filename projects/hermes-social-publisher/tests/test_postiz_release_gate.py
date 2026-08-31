import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hermes_social_publisher.ledger import Destination, Ledger
from hermes_social_publisher.release_gate import (
    LINKEDIN_RANGE_BYTES,
    X_RANGE_BYTES,
    PostizPendingCoordinator,
    inspect_linkedin_versions,
    select_pinterest_mp4,
    verify_key_url_discovery,
    verify_ranged_upload,
    verify_stateless_mcp,
)


class FakePostizPending:
    def __init__(self):
        self.create_calls = []
        self.states = [
            {"id": "postiz-42", "state": "pending"},
            {
                "id": "postiz-42",
                "state": "completed",
                "platformPostId": "native-42",
                "url": "https://social.example/posts/native-42",
            },
        ]

    def create_post(self, payload):
        self.create_calls.append(payload)
        return {"id": "postiz-42", "state": "pending"}

    def get_post(self, postiz_id):
        assert postiz_id == "postiz-42"
        return self.states.pop(0)


class PostizReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.ledger = Ledger(Path(self.temp.name) / "ledger.sqlite3")
        self.ledger.save_destination(
            Destination("destination-1", "x", "native-account", "handle", "Name", "https://x.com", True)
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_pending_attempt_reconciles_after_interruption_without_second_native_post(self):
        postiz = FakePostizPending()
        coordinator = PostizPendingCoordinator(self.ledger, postiz)
        first = coordinator.publish(
            attempt_id="hermes-attempt-1",
            idempotency_key="asset:x:account",
            destination_id="destination-1",
            visibility="now",
            payload={"type": "now"},
        )
        self.assertEqual("postiz_pending", first["status"])
        self.assertEqual("hermes-attempt-1", first["attempt_id"])
        self.assertEqual("postiz-42", first["postiz_post_id"])

        recovered = coordinator.publish(
            attempt_id="hermes-attempt-1",
            idempotency_key="asset:x:account",
            destination_id="destination-1",
            visibility="now",
            payload={"type": "now"},
        )

        self.assertEqual("published_verified", recovered["status"])
        self.assertEqual("native-42", recovered["platform_post_id"])
        self.assertEqual(1, len(postiz.create_calls))

    def test_unknown_outcome_is_not_resubmitted(self):
        self.ledger.begin_attempt("attempt-unknown", "unknown-key", "destination-1", "now")
        postiz = FakePostizPending()
        result = PostizPendingCoordinator(self.ledger, postiz).publish(
            attempt_id="attempt-unknown",
            idempotency_key="unknown-key",
            destination_id="destination-1",
            visibility="now",
            payload={"type": "now"},
        )
        self.assertEqual("outcome_unknown", result["status"])
        self.assertEqual([], postiz.create_calls)

    def test_mcp_streamable_http_is_stateless(self):
        result = verify_stateless_mcp(
            [
                {"request_id": 1, "status": 200, "session_id": None},
                {"request_id": 2, "status": 200, "session_id": None},
            ]
        )
        self.assertTrue(result.ready, result.blockers)

    def test_key_in_url_discovery_is_404_and_evidence_is_sanitized(self):
        sensitive_value = "synthetic-sensitive-value"  # pragma: allowlist secret
        result = verify_key_url_discovery(
            {
                "/.well-known/oauth-protected-resource/mcp/anything": 404,
                "/.well-known/oauth-protected-resource": 404,
            },
            f"https://mcp.example/mcp/?key={sensitive_value}",
        )
        self.assertTrue(result.ready, result.blockers)
        self.assertNotIn(sensitive_value, repr(result))
        self.assertIn("%5BREDACTED%5D", result.evidence[0])

    def test_x_uses_one_megabyte_ranged_reads(self):
        size = X_RANGE_BYTES * 2 + 7
        result = verify_ranged_upload(
            size,
            ("bytes=0-1048575", "bytes=1048576-2097151", "bytes=2097152-2097158"),
            X_RANGE_BYTES,
        )
        self.assertTrue(result.ready, result.blockers)

    def test_linkedin_uses_two_megabyte_ranged_reads(self):
        size = LINKEDIN_RANGE_BYTES + 3
        result = verify_ranged_upload(
            size,
            ("bytes=0-2097151", "bytes=2097152-2097154"),
            LINKEDIN_RANGE_BYTES,
        )
        self.assertTrue(result.ready, result.blockers)

    def test_pinterest_selects_mp4_instead_of_first_cover(self):
        selected = select_pinterest_mp4(
            [
                {"path": "https://media.example/cover.jpg"},
                {"path": "https://media.example/video.MP4?signature=redacted"},
            ]
        )
        self.assertIn("video.MP4", selected["path"])

    def test_linkedin_source_gate_rejects_sunset_version(self):
        source = Path(self.temp.name) / "linkedin.provider.ts"
        source.write_text("headers: {'Linkedin-Version': '202508'}", encoding="utf-8")
        result = inspect_linkedin_versions(self.temp.name)
        self.assertFalse(result.ready)
        self.assertIn("sunset LinkedIn versions found: 202508", result.blockers)

    def test_linkedin_source_gate_accepts_supported_version(self):
        source = Path(self.temp.name) / "linkedin.provider.ts"
        source.write_text("headers: {'Linkedin-Version': '202601'}", encoding="utf-8")
        result = inspect_linkedin_versions(self.temp.name)
        self.assertTrue(result.ready, result.blockers)


if __name__ == "__main__":
    unittest.main()