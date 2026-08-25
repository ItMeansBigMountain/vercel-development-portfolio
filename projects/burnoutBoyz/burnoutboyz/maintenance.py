from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .auth import require_record_owner, require_vehicle_owner

_RECEIPT_MEDIA_TYPES = frozenset({"image/jpeg", "image/png", "image/webp", "application/pdf"})


def _id() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _iso_date(value: str) -> str:
    return date.fromisoformat(value).isoformat()


class MaintenanceService:
    """Owner-confirmed maintenance evidence, reminders, costs, and privacy operations."""

    def __init__(self, connection: sqlite3.Connection, *, receipt_root: str | Path, actor_user_id: str, max_receipt_bytes: int = 10 * 1024 * 1024, max_notifications_per_run: int = 20):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.receipt_root = Path(receipt_root)
        self.receipt_root.mkdir(parents=True, exist_ok=True)
        self.actor_user_id = actor_user_id
        self.max_receipt_bytes = max(1, max_receipt_bytes)
        self.max_notifications_per_run = max(1, max_notifications_per_run)

    def _own_vehicle(self, vehicle_id: str) -> None:
        require_vehicle_owner(self.connection, self.actor_user_id, vehicle_id)

    def _fingerprint(self, vehicle_id: str, performed_at: str, odometer_value: int | None, item_ids: Iterable[str]) -> str:
        payload = [vehicle_id, performed_at, odometer_value, sorted(set(item_ids))]
        return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()

    def _validate_items(self, item_ids: list[str]) -> list[str]:
        unique = sorted(set(item_ids))
        if not unique:
            raise ValueError("at least one service item is required")
        marks = ",".join("?" for _ in unique)
        found = {r[0] for r in self.connection.execute(f"SELECT id FROM service_items WHERE id IN ({marks})", unique)}
        missing = set(unique) - found
        if missing:
            raise ValueError(f"unknown service items: {', '.join(sorted(missing))}")
        return unique

    def add_record(
        self, vehicle_id: str, *, performed_at: str, item_ids: list[str], odometer_value: int | None = None,
        parts: list[str] | None = None, fluids: list[str] | None = None, shop: str | None = None,
        notes: str | None = None, costs: list[dict[str, Any]] | None = None, receipt: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._own_vehicle(vehicle_id)
        performed_at = _iso_date(performed_at)
        if odometer_value is not None and (not isinstance(odometer_value, int) or odometer_value < 0):
            raise ValueError("odometer must be a non-negative integer")
        item_ids = self._validate_items(item_ids)
        fingerprint = self._fingerprint(vehicle_id, performed_at, odometer_value, item_ids)
        duplicate = self.connection.execute(
            "SELECT id FROM service_records WHERE vehicle_id=? AND duplicate_fingerprint=? AND deleted_at IS NULL",
            (vehicle_id, fingerprint),
        ).fetchone()
        if duplicate:
            return {"record_id": duplicate[0], "duplicate": True}
        record_id, now = _id(), _now()
        try:
            with self.connection:
                self.connection.execute(
                    "INSERT INTO service_records(id,vehicle_id,service_item_id,performed_at,odometer_value,odometer_unit,status,provider_name,shop_name,notes,duplicate_fingerprint,created_at) VALUES (?,?,?,?,?,?,'confirmed',?,?,?,?,?)",
                    (record_id, vehicle_id, item_ids[0], performed_at, odometer_value, "mi" if odometer_value is not None else None, shop, shop, notes, fingerprint, now),
                )
                self.connection.executemany("INSERT INTO service_record_items(service_record_id,service_item_id) VALUES (?,?)", [(record_id, item) for item in item_ids])
                self.connection.execute("INSERT INTO service_record_details(service_record_id,parts_json,fluids_json) VALUES (?,?,?)", (record_id, json.dumps(parts or []), json.dumps(fluids or [])))
                for cost in costs or []:
                    amount = cost.get("amount_minor")
                    kind = cost.get("type", "other")
                    if not isinstance(amount, int) or amount < 0 or kind not in {"parts", "labor", "tax", "fee", "total", "other"}:
                        raise ValueError("invalid cost")
                    self.connection.execute("INSERT INTO service_costs(id,service_record_id,amount_minor,currency,cost_type,created_at) VALUES (?,?,?,?,?,?)", (_id(), record_id, amount, cost.get("currency", "USD").upper(), kind, now))
                if receipt:
                    self._store_receipt(record_id, receipt, now)
        except sqlite3.IntegrityError as exc:
            if "duplicate_fingerprint" in str(exc):
                row = self.connection.execute("SELECT id FROM service_records WHERE vehicle_id=? AND duplicate_fingerprint=?", (vehicle_id, fingerprint)).fetchone()
                return {"record_id": row[0], "duplicate": True}
            raise
        return {"record_id": record_id, "duplicate": False}

    def _store_receipt(self, record_id: str, receipt: dict[str, Any], now: str) -> None:
        content = receipt.get("content")
        if not isinstance(content, bytes) or not content:
            raise ValueError("receipt content must be non-empty bytes")
        if len(content) > self.max_receipt_bytes:
            raise ValueError("receipt exceeds size limit")
        media_type = receipt.get("media_type")
        if media_type not in _RECEIPT_MEDIA_TYPES:
            raise ValueError("unsupported receipt media type")
        digest = hashlib.sha256(content).hexdigest()
        receipt_id = _id()
        path = self.receipt_root / f"{receipt_id}-{digest}"
        path.write_bytes(content)
        self.connection.execute(
            "INSERT INTO receipts(id,service_record_id,storage_key,media_type,original_filename,sha256,created_at) VALUES (?,?,?,?,?,?,?)",
            (receipt_id, record_id, str(path), media_type, Path(str(receipt.get("filename", "receipt"))).name, digest, now),
        )

    def list_records(self, vehicle_id: str) -> list[dict[str, Any]]:
        self._own_vehicle(vehicle_id)
        ids = [r[0] for r in self.connection.execute("SELECT id FROM service_records WHERE vehicle_id=? AND deleted_at IS NULL ORDER BY performed_at,id", (vehicle_id,))]
        return [self.get_record(record_id) for record_id in ids]

    def get_record(self, record_id: str) -> dict[str, Any]:
        require_record_owner(self.connection, self.actor_user_id, record_id)
        row = self.connection.execute("SELECT * FROM service_records WHERE id=? AND deleted_at IS NULL", (record_id,)).fetchone()
        if not row:
            raise ValueError("unknown service record")
        result = dict(row)
        result["item_ids"] = [r[0] for r in self.connection.execute("SELECT service_item_id FROM service_record_items WHERE service_record_id=? ORDER BY service_item_id", (record_id,))]
        detail = self.connection.execute("SELECT parts_json,fluids_json FROM service_record_details WHERE service_record_id=?", (record_id,)).fetchone()
        result["parts"], result["fluids"] = (json.loads(detail[0]), json.loads(detail[1])) if detail else ([], [])
        costs = [dict(r) for r in self.connection.execute("SELECT amount_minor,currency,cost_type FROM service_costs WHERE service_record_id=? ORDER BY created_at,id", (record_id,))]
        result["costs"] = costs
        result["total_minor"] = sum(c["amount_minor"] for c in costs if c["cost_type"] != "total") or sum(c["amount_minor"] for c in costs)
        receipts = []
        for receipt in self.connection.execute("SELECT id,storage_key,media_type,original_filename,sha256,created_at FROM receipts WHERE service_record_id=? AND deleted_at IS NULL ORDER BY created_at,id", (record_id,)):
            item = dict(receipt); item["storage_exists"] = Path(item["storage_key"]).is_file(); receipts.append(item)
        result["receipts"] = receipts
        result["revision_count"] = self.connection.execute("SELECT COUNT(*) FROM service_record_revisions WHERE service_record_id=?", (record_id,)).fetchone()[0]
        return result

    def edit_record(self, record_id: str, *, notes: str | None = None, shop: str | None = None, receipt: dict[str, Any] | None = None) -> None:
        require_record_owner(self.connection, self.actor_user_id, record_id)
        before = self.get_record(record_id)
        now = _now()
        with self.connection:
            self.connection.execute("INSERT INTO service_record_revisions(id,service_record_id,snapshot_json,reason,created_at) VALUES (?,?,?,?,?)", (_id(), record_id, json.dumps(before, default=str, sort_keys=True), "owner edit", now))
            if notes is not None:
                self.connection.execute("UPDATE service_records SET notes=? WHERE id=?", (notes, record_id))
            if shop is not None:
                self.connection.execute("UPDATE service_records SET shop_name=?,provider_name=? WHERE id=?", (shop, shop, record_id))
            if receipt:
                old = list(self.connection.execute("SELECT id,storage_key FROM receipts WHERE service_record_id=? AND deleted_at IS NULL", (record_id,)))
                self.connection.execute("UPDATE receipts SET deleted_at=? WHERE service_record_id=? AND deleted_at IS NULL", (now, record_id))
                self._store_receipt(record_id, receipt, now)
                for row in old:
                    Path(row[1]).unlink(missing_ok=True)

    def import_history(self, vehicle_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
        self._own_vehicle(vehicle_id)
        report: dict[str, Any] = {"created": 0, "duplicates": 0, "errors": 0, "rows": []}
        for index, row in enumerate(rows):
            try:
                result = self.add_record(vehicle_id, **row)
                status = "duplicate" if result["duplicate"] else "created"
                report["duplicates" if result["duplicate"] else "created"] += 1
                report["rows"].append({"index": index, "status": status, "record_id": result["record_id"]})
            except (TypeError, ValueError, sqlite3.IntegrityError) as exc:
                report["errors"] += 1
                report["rows"].append({"index": index, "status": "error", "error": str(exc)})
        return report

    def set_reminder_preferences(self, vehicle_id: str, *, enabled: bool, channels: list[str], lead_days: int, lead_miles: int) -> None:
        self._own_vehicle(vehicle_id)
        allowed = {"email", "push", "sms", "in_app"}
        if not channels or not set(channels) <= allowed or lead_days < 0 or lead_miles < 0:
            raise ValueError("invalid reminder preferences")
        with self.connection:
            self.connection.execute("INSERT INTO reminder_preferences(vehicle_id,enabled,channels_json,lead_days,lead_miles,updated_at) VALUES (?,?,?,?,?,?) ON CONFLICT(vehicle_id) DO UPDATE SET enabled=excluded.enabled,channels_json=excluded.channels_json,lead_days=excluded.lead_days,lead_miles=excluded.lead_miles,updated_at=excluded.updated_at", (vehicle_id, int(enabled), json.dumps(sorted(set(channels))), lead_days, lead_miles, _now()))

    def notifications(self, vehicle_id: str, *, as_of: date, current_mileage: int | None, upcoming: list[dict[str, Any]]) -> list[dict[str, Any]]:
        self._own_vehicle(vehicle_id)
        pref = self.connection.execute("SELECT * FROM reminder_preferences WHERE vehicle_id=?", (vehicle_id,)).fetchone()
        if not pref or not pref["enabled"]:
            return []
        notices, seen = [], set()
        for item in upcoming:
            source_state = item.get("state", "expected")
            due_date = date.fromisoformat(item["due_date"]) if item.get("due_date") else None
            due_mileage = item.get("due_mileage")
            overdue = source_state == "overdue" or (due_date is not None and due_date < as_of) or (due_mileage is not None and current_mileage is not None and due_mileage < current_mileage)
            near = (due_date is not None and (due_date - as_of).days <= pref["lead_days"]) or (due_mileage is not None and current_mileage is not None and due_mileage - current_mileage <= pref["lead_miles"])
            if overdue or near:
                key = (item.get("occurrence_id"), item["item_id"], "overdue" if overdue else "upcoming")
                if key not in seen and len(notices) < self.max_notifications_per_run:
                    seen.add(key)
                    notices.append({"occurrence_id": item.get("occurrence_id"), "item_id": item["item_id"], "classification": key[2], "source_state": source_state, "channels": json.loads(pref["channels_json"])})
        return sorted(notices, key=lambda n: (n["classification"] != "overdue", n["item_id"]))

    def annual_cost_summary(self, vehicle_id: str, year: int) -> dict[str, Any]:
        self._own_vehicle(vehicle_id)
        rows = self.connection.execute("SELECT c.currency,c.cost_type,SUM(c.amount_minor) amount FROM service_costs c JOIN service_records r ON r.id=c.service_record_id WHERE r.vehicle_id=? AND r.deleted_at IS NULL AND substr(r.performed_at,1,4)=? GROUP BY c.currency,c.cost_type", (vehicle_id, f"{year:04d}")).fetchall()
        by_type = {f"{r['currency']}:{r['cost_type']}": r["amount"] for r in rows}
        totals: dict[str, int] = {}
        for row in rows:
            if row["cost_type"] != "total": totals[row["currency"]] = totals.get(row["currency"], 0) + row["amount"]
        return {"vehicle_id": vehicle_id, "year": year, "totals": totals, "by_type": by_type}

    def export_vehicle(self, vehicle_id: str) -> dict[str, Any]:
        self._own_vehicle(vehicle_id)
        vehicle = self.connection.execute("SELECT v.*,c.model_year,c.make,c.model,c.attributes_json FROM vehicles v JOIN vehicle_configurations c ON c.id=v.configuration_id WHERE v.id=?", (vehicle_id,)).fetchone()
        if not vehicle: raise ValueError("unknown vehicle")
        odometer = [dict(r) for r in self.connection.execute("SELECT observed_at,distance_value,distance_unit FROM odometer_observations WHERE vehicle_id=? ORDER BY observed_at", (vehicle_id,))]
        pref = self.connection.execute("SELECT enabled,channels_json,lead_days,lead_miles,updated_at FROM reminder_preferences WHERE vehicle_id=?", (vehicle_id,)).fetchone()
        related = {}
        for name in ("usage_profiles", "expected_occurrences", "reminders", "recalls", "recall_refreshes", "connected_signal_observations"):
            related[name] = [dict(r) for r in self.connection.execute(f"SELECT * FROM {name} WHERE vehicle_id=?", (vehicle_id,))]
        safe_vehicle = dict(vehicle)
        safe_vehicle.pop("vin_ciphertext", None)
        safe_vehicle.pop("vin_fingerprint", None)
        records = self.list_records(vehicle_id)
        for record in records:
            for receipt in record["receipts"]:
                receipt.pop("storage_key", None)
                receipt.pop("storage_exists", None)
        return {"schema_version": 1, "exported_at": _now(), "vehicle": safe_vehicle, "odometer": odometer, "service_records": records, "reminder_preferences": dict(pref) if pref else None, **related}

    def delete_vehicle(self, vehicle_id: str) -> str:
        self._own_vehicle(vehicle_id)
        exported = self.export_vehicle(vehicle_id)
        configuration_id = exported["vehicle"]["configuration_id"]
        event, now = _id(), _now()
        receipt_paths = [r[0] for r in self.connection.execute("SELECT storage_key FROM receipts WHERE service_record_id IN (SELECT id FROM service_records WHERE vehicle_id=?)", (vehicle_id,))]
        with self.connection:
            self.connection.execute("INSERT INTO deletion_events(id,requested_by_user_id,reason,requested_at,status) VALUES (?,?,?,?,'pending')", (event, self.actor_user_id, "owner requested complete vehicle deletion", now))
            self.connection.execute("UPDATE service_records SET matched_expected_occurrence_id=NULL WHERE vehicle_id=?", (vehicle_id,))
            for table in ("reminders", "reminder_preferences", "expected_occurrences", "usage_profiles", "odometer_observations", "recalls", "recall_refreshes", "connected_signal_observations", "connected_vehicle_links"):
                self.connection.execute(f"DELETE FROM {table} WHERE vehicle_id=?", (vehicle_id,))
            record_ids = [r[0] for r in self.connection.execute("SELECT id FROM service_records WHERE vehicle_id=?", (vehicle_id,))]
            for record_id in record_ids:
                for table in ("receipts", "service_costs", "service_record_revisions", "service_record_details", "service_record_items"):
                    self.connection.execute(f"DELETE FROM {table} WHERE service_record_id=?", (record_id,))
            self.connection.execute("DELETE FROM service_records WHERE vehicle_id=?", (vehicle_id,))
            self.connection.execute("DELETE FROM vehicles WHERE id=?", (vehicle_id,))
            self.connection.execute("DELETE FROM vehicle_configurations WHERE id=? AND NOT EXISTS (SELECT 1 FROM vehicles WHERE configuration_id=?)", (configuration_id, configuration_id))
            self.connection.execute("INSERT INTO deletion_lineage(id,deletion_event_id,entity_type,entity_id,action,processed_at,details_json) VALUES (?,?,?,?, 'deleted',?,?)", (_id(), event, "vehicle", vehicle_id, now, json.dumps({"service_record_count": len(exported["service_records"])})))
            self.connection.execute("UPDATE deletion_events SET status='completed',completed_at=? WHERE id=?", (now, event))
        for path in receipt_paths: Path(path).unlink(missing_ok=True)
        return event
