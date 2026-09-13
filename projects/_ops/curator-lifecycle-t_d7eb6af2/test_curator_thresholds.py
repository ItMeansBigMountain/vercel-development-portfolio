from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

sys.path.insert(0, "/opt/hermes")
from agent import curator
from tools import skill_usage


class CuratorThresholdSemanticsTests(unittest.TestCase):
    NOW = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)

    def row(self, age: timedelta, state: str = skill_usage.STATE_ACTIVE) -> dict:
        return {
            "name": "candidate",
            "pinned": False,
            "state": state,
            "use_count": 1,
            "last_activity_at": (self.NOW - age).isoformat(),
            "created_at": (self.NOW - age).isoformat(),
            "_persisted": True,
        }

    def transition(self, row: dict):
        with (
            patch.object(skill_usage, "curated_report", return_value=[row]),
            patch.object(skill_usage, "set_state") as set_state,
            patch.object(skill_usage, "archive_skill", return_value=(True, "ok")) as archive,
            patch.object(curator, "get_stale_after_days", return_value=30),
            patch.object(curator, "get_archive_after_days", return_value=90),
            patch.object(curator, "_cron_referenced_skills", return_value=set()),
        ):
            counts = curator.apply_automatic_transitions(now=self.NOW)
        return counts, set_state, archive

    def test_before_30_days_is_retained_active(self):
        counts, set_state, archive = self.transition(self.row(timedelta(days=30) - timedelta(seconds=1)))
        self.assertEqual(0, counts["marked_stale"])
        set_state.assert_not_called()
        archive.assert_not_called()

    def test_exactly_30_days_marks_stale(self):
        counts, set_state, archive = self.transition(self.row(timedelta(days=30)))
        self.assertEqual(1, counts["marked_stale"])
        set_state.assert_called_once_with("candidate", skill_usage.STATE_STALE)
        archive.assert_not_called()

    def test_before_90_days_is_not_archived(self):
        counts, _set_state, archive = self.transition(
            self.row(timedelta(days=90) - timedelta(seconds=1), skill_usage.STATE_STALE)
        )
        self.assertEqual(0, counts["archived"])
        archive.assert_not_called()

    def test_exactly_90_days_archives(self):
        counts, _set_state, archive = self.transition(
            self.row(timedelta(days=90), skill_usage.STATE_STALE)
        )
        self.assertEqual(1, counts["archived"])
        archive.assert_called_once_with("candidate")


if __name__ == "__main__":
    unittest.main()
