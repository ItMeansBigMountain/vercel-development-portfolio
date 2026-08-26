from __future__ import annotations

import json
import re
from pathlib import Path
from unittest import TestCase


ROOT = Path(__file__).resolve().parents[1]


class CurriculumParityTests(TestCase):
    def test_app_curriculum_matches_canonical_manifest(self) -> None:
        manifest = json.loads(
            (ROOT / "curriculum" / "canonical-curriculum-manifest.json").read_text()
        )
        source = (ROOT / "app" / "src" / "curriculum.ts").read_text()
        match = re.search(
            r"export const lessons: Lesson\[\] = (\[.*?\n\]);", source, re.DOTALL
        )
        if match is None:
            self.fail("app curriculum must remain a JSON-compatible array")
        app_lessons = json.loads(match.group(1))

        expected = [
            {
                "id": lesson["id"],
                "title": lesson["title"],
                "module": lesson["module"],
                "description": lesson["studentFacingGoal"],
                "starterCode": lesson["exercise"]["starterCode"],
                "rubric": lesson["assessment"]["rubric"],
                "prerequisites": lesson["prerequisites"],
                "ageBand": lesson["ageBand"],
                "exercise": lesson["exercise"]["studentPrompt"],
                "teacherNotes": lesson["exercise"]["teacherNotes"],
                "assessment": lesson["assessment"]["evidenceTypes"],
                "project": lesson["project"]["prompt"],
                "progressFields": [
                    "attempted",
                    "completed",
                    "teacher-reviewed",
                    "mastered",
                ],
            }
            for lesson in manifest["lessons"]
        ]
        self.assertEqual(app_lessons, expected)
