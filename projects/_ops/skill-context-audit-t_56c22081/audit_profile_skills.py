#!/usr/bin/env /opt/hermes/.venv/bin/python
"""Reproducible profile skill-catalog audit and least-privilege config writer."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path("/opt/data/HeRmEz")
OUT = ROOT / "projects/_ops/skill-context-audit-t_56c22081"
PLUGIN = ROOT / "projects/_trials/hermes-enhancement-tools-t_216c5923/repos/agent-skills/plugins/skill-retrieval"
PROFILES = ["default", "software-developer", "social-growth", "trading-specialist", "business-operator", "personal", "fitness", "redteam", "researcher"]
PROFILE_HOME = {p: (Path("/opt/data") if p == "default" else Path("/opt/data/profiles") / p) for p in PROFILES}

# Role-derived capabilities from AGENT_TEAM.md. Explicit names are retained even
# when usage is zero; usage is supporting evidence, never the sole criterion.
KEEP = {
    "default": {
        "hermes-agent", "hermes-agent-operations", "kanban-orchestrator", "kanban-worker",
        "self-review-gates", "session-librarian", "weekly-review-planning", "professional-work",
        "grounded-citations", "research-intelligence-sources", "computer-use", "native-mcp",
        "workspace-productivity-integrations", "document-to-action-items", "meeting-action-items",
        "email-discussion-briefing", "google-workspace", "github", "github-repo-management",
        "project-portfolio-lifecycle", "software-project-delivery", "webhook-subscriptions",
    },
    "software-developer": {
        "hermes-agent", "hermes-agent-operations", "kanban-worker", "self-review-gates",
        "computer-use", "native-mcp", "blocked-page-recovery", "agent-reach-integration",
        "secret-audit-and-precommit", "rtk-output-filter", "runelite-plugin-development",
        "minecraft-modpack-server", "trap-chat", "pdf", "xlsx", "docx", "linear",
        "document-production-workflows", "visual-artifact-design", "google-workspace",
        "youtube-transcript-ingestion", "youtube-automation-with-tts", "youtube-quota-queue-management",
    },
    "social-growth": {
        "hermes-agent", "hermes-agent-operations", "kanban-worker", "self-review-gates",
        "computer-use", "blocked-page-recovery", "grounded-citations", "research-intelligence-sources",
        "competitor-news-monitor", "google-workspace", "pdf", "docx", "xlsx",
        "document-production-workflows", "workspace-productivity-integrations",
        "creator-business-operations", "affiliate-business-operations", "music-and-audio-workflows",
    },
    "trading-specialist": {
        "hermes-agent", "hermes-agent-operations", "kanban-worker", "self-review-gates",
        "computer-use", "blocked-page-recovery", "grounded-citations", "research-intelligence-sources",
        "robinhood-trading-operator", "trading-operations-reporting", "competitor-news-monitor",
        "pdf", "xlsx", "document-to-action-items", "google-workspace", "browser-oauth-automation",
    },
    "business-operator": {
        "hermes-agent", "hermes-agent-operations", "kanban-worker", "self-review-gates",
        "computer-use", "blocked-page-recovery", "grounded-citations", "research-intelligence-sources",
        "competitor-news-monitor", "affiliate-business-operations", "creator-business-operations",
        "professional-work", "google-workspace", "pdf", "docx", "xlsx", "linear",
        "document-production-workflows", "workspace-productivity-integrations", "meeting-action-items",
        "email-discussion-briefing", "product-price-monitor", "browser-assisted-personal-applications",
    },
    "personal": {
        "hermes-agent", "hermes-agent-operations", "kanban-worker", "self-review-gates",
        "computer-use", "blocked-page-recovery", "grounded-citations", "personal-life-management",
        "professional-work", "weekly-review-planning", "google-workspace", "pdf", "docx", "xlsx",
        "document-production-workflows", "workspace-productivity-integrations", "meeting-action-items",
        "email-discussion-briefing", "email-inbox-triage", "browser-assisted-personal-applications",
        "product-price-monitor", "session-librarian", "alltrails-fitness-planner", "spotify",
    },
    "fitness": {"hermes-agent", "self-review-gates", "alltrails-fitness-planner"},
    "redteam": {
        "hermes-agent", "hermes-agent-operations", "kanban-worker", "self-review-gates",
        "computer-use", "blocked-page-recovery", "grounded-citations", "research-intelligence-sources",
        "intelbase", "secret-audit-and-precommit", "authorized-mantis-review", "security-research-repository-triage",
        "native-mcp", "github", "github-repo-management", "codebase-inspection", "godmode",
    },
    "researcher": {
        "hermes-agent", "hermes-agent-operations", "kanban-worker", "self-review-gates",
        "computer-use", "blocked-page-recovery", "grounded-citations", "research-intelligence-sources",
        "competitor-news-monitor", "intelbase", "pdf", "docx", "xlsx", "document-to-action-items",
        "google-workspace", "youtube-transcript-ingestion", "browser-oauth-automation", "product-price-monitor",
    },
}
KEEP_CATEGORIES = {
    "software-developer": {"software-development", "devops", "github", "mcp", "mlops", "mlops/inference", "mlops/research", "mlops/training", "integrations"},
    "social-growth": {"social-media", "creative", "media"},
}


def load_usage(home: Path) -> dict:
    path = home / "skills/.usage.json"
    try:
        raw = json.loads(path.read_text())
        return raw.get("skills", raw) if isinstance(raw, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def plugin_index(home: Path) -> list[dict]:
    code = f'''import json,sys\nfrom hermes_constants import set_hermes_home_override\nset_hermes_home_override({str(home)!r})\nsys.path.insert(0,{str(PLUGIN / "scripts")!r})\nimport bm25_retriever as b\nitems=b.load_active_skills()\nidx=b.BM25Index(); idx.build([x["skill_id"] for x in items],[x["text"] for x in items])\nprint(json.dumps(items))'''
    cp = subprocess.run(["/opt/hermes/.venv/bin/python", "-c", code], text=True, capture_output=True, check=True)
    return json.loads(cp.stdout)


def prompt_size(profile: str) -> dict:
    if profile == "fitness":
        return {"skills_index": {"chars": 0, "bytes": 0}, "skills_breakdown": []}
    cp = subprocess.run(["hermes", "--profile", profile, "prompt-size", "--platform", "discord", "--json"], text=True, capture_output=True, check=True)
    return json.loads(cp.stdout)


def snapshot(label: str) -> dict:
    result = {"schema_version": 1, "label": label, "generated_at": datetime.now(timezone.utc).isoformat(), "token_method": "UTF-8 description bytes divided by 4, ceiling; deterministic estimate", "profiles": {}}
    for profile in PROFILES:
        home = PROFILE_HOME[profile]
        items = plugin_index(home) if (home / "skills").exists() else []
        desc_block = "\n".join(f'{x["name"]}: {x["description"]}' for x in items)
        size = prompt_size(profile)
        usage = load_usage(home)
        result["profiles"][profile] = {
            "home": str(home), "config": str(home / "config.yaml"), "indexed_skills": len(items),
            "description_chars": len(desc_block), "description_bytes": len(desc_block.encode()),
            "description_token_estimate": (len(desc_block.encode()) + 3) // 4,
            "runtime_index_chars": size["skills_index"]["chars"], "runtime_index_bytes": size["skills_index"]["bytes"],
            "skills": [{"name": x["name"], "skill_id": x["skill_id"], "description": x["description"], "usage": usage.get(x["name"], {})} for x in items],
        }
    path = OUT / f"{label}.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    return result


def apply() -> None:
    from hermes_constants import reset_hermes_home_override, set_hermes_home_override
    from hermes_cli.config import load_config
    from hermes_cli.skills_config import save_disabled_skills

    before = snapshot("before")
    changes = {}
    for profile in PROFILES:
        home = PROFILE_HOME[profile]
        items = before["profiles"][profile]["skills"]
        keep = set(KEEP[profile])
        for item in items:
            category = item["skill_id"].rsplit("/", 1)[0] if "/" in item["skill_id"] else "uncategorized"
            if category in KEEP_CATEGORIES.get(profile, set()):
                keep.add(item["name"])
        installed = {x["name"] for x in items}
        disabled = installed - keep
        token = set_hermes_home_override(str(home))
        try:
            config = load_config() or {}
            save_disabled_skills(config, disabled)
        finally:
            reset_hermes_home_override(token)
        changes[profile] = {"kept": sorted(installed - disabled), "disabled": sorted(disabled), "missing_requested_keeps": sorted(keep - installed)}
    (OUT / "changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    snapshot("after")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["snapshot", "apply"])
    parser.add_argument("--label", default="snapshot")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.action == "apply": apply()
    else: snapshot(args.label)

if __name__ == "__main__":
    main()
