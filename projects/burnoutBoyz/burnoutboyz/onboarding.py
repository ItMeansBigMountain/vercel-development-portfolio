from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import sqlite3
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any, Callable

from .auth import require_garage_owner

_VIN_RE = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")
_TRANSLITERATION = {**{str(i): i for i in range(10)}, **dict(zip("ABCDEFGH", (1, 2, 3, 4, 5, 6, 7, 8))), **dict(zip("JKLMNPR", (1, 2, 3, 4, 5, 7, 9))), **dict(zip("STUVWXYZ", (2, 3, 4, 5, 6, 7, 8, 9)))}
_WEIGHTS = (8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2)
_VPIC_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _id() -> str:
    return str(uuid.uuid4())


def normalize_vin(value: str) -> str:
    return re.sub(r"[\s-]", "", value).upper()


def validate_vin(value: str) -> str:
    vin = normalize_vin(value)
    if not _VIN_RE.fullmatch(vin):
        raise ValueError("VIN must contain 17 valid characters; I, O and Q are not allowed")
    total = sum(_TRANSLITERATION[ch] * weight for ch, weight in zip(vin, _WEIGHTS))
    expected = "X" if total % 11 == 10 else str(total % 11)
    if vin[8] != expected:
        raise ValueError("VIN check digit is invalid")
    return vin


class VinProtector:
    """Authenticated, randomized VIN envelope using separate HMAC-derived keys."""

    def __init__(self, secret: bytes):
        if len(secret) < 32:
            raise ValueError("VIN secret must be at least 32 bytes")
        self._enc = hmac.new(secret, b"burnoutboyz/vin/encryption", hashlib.sha256).digest()
        self._mac = hmac.new(secret, b"burnoutboyz/vin/authentication", hashlib.sha256).digest()
        self._lookup = hmac.new(secret, b"burnoutboyz/vin/lookup", hashlib.sha256).digest()

    def protect(self, vin: str) -> tuple[bytes, str, str]:
        vin = validate_vin(vin)
        nonce = os.urandom(16)
        plaintext = vin.encode("ascii")
        stream = hmac.new(self._enc, nonce + b"\x00", hashlib.sha256).digest()
        ciphertext = bytes(a ^ b for a, b in zip(plaintext, stream))
        body = b"BBV1" + nonce + ciphertext
        tag = hmac.new(self._mac, body, hashlib.sha256).digest()
        fingerprint = hmac.new(self._lookup, plaintext, hashlib.sha256).hexdigest()
        return body + tag, fingerprint, vin[-4:]

    def reveal(self, envelope: bytes) -> str:
        if len(envelope) != 69 or not envelope.startswith(b"BBV1"):
            raise ValueError("invalid VIN envelope")
        body, tag = envelope[:-32], envelope[-32:]
        if not hmac.compare_digest(hmac.new(self._mac, body, hashlib.sha256).digest(), tag):
            raise ValueError("VIN envelope authentication failed")
        nonce, ciphertext = body[4:20], body[20:]
        stream = hmac.new(self._enc, nonce + b"\x00", hashlib.sha256).digest()
        return bytes(a ^ b for a, b in zip(ciphertext, stream)).decode("ascii")


@dataclass(frozen=True)
class DecodeResult:
    state: str
    source: str
    retrieved_at: str
    candidates: tuple[dict[str, Any], ...]
    errors: tuple[str, ...] = ()


