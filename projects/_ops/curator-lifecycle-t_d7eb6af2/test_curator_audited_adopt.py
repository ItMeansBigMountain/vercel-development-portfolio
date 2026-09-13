from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("curator_audited_adopt.py")
spec = importlib.util.spec_from_file_location("curator_audited_adopt", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PromotionAuditTests(unittest.TestCase):
    def make_skill(self, root: Path, name: str, content: str) -> Path:
        path = root / "skills" / "testing" / name
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text(content, encoding="utf-8")
        return path

    def test_valid_skill_passes_existing_static_and_guard_checks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_skill(root, "safe-skill", """---
name: safe-skill
description: Use when testing. Runs a harmless verification.
---

# Safe skill

Read the fixture and report its result.
""")
            result = module.audit_skill(root, "safe-skill")
            self.assertTrue(result["passed"], result)
            self.assertEqual([], result["failures"])

    def test_malformed_skill_fails_with_actionable_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_skill(root, "bad-skill", "no frontmatter\n")
            result = module.audit_skill(root, "bad-skill")
            self.assertFalse(result["passed"])
            self.assertTrue(any("frontmatter" in item for item in result["failures"]))

    def test_ambiguous_or_missing_skill_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = module.audit_skill(Path(raw), "missing")
            self.assertFalse(result["passed"])
            self.assertIn("exactly one", result["failures"][0])


if __name__ == "__main__":
    unittest.main()
