"""Read-only Hermes command-center dashboard API.

All endpoints are GET-only and expose summaries from canonical local sources.
Raw prompts, errors, credentials, task bodies, filesystem paths, and user data are
intentionally excluded.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any

from fastapi import APIRouter

router = APIRouter()
UTC = dt.timezone.utc
HOME = Path(os.environ.get("COMMAND_CENTER_HOME", "/opt/data"))
WORKSPACE = Path(os.environ.get("COMMAND_CENTER_WORKSPACE", "/opt/data/HeRmEz"))


def _now() -> dt.datetime:
    return dt.datetime.now(UTC)


def _iso_mtime(path: Path) -> str | None:
    try:
        return dt.datetime.fromtimestamp(path.stat().st_mtime, UTC).isoformat()
    except OSError:
        return None


def _age_state(path: Path, stale_hours: int) -> tuple[str, str | None]:
    stamp = _iso_mtime(path)
    if not stamp:
        return "unknown", None
    age = _now() - dt.datetime.fromisoformat(stamp)
    return ("stale" if age > dt.timedelta(hours=stale_hours) else "fresh"), stamp


def _read_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, "source unavailable"
    except (OSError, json.JSONDecodeError):
        return None, "source unreadable"


def _source(name: str, path: Path, status: str, updated_at: str | None, error: str | None = None) -> dict:
    return {"name": name, "status": status, "updated_at": updated_at, "error": error}


def collect_deployments() -> dict:
    path = WORKSPACE / "projects/_ops/active-app-deployment-inventory.json"
    raw, error = _read_json(path)
    state, stamp = _age_state(path, 24)
    if error or not isinstance(raw, dict):
        return {"status": "unknown", "items": [], "counts": {}, "source": _source("deployment inventory", path, "unknown", stamp, error)}
    items = []
    for app in raw.get("apps", []):
        if not isinstance(app, dict):
            continue
        url = app.get("canonical_production_alias")
        items.append({"name": app.get("app") or "unknown", "status": app.get("classification") or "unknown", "url": url if isinstance(url, str) and url.startswith("https://") else None})
    counts = Counter(x["status"] for x in items)
    return {"status": state, "items": items, "counts": dict(counts), "source": _source("deployment inventory", path, state, raw.get("generated_at") or stamp)}


def collect_cron() -> dict:
    path = HOME / "cron/jobs.json"
    raw, error = _read_json(path)
    state, stamp = _age_state(path, 1)
    jobs = raw.get("jobs", []) if isinstance(raw, dict) else []
    if error or not isinstance(jobs, list):
        return {"status": "unknown", "items": [], "counts": {}, "source": _source("cron registry", path, "unknown", stamp, error)}
    items, counts = [], Counter()
    for job in jobs:
        if not isinstance(job, dict):
            continue
        status = "paused" if not job.get("enabled") else ("failing" if job.get("failure_streak", 0) else (job.get("last_status") or "never-run"))
        counts[status] += 1
        items.append({"id": job.get("id"), "name": job.get("name") or "unnamed", "status": status, "schedule": job.get("schedule_display"), "last_run_at": job.get("last_run_at"), "next_run_at": job.get("next_run_at"), "failure_streak": int(job.get("failure_streak") or 0)})
    return {"status": state, "items": items, "counts": dict(counts), "source": _source("cron registry", path, state, stamp)}


def collect_kanban() -> dict:
    path = HOME / "kanban.db"
    stamp = _iso_mtime(path)
    try:
        uri = f"file:{path}?mode=ro"
        with sqlite3.connect(uri, uri=True, timeout=2) as conn:
            rows = conn.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status").fetchall()
            active = conn.execute("SELECT id,title,assignee,status,priority,last_heartbeat_at FROM tasks WHERE status IN ('running','blocked','review','ready') ORDER BY priority DESC, created_at DESC LIMIT 30").fetchall()
            artifacts = conn.execute("SELECT a.task_id,a.filename,a.content_type,a.size,a.created_at FROM task_attachments a ORDER BY a.created_at DESC LIMIT 20").fetchall()
    except (OSError, sqlite3.Error):
        return {"status": "unknown", "counts": {}, "active": [], "artifacts": [], "source": _source("canonical Kanban", path, "unknown", stamp, "source unavailable")}
    return {
        "status": "fresh",
        "counts": {str(k): v for k, v in rows},
        "active": [{"id": r[0], "title": r[1], "assignee": r[2] or "unassigned", "status": r[3], "priority": r[4], "last_heartbeat_at": r[5], "url": f"/kanban?task={r[0]}"} for r in active],
        "artifacts": [{"task_id": r[0], "name": r[1], "content_type": r[2] or "unknown", "size": r[3], "created_at": r[4], "url": f"/kanban?task={r[0]}"} for r in artifacts],
        "source": _source("canonical Kanban", path, "fresh", stamp),
    }


def collect_models() -> dict:
    path = HOME / "config.yaml"
    stamp = _iso_mtime(path)
    try:
        import yaml
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        model = raw.get("model") or {}
        fallbacks = raw.get("fallback_providers") or []
        primary = {"provider": model.get("provider") or "unknown", "model": model.get("default") or "unknown"}
        chain = [{"provider": x.get("provider") or "unknown", "model": x.get("model") or "unknown"} for x in fallbacks if isinstance(x, dict)]
        return {"status": "fresh", "primary": primary, "fallbacks": chain, "quota": {"status": "unknown", "message": "Provider quota is not exposed by a canonical local source."}, "source": _source("Hermes model config", path, "fresh", stamp)}
    except Exception:
        return {"status": "unknown", "primary": None, "fallbacks": [], "quota": {"status": "unknown", "message": "Model and quota source unavailable."}, "source": _source("Hermes model config", path, "unknown", stamp, "source unavailable")}


def collect_overview() -> dict:
    deployments, cron, kanban, models = collect_deployments(), collect_cron(), collect_kanban(), collect_models()
    sources = [deployments["source"], cron["source"], kanban["source"], models["source"]]
    return {"generated_at": _now().isoformat(), "mode": "read-only", "conversation_home": {"label": "Discord #general", "channel_id": "1499990220077137943"}, "sections": {"deployments": deployments, "kanban": kanban, "cron": cron, "models": models}, "sources": sources}


@router.get("/overview")
async def overview() -> dict:
    return collect_overview()
