from __future__ import annotations

from datetime import datetime, UTC
from unittest import TestCase

import json
from pathlib import Path

from coding_school.curriculum import curriculum_catalog
from coding_school.models import Account, Evidence, MasteryLevel, PortfolioProject, ReviewStatus, Role, Submission
from coding_school.service import LearningPlatform


class LearningPlatformTests(TestCase):
    def setUp(self) -> None:
        self.platform = LearningPlatform()
        for account in (
            Account("teacher-demo", Role.TEACHER, "Coach Rivera", True),
            Account("student-demo", Role.STUDENT, "Learner One", True),
            Account("parent-demo", Role.PARENT, "Family View", True),
            Account("admin-demo", Role.ADMIN, "Ops Lead", True),
        ):
            self.platform.add_account(account)
        self.platform.link_parent("parent-demo", "student-demo")
        self.platform.assign_lesson("teacher-demo", "student-demo", "student-linear-search")

    def submit_linear_search(self) -> None:
        self.platform.submit(Submission(
            "submission-1",
            "student-demo",
            "student-linear-search",
            (Evidence("runnable-code", "Linear search returns the matching index", "examples/linear_search.py"),),
            "The value is the treasure and the index is its address.",
        ))

    def test_curriculum_source_order_and_scope(self) -> None:
        catalog = curriculum_catalog()
        teacher_items = [item for item in catalog if item.track == "teacher"]
        basic_items = [item for item in catalog if item.module == "Basic 13"]
        linear_search = next(item for item in catalog if item.id == "student-linear-search")
        self.assertGreaterEqual(len(teacher_items), 3)
        self.assertEqual(teacher_items[0].stage, "T0")
        self.assertEqual(len(basic_items), 13)
        self.assertIn("indexing", linear_search.concept_tags)
        self.assertTrue(all(item.age_band == "adult teacher/coaches" for item in teacher_items))
        self.assertTrue(any(item.module == "Data Objects and Arrays" for item in catalog))
        self.assertTrue(any(item.module == "APIs, JSON, Fetch, and Errors" for item in catalog))
        self.assertTrue(all((item.exercise is None or item.exercise.solution_visibility == "teacher-only") for item in catalog))

    def test_curriculum_manifest_matches_required_module_map(self) -> None:
        manifest_path = Path(__file__).resolve().parents[1] / "curriculum" / "canonical-curriculum-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        lesson_ids = {item["id"] for item in manifest["lessons"]}
        module_ids = {item["id"] for item in manifest["modules"]}
        self.assertIn("basic-13", module_ids)
        self.assertIn("javascript-data", module_ids)
        self.assertIn("api-json-fetch", module_ids)
        self.assertEqual(len([item for item in manifest["lessons"] if item["moduleId"] == "basic-13"]), 13)
        self.assertIn("student-js-manipulation-01", lesson_ids)
        self.assertIn("student-api-errors-01", lesson_ids)
        self.assertTrue(all(item["ageBand"] in ("10-14 JavaScript Core", "adult teacher/coaches") for item in manifest["lessons"]))
        self.assertTrue(all(item["exercise"]["solutionVisibility"] == "teacher-only" for item in manifest["lessons"]))
        self.assertIn("teacherReviewStatus", manifest["progressFields"])
        self.assertNotIn("blocked:", manifest["canonicalDriveFolder"]["syncStatus"])
        self.assertEqual(manifest["canonicalDriveFolder"]["syncVerifiedAt"], "2026-08-29")

    def test_source_of_truth_uses_canonical_basic_13_order(self) -> None:
        source = (Path(__file__).resolve().parents[1] / "CURRICULUM_SOURCE_OF_TRUTH.md").read_text()
        expected = [
            "8. Count above Y.",
            "9. Square values.",
            "10. Replace negatives.",
            "11. Min/max/avg.",
            "12. Shift values.",
            "13. Replace negatives with Dojo.",
        ]
        positions = [source.index(item) for item in expected]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("Convert matching values to zero", source)
        self.assertNotIn("Replace negatives with `below zero`", source)

    def test_demo_student_privacy_boundary(self) -> None:
        with self.assertRaises(ValueError):
            self.platform.add_account(Account("real-child", Role.STUDENT, "Real Child", False))
        with self.assertRaises(ValueError):
            self.platform.update_profile("student-demo", {"schoolEmail": "learner@example.com"})

    def test_submission_needs_evidence_and_reflection(self) -> None:
        with self.assertRaises(ValueError):
            self.platform.submit(Submission("empty", "student-demo", "student-linear-search", (), ""))

    def test_teacher_review_controls_mastery_and_badges(self) -> None:
        self.submit_linear_search()
        dashboard = self.platform.teacher_dashboard("teacher-demo")
        self.assertEqual(dashboard["pending_reviews"], ("submission-1",))
        with self.assertRaises(ValueError):
            self.platform.review_submission(
                "submission-1",
                reviewer_id="teacher-demo",
                status=ReviewStatus.NEEDS_REVISION,
                mastery=MasteryLevel.PRACTICING,
                badge_ids=("trace-passed",),
                parent_safe_summary="Try another trace before mastery.",
            )
        self.platform.review_submission(
            "submission-1",
            reviewer_id="teacher-demo",
            status=ReviewStatus.APPROVED,
            mastery=MasteryLevel.PROFICIENT,
            badge_ids=("trace-passed", "explanation-approved"),
            parent_safe_summary="Learner One traced a search and explained index versus value independently.",
        )
        progress = self.platform.student_progress("student-demo")
        self.assertEqual(progress.completed_lessons, 1)
        self.assertEqual(progress.mastered_lessons, 1)
        self.assertEqual(progress.badges, ("explanation-approved", "trace-passed"))

    def test_parent_and_admin_dashboards_are_role_scoped(self) -> None:
        self.submit_linear_search()
        parent = self.platform.parent_dashboard("parent-demo", "student-demo")
        self.assertEqual(parent["student_name"], "Learner One")
        admin = self.platform.admin_dashboard("admin-demo")
        self.assertEqual(admin["real_student_records"], 0)
        self.assertEqual(admin["demo_accounts"], 4)
        with self.assertRaises(PermissionError):
            self.platform.admin_dashboard("teacher-demo")

    def test_portfolio_iterations_are_private_and_reviewable(self) -> None:
        project = PortfolioProject("project-1", "student-demo", "Treasure Hunt", "Search game demo")
        self.platform.create_project(project)
        self.platform.add_project_iteration(
            "project-1",
            student_id="student-demo",
            artifact="https://example.invalid/demo",
            reflection="I built the smallest runnable version first.",
        )
        self.platform.review_project_iteration(
            "project-1",
            reviewer_id="teacher-demo",
            feedback="Good scope; add one missing-value case next.",
            approved=True,
            reviewed_at=datetime.now(UTC),
        )
        reviewed = self.platform.project("project-1", requester_id="admin-demo")
        self.assertEqual(reviewed.milestones, ("idea-scoped", "first-run"))
        self.assertTrue(reviewed.iterations[-1].approved)
        with self.assertRaises(KeyError):
            self.platform.project("project-1", requester_id="unknown")
