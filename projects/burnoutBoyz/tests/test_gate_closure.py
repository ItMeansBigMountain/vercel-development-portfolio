from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from burnoutboyz.auth import AuthorizationError
from burnoutboyz.db import Database
from burnoutboyz.maintenance import MaintenanceService
from burnoutboyz.timeline import ScheduleRule, ServiceConfirmation, VehicleSnapshot, evaluate_rule


class GateClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Database(Path(self.tmp.name) / "gate.db")
        self.db.migrate()
        self.conn = self.db.connection
        self.conn.execute("INSERT INTO users(id,email,created_at) VALUES ('u1','one@example.test','2026-01-01')")
        self.conn.execute("INSERT INTO users(id,email,created_at) VALUES ('u2','two@example.test','2026-01-01')")
        self.conn.execute("INSERT INTO garages(id,user_id,name,created_at) VALUES ('g1','u1','one','2026-01-01')")
        self.conn.execute("INSERT INTO provenance_sources(id,source_type,provider_name,source_uri,retrieved_at,license_classification) VALUES ('s','manual','owner','manual-entry','2026-01-01','user supplied')")
        self.conn.execute("INSERT INTO vehicle_configurations(id,model_year,make,model,identity_state,source_id,attributes_json) VALUES ('c',2020,'Synthetic','Fixture','confirmed','s','{}')")
        self.conn.execute("INSERT INTO vehicles(id,garage_id,configuration_id,created_at) VALUES ('v1','g1','c','2026-01-01')")
        self.conn.execute("INSERT INTO schedule_providers(id,external_id,name,source_type,license_classification,created_at) VALUES ('p','fixture','Synthetic fixture','synthetic','synthetic test data','2026-01-01')")
        self.conn.execute("INSERT INTO service_items(id,provider_id,external_id,name,category) VALUES ('oil','p','oil','Oil','engine')")
        self.conn.commit()

    def tearDown(self) -> None:
        self.db.close()
        self.tmp.cleanup()

    def test_cross_tenant_read_write_export_and_delete_are_denied(self) -> None:
        service = MaintenanceService(self.conn, receipt_root=Path(self.tmp.name) / "receipts", actor_user_id="u2")
        operations = [
            lambda: service.list_records("v1"),
            lambda: service.add_record("v1", performed_at="2026-01-01", item_ids=["oil"]),
            lambda: service.export_vehicle("v1"),
            lambda: service.delete_vehicle("v1"),
        ]
        for operation in operations:
            with self.subTest(operation=operation), self.assertRaises(AuthorizationError):
                operation()

    def test_receipts_reject_oversize_and_unsafe_types_and_export_redacts_storage(self) -> None:
        service = MaintenanceService(self.conn, receipt_root=Path(self.tmp.name) / "receipts", actor_user_id="u1", max_receipt_bytes=8)
        for receipt in (
            {"content": b"123456789", "media_type": "image/jpeg", "filename": "x.jpg"},
            {"content": b"ok", "media_type": "text/html", "filename": "../../x.html"},
        ):
            with self.subTest(receipt=receipt), self.assertRaises(ValueError):
                service.add_record("v1", performed_at="2026-01-01", item_ids=["oil"], receipt=receipt)

        service.add_record("v1", performed_at="2026-01-02", item_ids=["oil"], receipt={"content": b"pdf", "media_type": "application/pdf", "filename": "../../safe.pdf"})
        exported = service.export_vehicle("v1")
        receipt = exported["service_records"][0]["receipts"][0]
        self.assertNotIn("storage_key", receipt)
        self.assertNotIn(str(Path(self.tmp.name)), str(exported))

    def test_notification_output_is_deduped_and_bounded(self) -> None:
        service = MaintenanceService(self.conn, receipt_root=Path(self.tmp.name), actor_user_id="u1", max_notifications_per_run=2)
        service.set_reminder_preferences("v1", enabled=True, channels=["push"], lead_days=30, lead_miles=1000)
        items = [{"occurrence_id": "same", "item_id": "oil", "due_date": "2026-01-02"}] * 5
        notices = service.notifications("v1", as_of=date(2026, 1, 1), current_mileage=0, upcoming=items)
        self.assertEqual(len(notices), 1)


class SyntheticAutomotiveMatrixTests(unittest.TestCase):
    def rule(self, **changes: object) -> ScheduleRule:
        values = dict(rule_id="r", item_id="oil", item_name="Oil", provider_id="synthetic", provider_name="Synthetic test fixture", schedule_version="fixture-v1", source_url="file://synthetic-fixture", source_type="synthetic_test_fixture", confidence="medium", severity="all", trigger_mode="mileage_only", applicability={"trim": "EX"}, mileage_interval=5000)
        values.update(changes)
        return ScheduleRule(**values)

    def vehicle(self, **changes: object) -> VehicleSnapshot:
        values = dict(vehicle_id="v", odometer_miles=12000, as_of=date(2026, 1, 1), in_service_date=date(2025, 1, 1), usage_severity="normal", applicability={"trim": "EX"})
        values.update(changes)
        return VehicleSnapshot(**values)

    def test_interval_severity_applicability_version_and_tolerance_matrix(self) -> None:
        cases = [
            (self.rule(), self.vehicle(), "overdue", 2),
            (self.rule(trigger_mode="time_only", mileage_interval=None, time_interval_months=6), self.vehicle(), "overdue", 2),
            (self.rule(trigger_mode="whichever_first", time_interval_months=6), self.vehicle(), "overdue", 2),
            (self.rule(recurrence="one_time", initial_mileage=1000), self.vehicle(), "overdue", 1),
            (self.rule(severity="severe"), self.vehicle(), "not_applicable", 0),
            (self.rule(), self.vehicle(applicability={"trim": "LX"}), "not_applicable", 0),
            (self.rule(mileage_tolerance=3000), self.vehicle(odometer_miles=7000), "unknown", 1),
        ]
        for rule, vehicle, classification, count in cases:
            with self.subTest(rule=rule, vehicle=vehicle):
                result = evaluate_rule(vehicle, rule, [])
                self.assertEqual((result.classification, result.expected_count), (classification, count))
                self.assertEqual(result.source.source_type, "synthetic_test_fixture")

        old = ServiceConfirmation("done", "oil", date(2025, 1, 1), 5000, "fixture-v0")
        result = evaluate_rule(self.vehicle(odometer_miles=5000), self.rule(), [old])
        self.assertEqual(result.confirmed_count, 0)


if __name__ == "__main__":
    unittest.main()