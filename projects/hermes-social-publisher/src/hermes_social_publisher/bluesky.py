from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from typing import Any

from .ledger import Destination, Ledger


SECRET_FIELDS = {"authorization", "token", "access_token", "refresh_token", "api_key", "password", "secret"}
SECRET_PATTERN = re.compile(r"(?i)(authorization\s*:\s*|pos_)[^\s,;]+")


def sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if key.lower() in SECRET_FIELDS else sanitize(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, str):
        return SECRET_PATTERN.sub("[REDACTED]", value)
    return value


class DestinationMismatch(RuntimeError):
    pass


class AuthorizationRequired(RuntimeError):
    def __init__(self, code: str, action: str, safe_authorization_url: str | None = None):
        super().__init__(action)
        self.code = code
        self.action = action
        self.safe_authorization_url = safe_authorization_url

    def as_dict(self):
        return {
            "status": "human_authorization_required",
            "code": self.code,
            "action": self.action,
            "safe_authorization_url": self.safe_authorization_url,
        }


@dataclass(frozen=True)
class PublicationResult:
    attempt_id: str
    status: str
    postiz_post_id: str | None
    platform_post_id: str | None
    url: str | None


class PublisherService:
    def __init__(self, *, postiz, identity_probe, ledger: Ledger, reporter):
        self.postiz = postiz
        self.identity_probe = identity_probe
        self.ledger = ledger
        self.reporter = reporter

    def onboard(self, integration_id: str, expected: dict[str, str]) -> Destination:
        integration = next(
            (item for item in self.postiz.list_integrations() if item.get("id") == integration_id),
            None,
        )
        if integration is None:
            raise DestinationMismatch("Postiz integration ID was not found")
        if integration.get("identifier") != "bluesky" or integration.get("disabled"):
            raise DestinationMismatch("Integration is not an enabled Bluesky destination")

        identity = self.identity_probe.verify(integration)
        required = ("did", "handle", "display_name", "service_url")
        if any(not identity.get(field) for field in required):
            raise DestinationMismatch("Identity probe did not return complete destination proof")
        mismatches = [field for field in required if identity.get(field) != expected.get(field)]
        if integration.get("profile") != identity["handle"]:
            mismatches.append("postiz_profile")
        if integration.get("name") != identity["display_name"]:
            mismatches.append("postiz_name")
        if mismatches:
            raise DestinationMismatch("Destination identity mismatch: " + ", ".join(sorted(set(mismatches))))

        destination = Destination(
            id=integration_id,
            platform="bluesky",
            immutable_account_id=identity["did"],
            handle=identity["handle"],
            display_name=identity["display_name"],
            service_url=identity["service_url"],
            enabled=True,
        )
        self.ledger.save_destination(destination)
        self.reporter.send(
            {
                "event": "destination_verified",
                "platform": destination.platform,
                "integration_id": destination.id,
                "immutable_account_id": destination.immutable_account_id,
                "handle": destination.handle,
                "display_name": destination.display_name,
            }
        )
        return destination

    def publish(
        self,
        destination_id: str,
        content: str,
        *,
        visibility: str,
        idempotency_key: str,
        allow_public: bool = False,
    ) -> PublicationResult:
        prior = self.ledger.get_by_idempotency_key(idempotency_key)
        if prior:
            return self._result(prior)
        destination = self.ledger.get_destination(destination_id)
        if destination is None or not destination.enabled:
            raise DestinationMismatch("Destination is not verified and enabled")
        if visibility not in {"draft", "now", "private"}:
            raise ValueError("visibility must be draft, now, or private")
        if visibility != "draft" and not allow_public:
            raise AuthorizationRequired(
                "public_bluesky_approval",
                "Bluesky has no native private visibility; explicit public-post approval is required",
            )

        effective_visibility = "draft" if visibility == "draft" else "now"
        attempt_id = str(uuid.uuid4())
        self.ledger.begin_attempt(attempt_id, idempotency_key, destination_id, visibility)
        payload = {
            "type": effective_visibility,
            "date": "",
            "shortLink": False,
            "tags": [],
            "posts": [
                {
                    "integration": {"id": destination.id},
                    "value": [{"content": content, "image": []}],
                    "settings": {"__type": "bluesky"},
                }
            ],
        }
        try:
            response = sanitize(self.postiz.create_post(payload))
        except Exception as error:
            safe_error = sanitize(str(error))
            self.ledger.finish_attempt(attempt_id, status="api_failure", error=safe_error)
            self.reporter.send(
                {"event": "publication_failed", "attempt_id": attempt_id, "error": safe_error}
            )
            raise RuntimeError(safe_error) from None

        first = response[0] if isinstance(response, list) and response else {}
        postiz_post_id = first.get("postId") if isinstance(first, dict) else None
        platform_post_id = first.get("platformPostId") or first.get("releaseId") if isinstance(first, dict) else None
        url = first.get("url") if isinstance(first, dict) else None
        if effective_visibility == "draft" and postiz_post_id:
            status = "accepted_draft"
        elif postiz_post_id and platform_post_id and url:
            status = "published_verified"
        else:
            status = "unverified_response"
        self.ledger.finish_attempt(
            attempt_id,
            status=status,
            response=response,
            postiz_post_id=postiz_post_id,
            platform_post_id=platform_post_id,
            url=url,
        )
        report = {
            "event": "publication_recorded",
            "attempt_id": attempt_id,
            "platform": destination.platform,
            "destination_id": destination.id,
            "requested_visibility": visibility,
            "effective_visibility": effective_visibility,
            "status": status,
            "postiz_post_id": postiz_post_id,
            "platform_post_id": platform_post_id,
            "url": url,
        }
        self.reporter.send(sanitize(report))
        return PublicationResult(attempt_id, status, postiz_post_id, platform_post_id, url)

    @staticmethod
    def _result(row: dict[str, Any]) -> PublicationResult:
        return PublicationResult(
            row["attempt_id"], row["status"], row["postiz_post_id"], row["platform_post_id"], row["url"]
        )
