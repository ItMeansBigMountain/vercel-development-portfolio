from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .bluesky import sanitize
from .ledger import Ledger

X_RANGE_BYTES = 1024 * 1024
LINKEDIN_RANGE_BYTES = 2 * 1024 * 1024
LINKEDIN_SUNSET_VERSION = 202508


class ReleaseGateError(RuntimeError):
    pass


@dataclass(frozen=True)
class CompatibilityResult:
    ready: bool
    evidence: tuple[str, ...]
    blockers: tuple[str, ...] = ()


def sanitize_discovery_url(url: str) -> str:
    """Keep discovery routing intact while removing every query value."""
    parts = urlsplit(url)
    safe_query = urlencode([(key, "[REDACTED]") for key, _ in parse_qsl(parts.query, keep_blank_values=True)])
    return urlunsplit((parts.scheme, parts.netloc, parts.path, safe_query, ""))


def verify_stateless_mcp(exchange: Iterable[dict[str, Any]]) -> CompatibilityResult:
    rows = list(exchange)
    blockers: list[str] = []
    if len(rows) < 2:
        blockers.append("two initialize requests are required")
    for index, row in enumerate(rows, 1):
        if row.get("status") != 200:
            blockers.append(f"initialize request {index} did not return 200")
        if row.get("session_id"):
            blockers.append(f"initialize request {index} returned stateful session metadata")
    request_ids = [row.get("request_id") for row in rows]
    if any(item is None for item in request_ids) or len(set(request_ids)) != len(request_ids):
        blockers.append("initialize requests must carry distinct request IDs")
    return CompatibilityResult(not blockers, ("independent Streamable HTTP initialize responses",), tuple(blockers))


def verify_key_url_discovery(probes: dict[str, int], connector_url: str) -> CompatibilityResult:
    blockers: list[str] = []
    required_404 = (
        "/.well-known/oauth-protected-resource/mcp/anything",
        "/.well-known/oauth-protected-resource",
    )
    for path in required_404:
        if probes.get(path) != 404:
            blockers.append(f"{path} must return 404 for key-in-URL MCP")
    safe_url = sanitize_discovery_url(connector_url)
    if any(value and value in safe_url for _, value in parse_qsl(urlsplit(connector_url).query)):
        blockers.append("connector key leaked into discovery evidence")
    return CompatibilityResult(not blockers, (f"sanitized connector: {safe_url}",), tuple(blockers))


def expected_ranges(size: int, chunk_size: int) -> tuple[str, ...]:
    if size <= 0 or chunk_size <= 0:
        raise ValueError("size and chunk_size must be positive")
    return tuple(
        f"bytes={start}-{min(start + chunk_size, size) - 1}"
        for start in range(0, size, chunk_size)
    )


def verify_ranged_upload(size: int, observed_ranges: Iterable[str], chunk_size: int) -> CompatibilityResult:
    expected = expected_ranges(size, chunk_size)
    observed = tuple(observed_ranges)
    blockers = () if observed == expected else (f"ranges differ: expected {expected}, observed {observed}",)
    return CompatibilityResult(not blockers, (f"{len(expected)} ranged chunks at {chunk_size} bytes",), blockers)


def select_pinterest_mp4(media: Iterable[dict[str, str]]) -> dict[str, str]:
    for item in media:
        path = item.get("path", "")
        if urlsplit(path).path.lower().endswith(".mp4"):
            return item
    raise ReleaseGateError("Pinterest video fixture has no MP4 media")


def inspect_linkedin_versions(source_root: str | Path) -> CompatibilityResult:
    versions: set[int] = set()
    for path in Path(source_root).rglob("linkedin*.provider.ts"):
        text = path.read_text(encoding="utf-8")
        versions.update(int(item) for item in re.findall(r"['\"]Linked[Ii]n-Version['\"]\s*:\s*['\"](\d{6})", text))
    blockers: list[str] = []
    if not versions:
        blockers.append("no effective Linkedin-Version header found")
    unsupported = sorted(item for item in versions if item <= LINKEDIN_SUNSET_VERSION)
    if unsupported:
        blockers.append("sunset LinkedIn versions found: " + ", ".join(map(str, unsupported)))
    return CompatibilityResult(not blockers, tuple(f"Linkedin-Version {item}" for item in sorted(versions)), tuple(blockers))


class PostizPendingCoordinator:
    """Preserves Hermes idempotency while reconciling Postiz pending/final states."""

    def __init__(self, ledger: Ledger, postiz: Any):
        self.ledger = ledger
        self.postiz = postiz

    def publish(self, *, attempt_id: str, idempotency_key: str, destination_id: str, visibility: str, payload: dict[str, Any]):
        prior = self.ledger.get_by_idempotency_key(idempotency_key)
        if prior:
            if prior["attempt_id"] != attempt_id:
                raise ReleaseGateError("idempotency key is already correlated with another Hermes attempt")
            return self.reconcile(attempt_id)

        self.ledger.begin_attempt(attempt_id, idempotency_key, destination_id, visibility)
        response = sanitize(self.postiz.create_post(payload))
        postiz_id = response.get("id") or response.get("postId")
        if not postiz_id:
            self.ledger.finish_attempt(attempt_id, status="outcome_unknown", response=response)
            raise ReleaseGateError("Postiz accepted no correlatable post ID; automatic retry is prohibited")
        state = response.get("state") or response.get("status") or "pending"
        self._record(attempt_id, postiz_id, state, response)
        return self.reconcile(attempt_id)

    def reconcile(self, attempt_id: str):
        attempt = self.ledger.get_attempt(attempt_id)
        if attempt is None:
            raise ReleaseGateError("unknown Hermes attempt")
        if attempt["status"] == "published_verified":
            return attempt
        postiz_id = attempt["postiz_post_id"]
        if not postiz_id:
            self.ledger.finish_attempt(attempt_id, status="outcome_unknown", error="manual reconciliation required")
            return self.ledger.get_attempt(attempt_id)
        state = sanitize(self.postiz.get_post(postiz_id))
        self._record(attempt_id, postiz_id, state.get("state") or state.get("status") or "pending", state)
        return self.ledger.get_attempt(attempt_id)

    def _record(self, attempt_id: str, postiz_id: str, state: str, response: dict[str, Any]):
        normalized = state.lower()
        platform_id = response.get("platformPostId") or response.get("releaseId")
        url = response.get("url") or response.get("releaseURL")
        verified = normalized in {"completed", "published", "success"} and bool(platform_id and url)
        status = "published_verified" if verified else "postiz_pending"
        self.ledger.finish_attempt(
            attempt_id,
            status=status,
            response=response,
            postiz_post_id=postiz_id,
            platform_post_id=platform_id,
            url=url,
        )
