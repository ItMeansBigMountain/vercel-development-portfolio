#!/usr/bin/env python3
"""Render the production-candidate review queue from verified evidence."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BROWSER = ROOT / "production-candidate-preview-browser-verification.json"
OUT_JSON = ROOT / "production-candidate-review-queue.json"
OUT_MD = ROOT / "production-candidate-review-queue.md"

SHARED_REPO = "https://github.com/ItMeansBigMountain/HeRmEz"
NO_PREVIEW = "No Vercel Preview-environment deployment exists; existing Vercel deployment is target=production and is not an acceptable review build."
NO_REMOTE_WORKFLOW = "No matching GitHub Actions Vercel-development workflow is present on the repository default branch."

CANDIDATES = [
    {"order": 1, "app": "tweetBetweenTheLines", "owner_repo": SHARED_REPO, "source": "projects/tweetBetweenTheLines", "kind": "web/universal app", "vercel_project": "tweetbetweenthelines", "immutable_preview": "https://tweetbetweenthelines-2hr5230u9-itmeansbigmountains-projects.vercel.app", "persistent_preview": None, "deployment_id": "dpl_37rzk9EjZYGdLk1FrcUcSkuksNBj", "deployment_sha": "0be45e3102379f0c5fb9ad5fe363c47d62fe27aa", "github_actions": {"remote_workflow": ".github/workflows/tweet-between-the-lines-vercel-dev.yml", "latest_run": "https://github.com/ItMeansBigMountain/HeRmEz/actions/runs/33348943516", "latest_conclusion": "failure"}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": "Remote workflow exists but its only run failed before tests/build/deploy because projects/tweetBetweenTheLines/package-lock.json was absent at remote commit 5d1fd04272fec8b46e085aa1871b2ca5e80add4f; no stable preview alias exists. Reconcile remote history/source first, then rerun Actions."},
    {"order": 2, "app": "Journal AI", "owner_repo": SHARED_REPO, "source": "projects/journal-ai", "kind": "web/universal app", "vercel_project": "journal-ai", "immutable_preview": "https://journal-qmx4djhze-itmeansbigmountains-projects.vercel.app", "persistent_preview": None, "deployment_id": "dpl_oC6Hs3NcuYCZ3NLyFaBj2xAsWByX", "deployment_sha": "9e0a340c39f052b5cfe9f5ae8c8a79aea9350e90", "github_actions": {"remote_workflow": None, "latest_run": None, "latest_conclusion": None}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": "Preview is manual/untraceable (Vercel gitSource=null), has no stable alias, and desktop emits an unexplained 404 console error. A local workflow exists but is not on GitHub's default branch."},
    {"order": 3, "app": "Coding School / Algorithm Academy", "owner_repo": SHARED_REPO, "source": "projects/coding-school-platform", "kind": "web/universal app", "vercel_project": "coding-school-platform", "immutable_preview": "https://coding-school-platform-5hh2k4xao-itmeansbigmountains-projects.vercel.app", "persistent_preview": None, "deployment_id": "dpl_5kknrFDQcYMrHHanMfojmRciQCrT", "deployment_sha": "da5507236c741fec2d16e03cd0796c8ee5c03e0d", "github_actions": {"remote_workflow": None, "latest_run": None, "latest_conclusion": None}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": "Preview is manual/untraceable (Vercel gitSource=null), has no stable alias, and mobile viewport overflows (scrollWidth > clientWidth). Local CI/preview workflow is not on GitHub's default branch."},
    {"order": 4, "app": "CombatAtlas Web", "owner_repo": "https://github.com/ItMeansBigMountain/CombatAtlas", "source": "projects/CombatAtlas", "kind": "web app", "vercel_project": "combatatlas", "immutable_preview": None, "persistent_preview": None, "github_actions": {"remote_workflow": None, "latest_run": None, "latest_conclusion": None}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": NO_PREVIEW + " " + NO_REMOTE_WORKFLOW},
    {"order": 5, "app": "CombatAtlas Universal", "owner_repo": "https://github.com/ItMeansBigMountain/CombatAtlas", "source": "projects/CombatAtlas/mobile", "kind": "web/universal app", "vercel_project": "combatatlas-mobile", "immutable_preview": None, "persistent_preview": None, "github_actions": {"remote_workflow": None, "latest_run": None, "latest_conclusion": None}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": NO_PREVIEW + " Local production-only workflow is not published and violates the Vercel-development-only policy."},
    {"order": 6, "app": "Wornly", "owner_repo": "https://github.com/ItMeansBigMountain/fashion-social", "source": "projects/_archive/wornly", "kind": "web/universal commerce app", "vercel_project": "fashion-social", "immutable_preview": None, "persistent_preview": None, "github_actions": {"remote_workflow": None, "latest_run": None, "latest_conclusion": None}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": NO_PREVIEW + " " + NO_REMOTE_WORKFLOW},
    {"order": 7, "app": "Card Intel Scanner", "owner_repo": SHARED_REPO, "source": "projects/_archive/card-intel-scanner", "kind": "web scanner app", "vercel_project": "card-intel-scanner", "immutable_preview": None, "persistent_preview": None, "github_actions": {"remote_workflow": None, "latest_run": None, "latest_conclusion": None}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": NO_PREVIEW + " " + NO_REMOTE_WORKFLOW},
    {"order": 8, "app": "Honda Tech Upgrade", "owner_repo": SHARED_REPO, "source": "projects/honda-tech-upgrade", "kind": "web app", "vercel_project": "honda-tech-upgrade", "immutable_preview": None, "persistent_preview": None, "github_actions": {"remote_workflow": None, "latest_run": None, "latest_conclusion": None}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": NO_PREVIEW + " " + NO_REMOTE_WORKFLOW},
    {"order": 9, "app": "MusicAI", "owner_repo": SHARED_REPO, "source": "projects/MusicAI", "kind": "web service/app", "vercel_project": "musicai", "immutable_preview": None, "persistent_preview": None, "github_actions": {"remote_workflow": None, "latest_run": None, "latest_conclusion": None}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": NO_PREVIEW + " " + NO_REMOTE_WORKFLOW},
    {"order": 10, "app": "BurnoutBoyz", "owner_repo": SHARED_REPO, "source": "projects/burnoutBoyz", "kind": "web/universal app + service", "vercel_project": None, "immutable_preview": None, "persistent_preview": None, "github_actions": {"remote_workflow": None, "latest_run": None, "latest_conclusion": None}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": "Local gates were recorded passing, but no Vercel development project/preview or remote GitHub Actions workflow exists; final reviewer card remains blocked."},
    {"order": 11, "app": "Clan War Board service", "owner_repo": "https://github.com/ItMeansBigMountain/clan-war-board-service", "source": "projects/osrs-plugins/services/clan-war-board-service", "kind": "web/API service (RuneLite client is separately verified)", "vercel_project": None, "immutable_preview": None, "persistent_preview": None, "github_actions": {"remote_workflow": None, "latest_run": None, "latest_conclusion": None}, "checks": {"repo": "pass", "tests_build_in_workflow": "fail", "actions_deploy": "fail", "persistent_preview_alias": "fail"}, "blocker": "Standalone GitHub repo exists, but there is no GitHub Actions-backed Vercel development deployment. Azure/production migration is explicitly out of scope. RuneLite plugin verification remains Gradle/RuneLite/Plugin Hub only."},
]


def main() -> None:
    browser = json.loads(BROWSER.read_text())
    by_app: dict[str, list[dict]] = {}
    for check in browser["checks"]:
        by_app.setdefault(check["app"], []).append(check)
    aliases = {"tweetBetweenTheLines": "tweetbetweenthelines", "Journal AI": "journal-ai", "Coding School / Algorithm Academy": "coding-school-platform"}
    for row in CANDIDATES:
        app_name = str(row["app"])
        checks = by_app.get(aliases.get(app_name, app_name), [])
        row["browser_verification"] = {
            "checks": len(checks),
            "passed": sum(bool(c["passed"]) for c in checks),
            "failed": sum(not c["passed"] for c in checks),
            "desktop": next((c for c in checks if c["device"] == "desktop"), None),
            "mobile": next((c for c in checks if c["device"] == "mobile"), None),
        }
        row["review_eligible"] = all(v == "pass" for v in row["checks"].values()) and row["browser_verification"]["failed"] == 0 and row["browser_verification"]["checks"] == 2
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    output = {
        "generated_at": now,
        "policy": "Vercel is development/staging only. No production promotion before Oyama personally tests and approves an Actions-traceable preview. Manual/untraceable deployments are unacceptable.",
        "scope": {"candidate_count": len(CANDIDATES), "review_eligible_count": sum(r["review_eligible"] for r in CANDIDATES), "browser_checked_preview_count": sum(bool(r["immutable_preview"]) for r in CANDIDATES), "excluded": "Static review shells, retired apps, and RuneLite plugin repos. RuneLite clients use Gradle/RuneLite/Plugin Hub verification; their web/API services still require GitHub Actions-backed Vercel development previews."},
        "sources": ["current Kanban task/card census", "projects/_docs/portfolio-sort-2026-08-31.md", "projects/PROJECT_REVIEW_SHEET.md", "Vercel team API", "GitHub API/Actions", "production-candidate-preview-browser-verification.json"],
        "candidates": CANDIDATES,
        "safety": {"production_promotions": 0, "deployments_deleted": 0, "aliases_changed": 0, "secrets_exposed": False},
    }
    OUT_JSON.write_text(json.dumps(output, indent=2) + "\n")
    lines = ["# Production-candidate application review queue", "", f"Generated: {now}", "", "## Gate", "", "- Vercel is development/staging only.", "- Oyama must personally test and approve an Actions-traceable preview before any production work.", "- Manual/untraceable Vercel deployments do not qualify.", "- Current result: **0/11 candidates eligible for Oyama review**; no production promotion was performed.", "", "## Recommended review order", ""]
    for row in CANDIDATES:
        b = row["browser_verification"]
        lines += [f"### {row['order']}. {row['app']}", f"- Repo: {row['owner_repo']} (`{row['source']}`)", f"- Immutable preview: {row['immutable_preview'] or 'missing'}", f"- Persistent preview: {row['persistent_preview'] or 'missing'}", f"- Browser: {b['passed']}/{b['checks']} strict desktop/mobile checks passed" if b["checks"] else "- Browser: not runnable; no acceptable preview URL", f"- GitHub Actions: {row['github_actions']['remote_workflow'] or 'missing on default branch'}; latest: {row['github_actions']['latest_conclusion'] or 'no run'}", f"- Blocker: {row['blocker']}", ""]
    lines += ["## Existing preview browser findings", "", "- tweetBetweenTheLines: desktop/mobile 200, correct identity, no overflow/console/page/network errors (2/2 pass); still fails traceability and persistent-alias gates.", "- Journal AI: mobile passes; desktop has one unexplained 404 console error (1/2 pass); preview has `gitSource=null` and no alias.", "- Coding School: desktop passes; 390×844 mobile overflows horizontally (1/2 pass); preview has `gitSource=null` and no alias.", "", "## Reconciliation notes", "", "- GitHub currently exposes only two remote workflows in HeRmEz: tweetBetweenTheLines Vercel development and EAS preview. The only Vercel-development run failed before build/deploy.", "- Local untracked workflows for Coding School and CombatAtlas are not remote CI evidence. CombatAtlas local deploy workflow also targets production and must not be used under this policy.", "- Existing Vercel aliases and target=production deployments were preserved as historical baselines, not endorsed as production releases.", "- `dist` is a known duplicate/misnamed tweetBetweenTheLines Vercel project and is excluded as a separate product candidate; it was not deleted.", "- Static review shells and retired apps are excluded because HTTP 200 is not product readiness.", "", "## Safety", "", "- Production promotions: 0", "- Deployments/history deleted: 0", "- Aliases changed: 0", "- Secrets printed or stored: no", ""]
    OUT_MD.write_text("\n".join(lines))
    print(json.dumps({"candidates": len(CANDIDATES), "eligible": sum(r["review_eligible"] for r in CANDIDATES), "browser_checks": sum(r["browser_verification"]["checks"] for r in CANDIDATES), "json": str(OUT_JSON), "markdown": str(OUT_MD)}))


if __name__ == "__main__":
    main()
