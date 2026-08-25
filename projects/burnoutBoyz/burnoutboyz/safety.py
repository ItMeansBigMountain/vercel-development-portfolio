from __future__ import annotations

import json
import sqlite3
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from typing import Any, Callable

from .auth import require_connection_owner, require_vehicle_owner

_NHTSA_RECALL_URL = "https://api.nhtsa.gov/recalls/recallsByVehicle?{query}"
_ALLOWED_SIGNALS = frozenset({"odometer", "oil_life", "dtc"})
_RECALL_CAVEAT = "Year/make/model results identify campaigns for a model population; this lookup does not prove this VIN is affected or that a repair is outstanding. Confirm VIN-specific open-recall status with NHTSA or the manufacturer."
_SIGNAL_CAVEAT = "Connected data is owner-authorized and availability varies. DTC data is a reported code, not a diagnosis; oil-life data is not proof that service was performed."


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _id() -> str:
    return str(uuid.uuid4())


class NhtsaRecallClient:
    def __init__(self, transport: Callable[[str], dict[str, Any]] | None = None, timeout: float = 10):
        self.transport = transport or self._request
        self.timeout = timeout

    def _request(self, url: str) -> dict[str, Any]:
        request = urllib.request.Request(url, headers={"User-Agent": "BurnoutBoyz/0.1 (safety recall lookup)"})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    def lookup(self, year: int, make: str, model: str) -> tuple[str, str, list[dict[str, Any]], str | None]:
        query = urllib.parse.urlencode({"modelYear": year, "make": make, "model": model})
        url = _NHTSA_RECALL_URL.format(query=query)
        try:
            payload = self.transport(url)
        except (OSError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            return "source_error", url, [], str(exc)
        rows = payload.get("results") or payload.get("Results") or []
        return ("resolved" if rows else "not_found"), url, rows, None


class RecallService:
    def __init__(self, connection: sqlite3.Connection, *, actor_user_id: str, client: NhtsaRecallClient | None = None):
        self.connection = connection
        self.actor_user_id = actor_user_id
        self.client = client or NhtsaRecallClient()

    def refresh(self, vehicle_id: str) -> dict[str, Any]:
        require_vehicle_owner(self.connection, self.actor_user_id, vehicle_id)
        vehicle = self.connection.execute(
            "SELECT c.model_year, c.make, c.model FROM vehicles v JOIN vehicle_configurations c ON c.id=v.configuration_id WHERE v.id=? AND v.deleted_at IS NULL",
            (vehicle_id,),
        ).fetchone()
        if not vehicle or not all(vehicle):
            raise ValueError("vehicle needs year, make and model for recall lookup")
        state, source_uri, rows, error = self.client.lookup(int(vehicle[0]), vehicle[1], vehicle[2])
        checked_at = _now()
        with self.connection:
            self.connection.execute(
                "INSERT INTO recall_refreshes(id, vehicle_id, lookup_basis, state, source_uri, checked_at, caveat, error) VALUES (?, ?, 'year_make_model', ?, ?, ?, ?, ?)",
                (_id(), vehicle_id, state, source_uri, checked_at, _RECALL_CAVEAT, error),
            )
            if state != "source_error":
                source_id = _id()
                self.connection.execute(
                    "INSERT INTO provenance_sources(id, source_type, provider_name, source_uri, retrieved_at, license_classification) VALUES (?, 'government_api', 'NHTSA Recalls API', ?, ?, 'US government public data')",
                    (source_id, "https://api.nhtsa.gov/recalls/recallsByVehicle", checked_at),
                )
                for row in rows:
                    campaign = str(row.get("NHTSACampaignNumber") or "").strip()
                    if not campaign:
                        continue
                    received = _source_date(row.get("ReportReceivedDate"))
                    self.connection.execute(
                        "INSERT INTO recalls(id, vehicle_id, campaign_number, component, summary, remedy, report_received_date, status, source_id, checked_at) VALUES (?, ?, ?, ?, ?, ?, ?, 'unknown', ?, ?) ON CONFLICT(vehicle_id, campaign_number) DO UPDATE SET component=excluded.component, summary=excluded.summary, remedy=excluded.remedy, report_received_date=excluded.report_received_date, source_id=excluded.source_id, checked_at=excluded.checked_at",
                        (_id(), vehicle_id, campaign, row.get("Component"), row.get("Summary"), row.get("Remedy"), received, source_id, checked_at),
                    )
        return {"state": state, "lookup_basis": "year_make_model", "checked_at": checked_at, "source": source_uri, "count": len(rows), "caveat": _RECALL_CAVEAT, "error": error}


class ConnectedVehicleService:
    def __init__(self, connection: sqlite3.Connection, *, actor_user_id: str, adapters: dict[str, Any] | None = None, minimum_refresh_seconds: int = 300):
        self.connection = connection
        self.actor_user_id = actor_user_id
        self.adapters = adapters or {}
        self.minimum_refresh_seconds = max(1, minimum_refresh_seconds)

    def connect(self, user_id: str, provider: str, external_subject: str, scopes: list[str], *, consent: bool, token_ciphertext: bytes | None = None) -> str:
        if user_id != self.actor_user_id:
            raise PermissionError("resource not found")
        requested = set(scopes)
        if not consent:
            raise ValueError("explicit consent is required")
        if not requested or not requested <= _ALLOWED_SIGNALS:
            raise ValueError("permissions must be limited to odometer, oil_life and dtc")
        now, connection_id = _now(), _id()
        with self.connection:
            self.connection.execute(
                "INSERT INTO connected_accounts(id, user_id, provider, external_subject, token_ciphertext, scopes_json, status, connected_at, consented_at, consent_version) VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?, 'connected-data-v1')",
                (connection_id, user_id, provider, external_subject, token_ciphertext, json.dumps(sorted(requested)), now, now),
            )
        return connection_id

    def revoke(self, connection_id: str) -> None:
        require_connection_owner(self.connection, self.actor_user_id, connection_id)
        now = _now()
        with self.connection:
            cursor = self.connection.execute("UPDATE connected_accounts SET status='revoked', token_ciphertext=NULL, revoked_at=? WHERE id=? AND status='active'", (now, connection_id))
            if not cursor.rowcount:
                raise ValueError("unknown or inactive connection")

    def refresh(self, connection_id: str, vehicle_id: str) -> dict[str, Any]:
        require_connection_owner(self.connection, self.actor_user_id, connection_id)
        require_vehicle_owner(self.connection, self.actor_user_id, vehicle_id)
        account = self.connection.execute("SELECT provider, external_subject, scopes_json, status, last_refreshed_at FROM connected_accounts WHERE id=?", (connection_id,)).fetchone()
        if not account or account[3] != "active":
            raise ValueError("active owner-authorized connection required")
        if account[4]:
            elapsed = datetime.now(timezone.utc) - datetime.fromisoformat(account[4])
            if elapsed.total_seconds() < self.minimum_refresh_seconds:
                raise RuntimeError("connected data rate limit; try again later")
        adapter = self.adapters.get(account[0])
        if not adapter:
            raise ValueError("provider adapter is not configured")
        vehicle = self.connection.execute("SELECT c.model_year, c.make, c.model, v.vin_last4 FROM vehicles v JOIN vehicle_configurations c ON c.id=v.configuration_id WHERE v.id=?", (vehicle_id,)).fetchone()
        if not vehicle:
            raise ValueError("unknown vehicle")
        vehicle_info = {"year": vehicle[0], "make": vehicle[1], "model": vehicle[2], "vin_last4": vehicle[3]}
        compatibility = adapter.compatibility(vehicle_info)
        if compatibility.get("status") != "compatible":
            return {"compatibility": compatibility, "signals": {}, "caveat": _SIGNAL_CAVEAT}
        scopes = set(json.loads(account[2]))
        payload = adapter.fetch(account[1], sorted(scopes))
        signals = {key: value for key, value in payload.items() if key in scopes and key in _ALLOWED_SIGNALS}
        now = _now()
        with self.connection:
            self.connection.execute("INSERT INTO connected_vehicle_links(connection_id, vehicle_id, compatibility_status, compatibility_label, linked_at) VALUES (?, ?, ?, ?, ?) ON CONFLICT(connection_id, vehicle_id) DO UPDATE SET compatibility_status=excluded.compatibility_status, compatibility_label=excluded.compatibility_label", (connection_id, vehicle_id, compatibility["status"], compatibility["label"], now))
            source_id, confidence_id = _id(), _id()
            self.connection.execute("INSERT INTO provenance_sources(id, source_type, provider_name, source_uri, retrieved_at, license_classification) VALUES (?, 'connected_vehicle', ?, 'owner-authorized-provider-api', ?, 'provider terms apply')", (source_id, account[0], now))
            self.connection.execute("INSERT INTO confidence_assessments(id, level, score, rationale, source_id, created_at) VALUES (?, 'medium', 0.7, ?, ?, ?)", (confidence_id, _SIGNAL_CAVEAT, source_id, now))
            if "odometer" in signals:
                reading = signals["odometer"]
                self._insert_odometer(vehicle_id, reading["value"], reading.get("unit", "mi"), source_id, confidence_id, now)
            for signal_type in ("oil_life", "dtc"):
                if signal_type in signals:
                    self.connection.execute("INSERT INTO connected_signal_observations(id, connection_id, vehicle_id, signal_type, value_json, observed_at, caveat) VALUES (?, ?, ?, ?, ?, ?, ?)", (_id(), connection_id, vehicle_id, signal_type, json.dumps(signals[signal_type], sort_keys=True), now, _SIGNAL_CAVEAT))
            self.connection.execute("UPDATE connected_accounts SET last_refreshed_at=? WHERE id=?", (now, connection_id))
        return {"compatibility": compatibility, "signals": signals, "observed_at": now, "caveat": _SIGNAL_CAVEAT}

    def record_manual_mileage(self, vehicle_id: str, value: int, unit: str = "mi") -> str:
        require_vehicle_owner(self.connection, self.actor_user_id, vehicle_id)
        now, source_id, confidence_id = _now(), _id(), _id()
        with self.connection:
            self.connection.execute("INSERT INTO provenance_sources(id, source_type, provider_name, source_uri, retrieved_at, license_classification) VALUES (?, 'manual', 'vehicle owner', 'manual-entry', ?, 'user supplied')", (source_id, now))
            self.connection.execute("INSERT INTO confidence_assessments(id, level, score, rationale, source_id, created_at) VALUES (?, 'medium', 0.6, 'owner-entered odometer reading', ?, ?)", (confidence_id, source_id, now))
            return self._insert_odometer(vehicle_id, value, unit, source_id, confidence_id, now)

    def _insert_odometer(self, vehicle_id: str, value: int, unit: str, source_id: str, confidence_id: str, now: str) -> str:
        if not isinstance(value, int) or value < 0 or unit not in {"mi", "km"}:
            raise ValueError("odometer must be a non-negative integer in mi or km")
        observation_id = _id()
        self.connection.execute("INSERT INTO odometer_observations(id, vehicle_id, observed_at, distance_value, distance_unit, source_id, confidence_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (observation_id, vehicle_id, now, value, unit, source_id, confidence_id, now))
        return observation_id


def _source_date(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass
    return None