class VpicClient:
    def __init__(self, transport: Callable[[str], dict[str, Any]] | None = None, timeout: float = 10):
        self.timeout = timeout
        self.transport = transport or self._request

    def _request(self, url: str) -> dict[str, Any]:
        request = urllib.request.Request(url, headers={"User-Agent": "BurnoutBoyz/0.1 (vehicle onboarding)"})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    def decode(self, vin: str) -> DecodeResult:
        vin = validate_vin(vin)
        now = _now()
        url = _VPIC_URL.format(vin=urllib.parse.quote(vin))
        try:
            payload = self.transport(url)
        except (OSError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            return DecodeResult("source_error", url, now, (), (f"vPIC unavailable: {exc}",))
        rows = payload.get("Results") or []
        if not rows:
            return DecodeResult("not_found", url, now, (), ("vPIC returned no result",))
        row = rows[0]
        errors = tuple(part.strip() for part in str(row.get("ErrorText") or "").split(";") if part.strip() and not part.lstrip().startswith("0 -"))
        base = {"year": _integer(row.get("ModelYear")), "make": _clean(row.get("Make")), "model": _clean(row.get("Model")), "trim": _clean(row.get("Trim"))}
        engines = _values(row, (("DisplacementL", "EngineCylinders", "FuelTypePrimary", "EngineModel"),))
        transmissions = _values(row, (("TransmissionStyle", "TransmissionSpeeds"),))
        drivetrains = tuple(filter(None, (_clean(row.get("DriveType")),)))
        candidate = {**base, "engines": engines, "transmissions": transmissions, "drivetrains": drivetrains}
        required = (base["year"], base["make"], base["model"])
        ambiguous = any(len(values) != 1 for values in (engines, transmissions, drivetrains))
        state = "not_found" if not any(required) else "partial" if not all(required) or ambiguous else "resolved"
        return DecodeResult(state, url, now, (candidate,), errors)


def _clean(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


def _integer(value: Any) -> int | None:
    try:
        return int(value) if str(value or "").strip() else None
    except ValueError:
        return None


def _values(row: dict[str, Any], groups: tuple[tuple[str, ...], ...]) -> tuple[dict[str, Any], ...]:
    values = tuple({key: _clean(row.get(key)) for key in keys if _clean(row.get(key)) is not None} for keys in groups)
    return tuple(value for value in values if value)


class OnboardingService:
    def __init__(self, connection: sqlite3.Connection, vin_protector: VinProtector, *, actor_user_id: str):
        self.connection = connection
        self.vin_protector = vin_protector
        self.actor_user_id = actor_user_id

    def list_garages(self, user_id: str) -> list[dict[str, Any]]:
        if user_id != self.actor_user_id:
            raise PermissionError("resource not found")
        rows = self.connection.execute("SELECT id, name, created_at FROM garages WHERE user_id=? AND deleted_at IS NULL ORDER BY created_at", (user_id,)).fetchall()
        return [dict(row) for row in rows]

    def rename_garage(self, garage_id: str, name: str) -> None:
        require_garage_owner(self.connection, self.actor_user_id, garage_id)
        if not name.strip():
            raise ValueError("garage name is required")
        with self.connection:
            cursor = self.connection.execute("UPDATE garages SET name=? WHERE id=? AND deleted_at IS NULL", (name.strip(), garage_id))
            if not cursor.rowcount:
                raise ValueError("unknown garage")

    def delete_garage(self, garage_id: str) -> None:
        require_garage_owner(self.connection, self.actor_user_id, garage_id)
        with self.connection:
            active = self.connection.execute("SELECT COUNT(*) FROM vehicles WHERE garage_id=? AND deleted_at IS NULL", (garage_id,)).fetchone()[0]
            if active:
                raise ValueError("garage must be empty before deletion")
            cursor = self.connection.execute("UPDATE garages SET deleted_at=? WHERE id=? AND deleted_at IS NULL", (_now(), garage_id))
            if not cursor.rowcount:
                raise ValueError("unknown garage")

    def add_vehicle(self, garage_id: str, *, identity: dict[str, Any], vin: str | None = None, nickname: str | None = None, mileage: int | None = None, in_service_date: str | None = None, usage_answers: dict[str, bool] | None = None, selected_engine: dict[str, Any] | None = None, selected_transmission: dict[str, Any] | None = None, selected_drivetrain: str | None = None, source_uri: str = "manual-entry", source_type: str = "manual") -> str:
        require_garage_owner(self.connection, self.actor_user_id, garage_id)
        year, make, model = identity.get("year"), _clean(identity.get("make")), _clean(identity.get("model"))
        if not isinstance(year, int) or year < 1886 or year > date.today().year + 2 or not make or not model:
            raise ValueError("valid year, make and model are required")
        self._require_explicit_choice(identity.get("engines"), selected_engine, "engine")
        self._require_explicit_choice(identity.get("transmissions"), selected_transmission, "transmission")
        self._require_explicit_choice(identity.get("drivetrains"), selected_drivetrain, "drivetrain")
        selected_engine = self._only_candidate(identity.get("engines"), selected_engine)
        selected_transmission = self._only_candidate(identity.get("transmissions"), selected_transmission)
        selected_drivetrain = self._only_candidate(identity.get("drivetrains"), selected_drivetrain)
        if mileage is not None and (not isinstance(mileage, int) or mileage < 0):
            raise ValueError("mileage must be a non-negative integer")
        if in_service_date:
            date.fromisoformat(in_service_date)
        answers = usage_answers or {}
        severity = classify_usage(answers)
        now, source_id, confidence_id, configuration_id, vehicle_id = _now(), _id(), _id(), _id(), _id()
        if source_type == "government_api":
            # Decode request URLs contain the VIN; persist only the endpoint identity.
            source_uri = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues"
        cipher = fingerprint = last4 = None
        if vin:
            cipher, fingerprint, last4 = self.vin_protector.protect(vin)
        complete = all((selected_engine, selected_transmission, selected_drivetrain))
        attributes = {"trim": identity.get("trim"), "engine": selected_engine, "transmission": selected_transmission}
        with self.connection:
            self.connection.execute("INSERT INTO provenance_sources(id, source_type, provider_name, source_uri, retrieved_at, license_classification) VALUES (?, ?, ?, ?, ?, ?)", (source_id, source_type, "NHTSA vPIC" if source_type == "government_api" else "vehicle owner", source_uri, now, "US government public data" if source_type == "government_api" else "user supplied"))
            self.connection.execute("INSERT INTO confidence_assessments(id, level, score, rationale, source_id, created_at) VALUES (?, ?, ?, ?, ?, ?)", (confidence_id, "high" if source_type == "government_api" else "medium", 0.85 if source_type == "government_api" else 0.6, "configuration explicitly selected; source does not prove installed equipment" if source_type == "government_api" else "owner-entered configuration", source_id, now))
            self.connection.execute("INSERT INTO vehicle_configurations(id, model_year, make, model, drivetrain, identity_state, source_id, confidence_id, attributes_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (configuration_id, year, make, model, selected_drivetrain, "confirmed" if complete else "partial", source_id, confidence_id, json.dumps(attributes, sort_keys=True)))
            self.connection.execute("INSERT INTO vehicles(id, garage_id, configuration_id, nickname, vin_ciphertext, vin_fingerprint, vin_last4, in_service_date, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (vehicle_id, garage_id, configuration_id, nickname, cipher, fingerprint, last4, in_service_date, now))
            if mileage is not None:
                self.connection.execute("INSERT INTO odometer_observations(id, vehicle_id, observed_at, distance_value, distance_unit, source_id, confidence_id, created_at) VALUES (?, ?, ?, ?, 'mi', ?, ?, ?)", (_id(), vehicle_id, now, mileage, source_id, confidence_id, now))
            self.connection.execute("INSERT INTO usage_profiles(id, vehicle_id, severity, effective_from, answers_json, source_id, confidence_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (_id(), vehicle_id, severity, now, json.dumps(answers, sort_keys=True), source_id, confidence_id, now))
        return vehicle_id

    @staticmethod
    def _require_explicit_choice(options: Any, selected: Any, label: str) -> None:
        options = tuple(options or ())
        if len(options) > 1 and selected is None:
            raise ValueError(f"multiple {label} options require an explicit selection")
        if selected is not None and options and selected not in options:
            raise ValueError(f"selected {label} is not a decoded candidate")

    @staticmethod
    def _only_candidate(options: Any, selected: Any) -> Any:
        options = tuple(options or ())
        return options[0] if selected is None and len(options) == 1 else selected


def classify_usage(answers: dict[str, bool]) -> str:
    if not answers:
        return "unknown"
    severe_keys = {"frequent_short_trips", "extreme_temperatures", "towing_or_heavy_loads", "dusty_or_offroad", "extended_idling_or_stop_go"}
    known = severe_keys.intersection(answers)
    if not known:
        return "unknown"
    return "severe" if any(answers[key] for key in known) else "normal"
