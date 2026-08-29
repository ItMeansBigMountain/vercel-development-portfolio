from __future__ import annotations

import json
import os
import stat
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from .bluesky import AuthorizationRequired, sanitize


class PostizAPIError(RuntimeError):
    pass


class PostizHTTPClient:
    """Minimal official Public API adapter; the API key never enters payloads or errors."""

    def __init__(self, base_url: str, api_key: str, *, opener=urllib.request.urlopen):
        if not base_url.startswith("https://"):
            raise ValueError("Postiz base URL must use public HTTPS")
        if not api_key:
            raise AuthorizationRequired("postiz_api_key", "Install a narrow Postiz API key in the protected store")
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._opener = opener

    @classmethod
    def from_secret_file(cls, base_url: str, path: str | Path):
        secret_path = Path(path)
        try:
            mode = stat.S_IMODE(secret_path.stat().st_mode)
        except FileNotFoundError:
            raise AuthorizationRequired("postiz_api_key", "Install the Postiz API key secret file") from None
        if mode & 0o077:
            raise PermissionError("Postiz API key file must not be group/world accessible")
        return cls(base_url, secret_path.read_text(encoding="utf-8").strip())

    def list_integrations(self):
        return self._request("GET", "/public/v1/integrations")

    def create_post(self, payload):
        return self._request("POST", "/public/v1/posts", payload)

    def _request(self, method: str, path: str, payload: Any = None):
        body = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(
            self.base_url + path,
            data=body,
            method=method,
            headers={"Authorization": self._api_key, "Content-Type": "application/json"},
        )
        try:
            with self._opener(request, timeout=30) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as error:
            safe_body = sanitize(error.read().decode("utf-8", "replace"))
            raise PostizAPIError(f"Postiz HTTP {error.code}: {safe_body}") from None
        except urllib.error.URLError as error:
            raise PostizAPIError(f"Postiz request failed: {sanitize(str(error.reason))}") from None
        except TimeoutError as error:
            raise PostizAPIError(f"Postiz request failed: {sanitize(str(error))}") from None


class BlueskyPublicIdentityProbe:
    """Correlates Postiz's authenticated handle with Bluesky DID/profile identity."""

    def __init__(self, service_url: str = "https://public.api.bsky.app", *, opener=urllib.request.urlopen):
        self.service_url = service_url.rstrip("/")
        self._opener = opener

    def verify(self, integration):
        handle = integration.get("profile")
        if not handle:
            raise AuthorizationRequired("bluesky_connection", "Reconnect Bluesky so Postiz returns its profile handle")
        params = urllib.parse.urlencode({"actor": handle})
        url = f"{self.service_url}/xrpc/app.bsky.actor.getProfile?{params}"
        try:
            with self._opener(url, timeout=20) as response:
                profile = json.loads(response.read())
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as error:
            raise AuthorizationRequired("bluesky_identity_probe", "Complete Bluesky identity verification in Postiz") from None
        return {
            "did": profile.get("did"),
            "handle": profile.get("handle"),
            "display_name": profile.get("displayName") or integration.get("name"),
            "service_url": "https://bsky.social",
        }


class DiscordWebhookReporter:
    def __init__(self, webhook_url: str, *, opener=urllib.request.urlopen):
        if not webhook_url.startswith("https://"):
            raise ValueError("Discord webhook must use HTTPS")
        self._webhook_url = webhook_url
        self._opener = opener

    def send(self, report):
        safe = sanitize(report)
        content = json.dumps(safe, sort_keys=True, separators=(",", ":"))
        request = urllib.request.Request(
            self._webhook_url,
            data=json.dumps({"content": content[:1900]}).encode(),
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with self._opener(request, timeout=20):
            return None
