from __future__ import annotations

import sqlite3
import tempfile
import unittest
from datetime import date
from pathlib import Path

from burnoutboyz.db import Database
from burnoutboyz.auth import AuthorizationError
from burnoutboyz.ux import OwnersManualUXService


class OwnersManualUXTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Database(Path(self.tmp.name) / "burnoutboyz.db")
        self.db.migrate()
        self.conn = self.db.connection
        self._seed()
        self.ux = OwnersManualUXService(self.conn, actor_user_id="u1")

    def tearDown(self) -> None:
        self.db.close()
        self.tmp.cleanup()

    def _seed(self) -> None:
        self.conn.execute("INSERT INTO users(id,email,created_at) VALUES ('u1','owner@example.com','2026-01-01T00:00:00+00:00')")
        self.conn.execute("INSERT INTO users(id,email,created_at) VALUES ('u2','other@example.com','2026-01-01T00:00:00+00:00')")
        self.conn.execute("INSERT INTO garages(id,user_id,name,created_at) VALUES ('g1','u1','Daily drivers','2026-01-01T00:00:00+00:00')")
        self.conn.execute("INSERT INTO provenance_sources(id,source_type,provider_name,source_uri,retrieved_at,license_classification) VALUES ('src_manual','manual','vehicle owner','manual-entry','2026-01-01T00:00:00+00:00','user supplied')")
        self.conn.execute("INSERT INTO provenance_sources(id,source_type,provider_name,source_uri,retrieved_at,license_classification) VALUES ('src_sched','licensed','Synthetic Schedule','file://fixture','2026-01-01T00:00:00+00:00','synthetic test data')")
        self.conn.execute("INSERT INTO confidence_assessments(id,level,score,rationale,source_id,created_at) VALUES ('conf_manual','medium',0.6,'owner entered','src_manual','2026-01-01T00:00:00+00:00')")
        self.conn.execute("INSERT INTO vehicle_configurations(id,model_year,make,model,drivetrain,identity_state,source_id,confidence_id,attributes_json) VALUES ('cfg1',2020,'Honda','Civic','FWD','confirmed','src_manual','conf_manual',?)", ('{"trim":"EX"}',))
        self.conn.execute("INSERT INTO vehicles(id,garage_id,configuration_id,nickname,vin_last4,in_service_date,created_at) VALUES ('v1','g1','cfg1','Civic','1234','2020-01-01','2026-01-01T00:00:00+00:00')")
        self.conn.execute("INSERT INTO odometer_observations(id,vehicle_id,observed_at,distance_value,distance_unit,source_id,confidence_id,created_at) VALUES ('odo1','v1','2026-06-01T00:00:00+00:00',52000,'mi','src_manual','conf_manual','2026-06-01T00:00:00+00:00')")
        self.conn.execute("INSERT INTO usage_profiles(id,vehicle_id,severity,effective_from,answers_json,source_id,confidence_id,created_at) VALUES ('usage1','v1','severe','2026-01-01T00:00:00+00:00',?, 'src_manual','conf_manual','2026-01-01T00:00:00+00:00')", ('{"extended_idling_or_stop_go":true}',))
        self.conn.execute("INSERT INTO schedule_providers(id,external_id,name,source_type,license_classification,created_at) VALUES ('prov1','synthetic','Synthetic Schedule','synthetic','synthetic test data','2026-01-01T00:00:00+00:00')")
        self.conn.execute("INSERT INTO schedule_versions(id,provider_id,external_version,source_url,effective_from,retrieved_at,region,applicability_json,license_classification,confidence,content_hash,created_at) VALUES ('ver1','prov1','2026.1','file://fixture','2026-01-01','2026-01-01T00:00:00+00:00','US','{}','synthetic test data','medium','abc','2026-01-01T00:00:00+00:00')")
        self.conn.execute("INSERT INTO service_items(id,provider_id,external_id,name,category,canonical_key) VALUES ('oil','prov1','oil','Oil change','engine','oil_change')")
        self.conn.execute("INSERT INTO service_items(id,provider_id,external_id,name,category,canonical_key) VALUES ('tires','prov1','tires','Rotate tires','tires','tire_rotation')")
        self.conn.execute("INSERT INTO interval_rules(id,schedule_version_id,service_item_id,external_id,trigger_mode,mileage_interval,time_interval_months,usage_severity,applicability_json,confidence,source_note) VALUES ('rule_oil','ver1','oil','oil_5k','whichever_first',5000,6,'severe','{}','medium','Synthetic test interval')")
        self.conn.execute("INSERT INTO interval_rules(id,schedule_version_id,service_item_id,external_id,trigger_mode,mileage_interval,time_interval_months,usage_severity,applicability_json,confidence,source_note) VALUES ('rule_tires','ver1','tires','tires_60k','mileage_only',60000,NULL,'all','{}','medium','Synthetic test interval')")
        self.conn.execute("INSERT INTO expected_occurrences(id,vehicle_id,interval_rule_id,ordinal,due_mileage,due_date,state,calculated_at,assumptions_json) VALUES ('occ_due','v1','rule_oil',10,50000,'2025-12-01','overdue','2026-06-01T00:00:00+00:00','[]')")
        self.conn.execute("INSERT INTO expected_occurrences(id,vehicle_id,interval_rule_id,ordinal,due_mileage,due_date,state,calculated_at,assumptions_json) VALUES ('occ_next','v1','rule_tires',1,60000,NULL,'expected','2026-06-01T00:00:00+00:00','[]')")
        self.conn.execute("INSERT INTO service_records(id,vehicle_id,service_item_id,performed_at,odometer_value,odometer_unit,status,shop_name,created_at) VALUES ('rec1','v1','oil','2026-01-15',45000,'mi','confirmed','Local Shop','2026-01-15T00:00:00+00:00')")
        self.conn.execute("INSERT INTO service_record_items(service_record_id,service_item_id) VALUES ('rec1','oil')")
        self.conn.execute("INSERT INTO recall_refreshes(id,vehicle_id,lookup_basis,state,source_uri,checked_at,caveat) VALUES ('refresh1','v1','year_make_model','resolved','https://api.nhtsa.gov/recalls/recallsByVehicle','2026-06-01T00:00:00+00:00','model-level caveat')")
        self.conn.execute("INSERT INTO recalls(id,vehicle_id,campaign_number,component,summary,remedy,report_received_date,status,source_id,checked_at) VALUES ('recall1','v1','20V000','AIR BAGS','Air bag issue','Dealer repair','2020-01-01','unknown','src_sched','2026-06-01T00:00:00+00:00')")
        self.conn.execute("INSERT INTO reminder_preferences(vehicle_id,enabled,channels_json,lead_days,lead_miles,updated_at) VALUES ('v1',1,?,14,500,'2026-06-01T00:00:00+00:00')", ('["in_app"]',))
        self.conn.commit()

    def test_vehicle_manual_groups_due_history_recalls_and_sources(self) -> None:
        manual = self.ux.vehicle_manual("v1", as_of=date(2026, 6, 1))

        self.assertTrue(manual["layout"]["mobile_first"])
        self.assertEqual(manual["counts"]["due_now"], 1)
        self.assertEqual(manual["counts"]["upcoming"], 1)
        self.assertEqual(manual["counts"]["confirmed"], 1)
        self.assertEqual(manual["counts"]["recalls"], 1)
        self.assertEqual(manual["due_now"][0]["title"], "Oil change")
        self.assertEqual(manual["history"][0]["evidence_label"], "Owner-confirmed record")
        self.assertIn("not a diagnosis", manual["due_now"][0]["fear_free_copy"])
        self.assertIn("NHTSA", manual["recalls"]["caveat"])
        self.assertEqual(manual["source_confidence_drilldown"][0]["provider"], "Synthetic Schedule")

    def test_garage_dashboard_is_multi_vehicle_and_fear_free(self) -> None:
        dashboard = self.ux.garage_dashboard("u1", as_of=date(2026, 6, 1))

        self.assertEqual(dashboard["screen"], "garage_dashboard")
        self.assertIn("never fear-based", dashboard["tone"])
        self.assertEqual(dashboard["garages"][0]["totals"]["vehicles"], 1)
        self.assertEqual(dashboard["garages"][0]["vehicles"][0]["primary_action"], "Review due now")
        self.assertIn("Synthetic Schedule", dashboard["garages"][0]["vehicles"][0]["next_due"]["source_label"])

    def test_action_models_cover_service_mileage_reminders_and_offline(self) -> None:
        manual = self.ux.vehicle_manual("v1", as_of=date(2026, 6, 1))

        self.assertEqual(manual["actions"]["add_service"]["steps"][0]["input"], "multi_select_service_items")
        self.assertEqual(manual["actions"]["update_mileage"]["fields"][0]["type"], "non_negative_integer")
        self.assertEqual(manual["actions"]["reminders"]["aria_live"], "polite")
        self.assertIn("recall_refresh", manual["offline_state"]["blocked_actions"])
        self.assertIn("kept the last known data", manual["error_state"]["message"])

    def test_cross_tenant_vehicle_manual_is_denied_without_leaking_existence(self) -> None:
        other = OwnersManualUXService(self.conn, actor_user_id="u2")
        with self.assertRaisesRegex(AuthorizationError, "resource not found"):
            other.vehicle_manual("v1", as_of=date(2026, 6, 1))


if __name__ == "__main__":
    unittest.main()
