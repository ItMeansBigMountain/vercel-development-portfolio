import importlib.util
import json
import sqlite3
from pathlib import Path


def load_api(tmp_path, monkeypatch):
    home = tmp_path / "home"
    workspace = tmp_path / "workspace"
    monkeypatch.setenv("COMMAND_CENTER_HOME", str(home))
    monkeypatch.setenv("COMMAND_CENTER_WORKSPACE", str(workspace))
    path = Path(__file__).parents[1] / "dashboard/plugin_api.py"
    spec = importlib.util.spec_from_file_location("command_center_api", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, home, workspace


def make_kanban(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(path)
    c.executescript("""
      CREATE TABLE tasks(id TEXT,title TEXT,assignee TEXT,status TEXT,priority INT,last_heartbeat_at INT,created_at INT);
      CREATE TABLE task_attachments(task_id TEXT,filename TEXT,content_type TEXT,size INT,created_at INT);
      INSERT INTO tasks VALUES('t_12345678','Ship it','dev','running',4,100,100);
      INSERT INTO task_attachments VALUES('t_12345678','report.pdf','application/pdf',42,100);
    """)
    c.commit(); c.close()


def test_overview_is_read_only_summary(tmp_path, monkeypatch):
    api, home, workspace = load_api(tmp_path, monkeypatch)
    (home / "cron").mkdir(parents=True)
    (home / "cron/jobs.json").write_text(json.dumps({"jobs":[{"id":"j1","name":"Health","enabled":True,"last_status":"ok","failure_streak":0}]}))
    (workspace / "projects/_ops").mkdir(parents=True)
    (workspace / "projects/_ops/active-app-deployment-inventory.json").write_text(json.dumps({"generated_at":"2026-01-01T00:00:00+00:00","apps":[{"app":"app","classification":"healthy","canonical_production_alias":"https://example.com","secret":"no"}]}))
    (home / "config.yaml").write_text("model:\n  provider: openai-codex\n  default: gpt-test\nfallback_providers:\n  - provider: nous\n    model: fallback\napi_key: forbidden\n")
    make_kanban(home / "kanban.db")
    result = api.collect_overview()
    encoded = json.dumps(result)
    assert result["mode"] == "read-only"
    assert result["sections"]["kanban"]["counts"] == {"running": 1}
    assert result["sections"]["cron"]["counts"] == {"ok": 1}
    assert result["sections"]["deployments"]["items"][0]["url"] == "https://example.com"
    assert result["sections"]["models"]["quota"]["status"] == "unknown"
    assert "forbidden" not in encoded and "secret" not in encoded and "prompt" not in encoded


def test_missing_sources_are_honest_unknowns(tmp_path, monkeypatch):
    api, _, _ = load_api(tmp_path, monkeypatch)
    result = api.collect_overview()
    assert result["sections"]["kanban"]["status"] == "unknown"
    assert result["sections"]["cron"]["status"] == "unknown"
    assert result["sections"]["deployments"]["status"] == "unknown"
    assert result["sections"]["models"]["quota"]["status"] == "unknown"


def test_router_has_get_only_overview(tmp_path, monkeypatch):
    api, _, _ = load_api(tmp_path, monkeypatch)
    methods = [(r.path, r.methods) for r in api.router.routes]
    assert methods == [("/overview", {"GET"})]
