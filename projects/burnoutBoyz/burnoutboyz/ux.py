from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime, timezone
from typing import Any

from .auth import require_vehicle_owner


_FRIENDLY_SEVERITY = {
    "normal": "Standard schedule",
    "severe": "Severe-use schedule may apply",
    "mixed": "Mixed driving pattern",
    "unknown": "Driving pattern not confirmed",
}

_HELPFUL_EMPTY_STATE = "Nothing needs action from the data we have. Add mileage or service records to sharpen the timeline."
_NON_UPSELLING_TONE = "Helpful, evidence-first, never fear-based or shop-upsell driven."
_RECALL_CAVEAT = "Model-level recall results are not VIN-specific proof. Confirm open status with NHTSA or the manufacturer."


def _today() -> date:
    return datetime.now(timezone.utc).date()


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value[:10])


def _json(value: str | None, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


def _row_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


class OwnersManualUXService:
    """Mobile-first owner's-manual view models over the provenance backend.

    The service returns plain dictionaries so a web, native, or offline-first client can
    render the same evidence-backed dashboard without inferring service completion or
    using fear-based maintenance copy.
    """

    def __init__(self, connection: sqlite3.Connection, *, actor_user_id: str):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.actor_user_id = actor_user_id

    def _own_vehicle(self, vehicle_id: str) -> None:
        require_vehicle_owner(self.connection, self.actor_user_id, vehicle_id)

    def garage_dashboard(self, user_id: str, *, as_of: date | None = None) -> dict[str, Any]:
        if user_id != self.actor_user_id:
            raise PermissionError("resource not found")
        as_of = as_of or _today()
        garages = []
        for garage in self.connection.execute(
            "SELECT id,name FROM garages WHERE user_id=? AND deleted_at IS NULL ORDER BY created_at,id",
            (user_id,),
        ):
            vehicles = [self.vehicle_card(row["id"], as_of=as_of) for row in self._garage_vehicle_rows(garage["id"])]
            totals = {
                "vehicles": len(vehicles),
                "due_now": sum(card["counts"]["due_now"] for card in vehicles),
                "upcoming": sum(card["counts"]["upcoming"] for card in vehicles),
                "unknown": sum(card["counts"]["unknown"] for card in vehicles),
                "open_or_unknown_recalls": sum(card["counts"]["recalls"] for card in vehicles),
            }
            garages.append({"id": garage["id"], "name": garage["name"], "totals": totals, "vehicles": vehicles})
        return {
            "screen": "garage_dashboard",
            "layout": self._layout_contract("garage_dashboard"),
            "tone": _NON_UPSELLING_TONE,
            "as_of": as_of.isoformat(),
            "garages": garages,
            "empty_state": _HELPFUL_EMPTY_STATE if not garages else None,
            "offline_state": self.offline_state(),
        }

    def vehicle_card(self, vehicle_id: str, *, as_of: date | None = None) -> dict[str, Any]:
        manual = self.vehicle_manual(vehicle_id, as_of=as_of)
        identity = manual["vehicle"]
        counts = manual["counts"]
        next_item = manual["upcoming"][0] if manual["upcoming"] else None
        due_item = manual["due_now"][0] if manual["due_now"] else None
        return {
            "id": vehicle_id,
            "title": identity["display_name"],
            "subtitle": identity.get("nickname") or identity.get("trim") or "Owner's manual",
            "mileage": manual["mileage"],
            "severity": manual["severe_use"],
            "counts": counts,
            "primary_action": "Review due now" if counts["due_now"] else "Update mileage",
            "next_due": next_item,
            "most_urgent": due_item,
            "safe_copy": self._status_copy(counts),
        }

    def vehicle_manual(self, vehicle_id: str, *, as_of: date | None = None) -> dict[str, Any]:
        self._own_vehicle(vehicle_id)
        as_of = as_of or _today()
        vehicle = self._vehicle_identity(vehicle_id)
        if not vehicle:
            raise ValueError("unknown vehicle")
        mileage = self.latest_mileage(vehicle_id)
        severity = self.latest_usage(vehicle_id)
        due_now, upcoming, unknown = self._occurrence_sections(vehicle_id, as_of=as_of)
        history = self.service_history(vehicle_id)
        recalls = self.recall_section(vehicle_id)
        connected = self.connected_status(vehicle_id)
        counts = {
            "expected": len(due_now) + len(upcoming) + len(unknown),
            "confirmed": len(history),
            "due_now": len(due_now),
            "upcoming": len(upcoming),
            "unknown": len(unknown),
            "history": len(history),
            "recalls": len([r for r in recalls["campaigns"] if r["status"] in {"open", "unknown"}]),
        }
        return {
            "screen": "vehicle_owners_manual",
            "layout": self._layout_contract("vehicle_owners_manual"),
            "tone": _NON_UPSELLING_TONE,
            "as_of": as_of.isoformat(),
            "vehicle": vehicle,
            "mileage": mileage,
            "severe_use": self.severe_use_explanation(severity),
            "counts": counts,
            "tabs": ["due_now", "upcoming", "history", "recalls", "sources"],
            "due_now": due_now,
            "upcoming": upcoming,
            "unknown": unknown,
            "history": history,
            "recalls": recalls,
            "connected_data": connected,
            "source_confidence_drilldown": self.source_confidence_drilldown(vehicle_id),
            "actions": {
                "add_service": self.add_service_flow(vehicle_id),
                "update_mileage": self.mileage_update_model(vehicle_id),
                "reminders": self.accessible_reminder_copy(vehicle_id),
            },
            "empty_state": _HELPFUL_EMPTY_STATE if counts["expected"] == 0 and counts["history"] == 0 else None,
            "offline_state": self.offline_state(),
            "error_state": self.error_state("source_unavailable"),
        }

    def latest_mileage(self, vehicle_id: str) -> dict[str, Any]:
        row = self.connection.execute(
            "SELECT observed_at,distance_value,distance_unit FROM odometer_observations WHERE vehicle_id=? ORDER BY observed_at DESC,id DESC LIMIT 1",
            (vehicle_id,),
        ).fetchone()
        if not row:
            return {"value": None, "unit": "mi", "observed_at": None, "label": "Mileage not added yet", "confidence": "unknown"}
        return {
            "value": row["distance_value"],
            "unit": row["distance_unit"],
            "observed_at": row["observed_at"],
            "label": f"{row['distance_value']:,} {row['distance_unit']}",
            "confidence": self._confidence_for_odometer(vehicle_id, row["observed_at"]),
        }

    def service_history(self, vehicle_id: str) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT r.id,r.performed_at,r.odometer_value,r.odometer_unit,r.shop_name,r.notes,
                   GROUP_CONCAT(i.name, ', ') item_names, COUNT(i.id) item_count
            FROM service_records r
            LEFT JOIN service_record_items ri ON ri.service_record_id=r.id
            LEFT JOIN service_items i ON i.id=ri.service_item_id
            WHERE r.vehicle_id=? AND r.deleted_at IS NULL
            GROUP BY r.id
            ORDER BY r.performed_at DESC,r.id DESC
            """,
            (vehicle_id,),
        ).fetchall()
        return [
            {
                "record_id": row["id"],
                "performed_at": row["performed_at"],
                "mileage": row["odometer_value"],
                "unit": row["odometer_unit"],
                "summary": row["item_names"] or "Service record",
                "shop": row["shop_name"],
                "notes": row["notes"],
                "evidence_label": "Owner-confirmed record",
            }
            for row in rows
        ]

    def recall_section(self, vehicle_id: str) -> dict[str, Any]:
        campaigns = [
            {
                "campaign_number": row["campaign_number"],
                "component": row["component"],
                "summary": row["summary"],
                "remedy": row["remedy"],
                "report_received_date": row["report_received_date"],
                "status": row["status"],
                "checked_at": row["checked_at"],
                "caveat": _RECALL_CAVEAT,
                "action_label": "Check VIN-specific status",
            }
            for row in self.connection.execute(
                "SELECT campaign_number,component,summary,remedy,report_received_date,status,checked_at FROM recalls WHERE vehicle_id=? ORDER BY report_received_date DESC,campaign_number",
                (vehicle_id,),
            )
        ]
        refresh = _row_dict(
            self.connection.execute(
                "SELECT state,source_uri,checked_at,caveat,error FROM recall_refreshes WHERE vehicle_id=? ORDER BY checked_at DESC,id DESC LIMIT 1",
                (vehicle_id,),
            ).fetchone()
        )
        return {
            "lookup_basis": "year_make_model",
            "refresh": refresh,
            "campaigns": campaigns,
            "empty_state": "No campaigns found in the latest model-level lookup." if refresh and not campaigns else None,
            "caveat": _RECALL_CAVEAT,
        }

    def source_confidence_drilldown(self, vehicle_id: str) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT e.id occurrence_id,e.state,e.ordinal,e.assumptions_json,
                   i.name item_name,i.category,
                   p.name provider_name,p.source_type,p.license_classification,p.terms_uri,
                   v.external_version schedule_version,v.source_url,v.confidence schedule_confidence,
                   r.confidence rule_confidence,r.source_note
            FROM expected_occurrences e
            JOIN interval_rules r ON r.id=e.interval_rule_id
            JOIN service_items i ON i.id=r.service_item_id
            JOIN schedule_versions v ON v.id=r.schedule_version_id
            JOIN schedule_providers p ON p.id=v.provider_id
            WHERE e.vehicle_id=?
            ORDER BY i.name,e.ordinal
            """,
            (vehicle_id,),
        ).fetchall()
        return [
            {
                "occurrence_id": row["occurrence_id"],
                "service": row["item_name"],
                "category": row["category"],
                "state": row["state"],
                "ordinal": row["ordinal"],
                "provider": row["provider_name"],
                "source_type": row["source_type"],
                "license": row["license_classification"],
                "schedule_version": row["schedule_version"],
                "source_url": row["source_url"],
                "confidence": row["rule_confidence"] or row["schedule_confidence"],
                "source_note": row["source_note"],
                "assumptions": _json(row["assumptions_json"], []),
                "explanation": "Expected work is not treated as complete until the owner adds evidence.",
            }
            for row in rows
        ]

    def connected_status(self, vehicle_id: str) -> dict[str, Any]:
        links = [dict(row) for row in self.connection.execute("SELECT compatibility_status,compatibility_label,linked_at FROM connected_vehicle_links WHERE vehicle_id=? ORDER BY linked_at DESC", (vehicle_id,))]
        signals = [dict(row) for row in self.connection.execute("SELECT signal_type,value_json,observed_at,caveat FROM connected_signal_observations WHERE vehicle_id=? ORDER BY observed_at DESC", (vehicle_id,))]
        for signal in signals:
            signal["value"] = _json(signal.pop("value_json"), {})
        return {
            "available": bool(links),
            "compatibility": links[0] if links else {"compatibility_status": "unknown", "compatibility_label": "Manual entry available"},
            "signals": signals,
            "copy": "Connected data is optional. Manual mileage updates always work.",
        }

    def add_service_flow(self, vehicle_id: str) -> dict[str, Any]:
        return {
            "vehicle_id": vehicle_id,
            "title": "Add a completed service",
            "principle": "Only save work the owner confirms happened.",
            "steps": [
                {"id": "items", "label": "What was done?", "input": "multi_select_service_items", "required": True},
                {"id": "date", "label": "When was it done?", "input": "date", "required": True},
                {"id": "mileage", "label": "Mileage then", "input": "non_negative_integer", "required": False},
                {"id": "details", "label": "Parts, fluids, shop, notes", "input": "structured_notes", "required": False},
                {"id": "receipt", "label": "Receipt photo or PDF", "input": "file", "required": False},
            ],
            "confirmation_copy": "This creates owner-confirmed history; it does not change unrelated unknown intervals.",
        }

    def mileage_update_model(self, vehicle_id: str) -> dict[str, Any]:
        return {
            "vehicle_id": vehicle_id,
            "title": "Update mileage",
            "fields": [
                {"id": "value", "label": "Current odometer", "type": "non_negative_integer", "required": True},
                {"id": "unit", "label": "Unit", "type": "choice", "choices": ["mi", "km"], "default": "mi"},
            ],
            "copy": "A fresh mileage reading improves due-now and upcoming estimates. It is not proof that service was completed.",
        }

    def severe_use_explanation(self, severity: str) -> dict[str, Any]:
        return {
            "value": severity,
            "label": _FRIENDLY_SEVERITY.get(severity, _FRIENDLY_SEVERITY["unknown"]),
            "plain_language": "Short trips, towing, dusty roads, long idling, stop-and-go traffic, or extreme temperatures can make some maintenance due sooner.",
            "reassurance": "This is a schedule setting, not a warning that something is wrong.",
            "action": "Review or edit driving conditions",
        }

    def accessible_reminder_copy(self, vehicle_id: str) -> dict[str, Any]:
        pref = _row_dict(self.connection.execute("SELECT enabled,channels_json,lead_days,lead_miles,updated_at FROM reminder_preferences WHERE vehicle_id=?", (vehicle_id,)).fetchone())
        if pref:
            pref["channels"] = _json(pref.pop("channels_json"), [])
        return {
            "preferences": pref,
            "aria_live": "polite",
            "copy": "Reminder settings are optional. You choose channels and lead time; reminders never mark service complete.",
            "default_channels": ["in_app", "email"],
        }

    def offline_state(self) -> dict[str, Any]:
        return {
            "title": "You're offline",
            "message": "Saved garage data stays visible. New mileage, receipts, and recall refreshes will sync when connection returns.",
            "safe_actions": ["view_history", "draft_service_record", "draft_mileage_update"],
            "blocked_actions": ["recall_refresh", "vin_decode", "connected_vehicle_refresh"],
        }

    def error_state(self, kind: str) -> dict[str, Any]:
        messages = {
            "source_unavailable": "A source is unavailable, so we kept the last known data and labeled what could not be refreshed.",
            "missing_vehicle": "We need a vehicle before building the manual.",
            "incomplete_identity": "Confirm the exact vehicle configuration to improve schedule confidence.",
        }
        return {"kind": kind, "message": messages.get(kind, "Something needs attention, but your saved records are preserved."), "tone": _NON_UPSELLING_TONE}

    def _garage_vehicle_rows(self, garage_id: str) -> list[sqlite3.Row]:
        return self.connection.execute(
            "SELECT id FROM vehicles WHERE garage_id=? AND deleted_at IS NULL ORDER BY created_at,id",
            (garage_id,),
        ).fetchall()

    def _vehicle_identity(self, vehicle_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            """
            SELECT v.id,v.nickname,v.vin_last4,v.in_service_date,c.model_year,c.make,c.model,c.drivetrain,c.identity_state,c.attributes_json
            FROM vehicles v JOIN vehicle_configurations c ON c.id=v.configuration_id
            WHERE v.id=? AND v.deleted_at IS NULL
            """,
            (vehicle_id,),
        ).fetchone()
        if not row:
            return None
        attrs = _json(row["attributes_json"], {})
        parts = [str(row["model_year"] or "").strip(), row["make"], row["model"]]
        display = " ".join(part for part in parts if part)
        return {
            "id": row["id"],
            "nickname": row["nickname"],
            "display_name": display or "Vehicle",
            "year": row["model_year"],
            "make": row["make"],
            "model": row["model"],
            "trim": attrs.get("trim"),
            "drivetrain": row["drivetrain"],
            "identity_state": row["identity_state"],
            "vin_last4": row["vin_last4"],
            "in_service_date": row["in_service_date"],
        }

    def latest_usage(self, vehicle_id: str) -> str:
        row = self.connection.execute(
            "SELECT severity FROM usage_profiles WHERE vehicle_id=? AND effective_to IS NULL ORDER BY effective_from DESC,id DESC LIMIT 1",
            (vehicle_id,),
        ).fetchone()
        return row["severity"] if row else "unknown"

    def _occurrence_sections(self, vehicle_id: str, *, as_of: date) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
        rows = self.connection.execute(
            """
            SELECT e.id,e.ordinal,e.due_mileage,e.due_date,e.state,e.assumptions_json,
                   i.id item_id,i.name item_name,i.category,
                   p.name provider_name,p.source_type,v.external_version schedule_version,
                   r.confidence,r.source_note
            FROM expected_occurrences e
            JOIN interval_rules r ON r.id=e.interval_rule_id
            JOIN service_items i ON i.id=r.service_item_id
            JOIN schedule_versions v ON v.id=r.schedule_version_id
            JOIN schedule_providers p ON p.id=v.provider_id
            WHERE e.vehicle_id=? AND e.state IN ('expected','unknown','overdue')
            ORDER BY COALESCE(e.due_date, '9999-12-31'), COALESCE(e.due_mileage, 999999999), i.name, e.ordinal
            """,
            (vehicle_id,),
        ).fetchall()
        due_now: list[dict[str, Any]] = []
        upcoming: list[dict[str, Any]] = []
        unknown: list[dict[str, Any]] = []
        for row in rows:
            item = self._occurrence_card(row)
            due_date = _parse_date(row["due_date"])
            if row["state"] == "overdue" or (due_date is not None and due_date <= as_of):
                due_now.append(item)
            elif row["state"] == "unknown":
                unknown.append(item)
            else:
                upcoming.append(item)
        return due_now, upcoming, unknown

    def _occurrence_card(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "occurrence_id": row["id"],
            "item_id": row["item_id"],
            "title": row["item_name"],
            "category": row["category"],
            "ordinal": row["ordinal"],
            "state": row["state"],
            "due_mileage": row["due_mileage"],
            "due_date": row["due_date"],
            "source_label": f"{row['provider_name']} {row['schedule_version']}",
            "source_type": row["source_type"],
            "confidence": row["confidence"],
            "assumptions": _json(row["assumptions_json"], []),
            "owner_copy": "Add a service record if this was already completed.",
            "fear_free_copy": "This is a planning item, not a diagnosis.",
            "drilldown_id": row["id"],
        }

    def _confidence_for_odometer(self, vehicle_id: str, observed_at: str) -> str:
        row = self.connection.execute(
            """
            SELECT c.level FROM odometer_observations o
            LEFT JOIN confidence_assessments c ON c.id=o.confidence_id
            WHERE o.vehicle_id=? AND o.observed_at=? ORDER BY o.id DESC LIMIT 1
            """,
            (vehicle_id, observed_at),
        ).fetchone()
        return row["level"] if row and row["level"] else "unknown"

    def _status_copy(self, counts: dict[str, int]) -> str:
        if counts["due_now"]:
            return "Some items need review. Add records for work already done, or plan the next service."
        if counts["upcoming"]:
            return "You're set for now. Here's what is coming next."
        if counts["unknown"]:
            return "Some intervals need more source or history before we can classify them."
        return _HELPFUL_EMPTY_STATE

    def _layout_contract(self, screen: str) -> dict[str, Any]:
        return {
            "screen": screen,
            "mobile_first": True,
            "min_touch_target_px": 44,
            "primary_navigation": "bottom_tabs",
            "supports_multi_vehicle": True,
            "accessibility": ["semantic_sections", "aria_live_polite_reminders", "plain_language_status", "no_color_only_meaning"],
        }
