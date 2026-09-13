#!/usr/bin/env python3
"""Fail-closed static/security audit gate for Curator adoption."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROFILE_ROOT = Path("/opt/data/profiles")
DEFAULT_HOME = Path("/opt/data")
HERMES = "/opt/hermes/.venv/bin/hermes"


def home_for(profile: str) -> Path:
    return DEFAULT_HOME if profile == "default" else PROFILE_ROOT / profile


def find_skill(home: Path, name: str) -> Path | None:
    matches = [p.parent for p in (home / "skills").rglob("SKILL.md") if p.parent.name == name]
    return matches[0] if len(matches) == 1 else None


def audit_skill(home: Path, name: str) -> dict:
    os.environ["HERMES_HOME"] = str(home)
    sys.path.insert(0, "/opt/hermes")
    from tools.skill_manager_tool import (
        _validate_content_size,
        _validate_frontmatter,
        _validate_name,
    )
    from tools.skills_guard import format_scan_report, scan_skill, should_allow_install

    failures: list[str] = []
    skill_dir = find_skill(home, name)
    if skill_dir is None:
        failures.append("skill must resolve to exactly one local SKILL.md")
        return {"skill": name, "passed": False, "failures": failures}

    skill_md = skill_dir / "SKILL.md"
    try:
        content = skill_md.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        failures.append(f"SKILL.md is not readable UTF-8: {exc}")
        return {"skill": name, "path": str(skill_dir), "passed": False, "failures": failures}

    for check, error in (
        ("name", _validate_name(name)),
        ("frontmatter", _validate_frontmatter(content, new_skill=True)),
        ("content_size", _validate_content_size(content)),
    ):
        if error:
            failures.append(f"{check}: {error}")

    scan_summary = "not run"
    try:
        scan = scan_skill(skill_dir, source="curator-promotion")
        allowed, reason = should_allow_install(scan)
        scan_summary = format_scan_report(scan)
        if allowed is not True:
            failures.append(f"security_scan: {reason}; {scan_summary}")
    except Exception as exc:
        failures.append(f"security_scan failed closed: {type(exc).__name__}: {exc}")

    return {
        "skill": name,
        "path": str(skill_dir),
        "passed": not failures,
        "checks": ["name", "frontmatter_new_skill", "content_size", "skills_guard"],
        "failures": failures,
        "security_scan": scan_summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("skills", nargs="+")
    args = parser.parse_args()

    home = home_for(args.profile)
    if not (home / "skills").is_dir():
        parser.error(f"profile skills directory not found: {home / 'skills'}")

    audits = [audit_skill(home, name) for name in args.skills]
    rejected = [a for a in audits if not a["passed"]]
    promoted: list[str] = []
    command_results: list[dict] = []

    if not rejected:
        command = [HERMES]
        if args.profile != "default":
            command += ["--profile", args.profile]
        command += ["curator", "adopt", *args.skills]
        if args.dry_run:
            command.append("--dry-run")
        proc = subprocess.run(command, text=True, capture_output=True, check=False)
        command_results.append({"command": command, "returncode": proc.returncode,
                                "stdout": proc.stdout, "stderr": proc.stderr})
        if proc.returncode == 0 and not args.dry_run:
            promoted = list(args.skills)
        elif proc.returncode != 0:
            rejected.append({"skill": "<adoption-command>", "passed": False,
                             "failures": [f"adoption command exited {proc.returncode}"]})

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "profile": args.profile,
        "dry_run": args.dry_run,
        "scanned": len(audits),
        "passed": sum(a["passed"] for a in audits),
        "rejected": len(rejected),
        "promoted": len(promoted),
        "audits": audits,
        "command_results": command_results,
    }
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("profile", "dry_run", "scanned", "passed", "rejected", "promoted")}))
    if rejected:
        for row in rejected:
            print(f"REJECTED {row['skill']}: {'; '.join(row['failures'])}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
