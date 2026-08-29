import json
import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hermes_social_publisher.bluesky import (
    AuthorizationRequired,
    DestinationMismatch,
    PublisherService,
)
from hermes_social_publisher.ledger import Ledger


class FakePostiz:
    def __init__(self, integrations=None, response=None, error=None):
        self.integrations = integrations or []
        self.response = response
        self.error = error
        self.calls = []

    def list_integrations(self):
        return self.integrations

    def create_post(self, payload):
        self.calls.append(payload)
        if self.error:
            raise self.error
        return self.response


class FakeIdentityProbe:
    def __init__(self, identity=None, authorization_url=None):
        self.identity = identity
        self.authorization_url = authorization_url

    def verify(self, integration):
        if self.authorization_url:
            raise AuthorizationRequired(
                "bluesky_owner_action",
                "Connect Bluesky in Postiz with a dedicated app password",
                self.authorization_url,
            )
        return self.identity


class CapturingReporter:
    def __init__(self):
        self.messages = []

    def send(self, report):
        self.messages.append(report)


class BlueskyFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.db_path = Path(self.temp.name) / "publisher.sqlite3"
        self.ledger = Ledger(self.db_path)
        self.reporter = CapturingReporter()
        self.integration = {
            "id": "postiz-integration-1",
            "identifier": "bluesky",
            "name": "Hermes Pilot",
            "profile": "pilot.example",
            "disabled": False,
        }
        self.identity = {
            "did": "did:plc:immutable123",
            "handle": "pilot.example",
            "display_name": "Hermes Pilot",
            "service_url": "https://bsky.social",
        }
        self.expected = dict(self.identity)

    def tearDown(self):
        self.temp.cleanup()

    def service(self, postiz, probe=None):
        return PublisherService(
            postiz=postiz,
            identity_probe=probe or FakeIdentityProbe(self.identity),
            ledger=self.ledger,
            reporter=self.reporter,
        )

    def test_successful_onboarding_and_draft_publication_are_recorded_once(self):
        postiz = FakePostiz(
            [self.integration],
            [{"postId": "draft-123", "integration": "postiz-integration-1"}],
        )
        service = self.service(postiz)
        destination = service.onboard("postiz-integration-1", self.expected)

        first = service.publish(
            destination.id,
            "Original rights-safe copy",
            visibility="draft",
            idempotency_key="pilot-attempt-1",
        )
        second = service.publish(
            destination.id,
            "Original rights-safe copy",
            visibility="draft",
            idempotency_key="pilot-attempt-1",
        )

        self.assertEqual("draft-123", first.postiz_post_id)
        self.assertEqual(first.attempt_id, second.attempt_id)
        self.assertEqual(1, len(postiz.calls))
        self.assertEqual("draft", postiz.calls[0]["type"])
        self.assertEqual("bluesky", postiz.calls[0]["posts"][0]["settings"]["__type"])
        stored = self.ledger.get_attempt(first.attempt_id)
        self.assertEqual("accepted_draft", stored["status"])
        self.assertEqual([{"postId": "draft-123", "integration": "postiz-integration-1"}], stored["response"])
        self.assertNotIn("secret", json.dumps(self.reporter.messages).lower())

    def test_destination_mismatch_disables_onboarding(self):
        wrong = dict(self.expected, did="did:plc:someone-else")
        service = self.service(FakePostiz([self.integration]))

        with self.assertRaises(DestinationMismatch):
            service.onboard("postiz-integration-1", wrong)

        self.assertIsNone(self.ledger.get_destination("postiz-integration-1"))

    def test_missing_post_id_and_url_is_recorded_as_unverified(self):
        service = self.service(FakePostiz([self.integration], [{"integration": "postiz-integration-1"}]))
        destination = service.onboard("postiz-integration-1", self.expected)

        result = service.publish(
            destination.id,
            "Original copy",
            visibility="now",
            idempotency_key="missing-proof",
            allow_public=True,
        )

        self.assertEqual("unverified_response", result.status)
        self.assertIsNone(result.postiz_post_id)
        self.assertIsNone(result.url)
        self.assertEqual("unverified_response", self.ledger.get_attempt(result.attempt_id)["status"])

    def test_api_failure_is_recorded_and_secrets_are_redacted(self):
        token = "pos_SUPERSECRET"
        error = RuntimeError(f"upstream rejected Authorization: {token}")
        service = self.service(FakePostiz([self.integration], error=error))
        destination = service.onboard("postiz-integration-1", self.expected)

        with self.assertRaises(RuntimeError):
            service.publish(
                destination.id,
                "Original copy",
                visibility="draft",
                idempotency_key="api-failure",
            )

        attempt = self.ledger.get_by_idempotency_key("api-failure")
        rendered = json.dumps(attempt) + json.dumps(self.reporter.messages)
        self.assertNotIn(token, rendered)
        self.assertIn("[REDACTED]", rendered)
        self.assertEqual("api_failure", attempt["status"])

    def test_irreducible_human_authorization_is_a_structured_blocker(self):
        probe = FakeIdentityProbe(authorization_url="https://bsky.app/settings/app-passwords")
        service = self.service(FakePostiz([self.integration]), probe)

        with self.assertRaises(AuthorizationRequired) as raised:
            service.onboard("postiz-integration-1", self.expected)

        blocker = raised.exception.as_dict()
        self.assertEqual("human_authorization_required", blocker["status"])
        self.assertEqual("bluesky_owner_action", blocker["code"])
        self.assertEqual("https://bsky.app/settings/app-passwords", blocker["safe_authorization_url"])
        self.assertNotIn("password", json.dumps(self.reporter.messages).lower())

    def test_public_bluesky_publish_requires_explicit_approval(self):
        service = self.service(FakePostiz([self.integration], [{"postId": "p1"}]))
        destination = service.onboard("postiz-integration-1", self.expected)

        with self.assertRaises(AuthorizationRequired):
            service.publish(
                destination.id,
                "Original copy",
                visibility="private",
                idempotency_key="not-private",
            )


if __name__ == "__main__":
    unittest.main()
