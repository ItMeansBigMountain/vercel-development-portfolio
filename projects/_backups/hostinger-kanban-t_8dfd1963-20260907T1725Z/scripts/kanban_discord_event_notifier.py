#!/usr/bin/env python3
"""Post every new default-board Kanban event to #kanban-work."""
from __future__ import annotations
import json, os, sqlite3, sys, time, urllib.error, urllib.request
from pathlib import Path

def load_env_value(name: str, env_path: Path = Path("/opt/data/.env")) -> str:
    if os.getenv(name): return os.environ[name]
    try:
        for raw in env_path.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            k,v = line.split("=",1)
            if k.strip()==name: return v.strip().strip("'\"")
    except OSError: pass
    return ""

DB = Path(os.getenv("HERMES_KANBAN_DB","/opt/data/kanban.db"))
STATE = Path(os.getenv("KANBAN_NOTIFY_STATE","/opt/data/cron/state/kanban_discord_event_notifier.json"))
CHANNEL_ID = os.getenv("KANBAN_NOTIFY_CHANNEL_ID","1541610170919030905")
TOKEN = load_env_value("DISCORD_BOT_TOKEN")
API = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
BOARD_URL = "https://kanban.itmeansbigmountains.com"  # adjust if needed

def concise(value: object, limit: int = 120) -> str:
    """Collapse notification detail into one glanceable line."""
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def describe(kind: str, title: str, payload_raw: str | None, last_comment: str | None = None) -> str:
    try: payload = json.loads(payload_raw) if payload_raw else {}
    except: payload = {}
    emoji_map = {"created":"🆕","promoted":"➡️","claimed":"▶️","spawned":"🚀","heartbeat":"📊","completed":"✅","blocked":"⛔","dependency_wait":"⛓️","unblocked":"🔓","archived":"📦","assigned":"👤","edited":"✏️","reprioritized":"🔼","status":"🔄","commented":"💬","comment":"💬","linked":"🔗","unlinked":"⛓️","reclaimed":"♻️","crashed":"💥","timed_out":"⏰","stale":"🕰️","reconciled":"🔧","spawn_failed":"💣","protocol_violation":"⚠️","gave_up":"🛑","review_requested":"👀","changes_requested":"↩️"}
    detail_map = {
        "created": "created",
        "promoted": "moved to Ready",
        "claimed": "work started",
        "spawned": "worker launched",
        "heartbeat": f"progress: {payload.get('note','')}" if payload.get('note') else "progress update",
        "completed": f"completed: {payload.get('summary','')}" if payload.get('summary') else "completed",
        "blocked": f"blocked: {payload.get('reason','')}" if payload.get('reason') else "blocked",
        "dependency_wait": "waiting on dependency",
        "unblocked": "unblocked",
        "archived": "archived",
        "assigned": f"assigned to {payload.get('assignee','unassigned')}",
        "edited": "details edited",
        "reprioritized": f"priority → {payload.get('priority','')}",
        "status": f"status → {payload.get('status','')}",
        "commented": f"comment: {payload.get('body', last_comment or '')}" if (payload.get('body') or last_comment) else "comment added",
        "comment": f"comment: {payload.get('body', last_comment or '')}" if (payload.get('body') or last_comment) else "comment added",
        "linked": "dependency linked",
        "unlinked": "dependency removed",
        "reclaimed": "claim reclaimed → Ready",
        "crashed": "worker crashed; will retry",
        "timed_out": "worker timed out; will retry",
        "stale": "stale worker reclaimed; will retry",
        "reconciled": "orphaned task reconciled",
        "spawn_failed": "worker launch failed; will retry",
        "protocol_violation": "worker exited without close; will retry",
        "gave_up": "retry limit reached; blocked",
        "review_requested": "moved to Review",
        "changes_requested": f"changes requested: {payload.get('reason','')}" if payload.get('reason') else "changes requested",
    }
    emoji = emoji_map.get(kind,"📋")
    detail = concise(detail_map.get(kind, kind.replace("_"," ")))
    return f"{emoji}  **{concise(title, 80)}**\n*{detail}*\n\n"

def send(content: str) -> None:
    if not TOKEN: raise RuntimeError("DISCORD_BOT_TOKEN is not configured")
    req = urllib.request.Request(API, data=json.dumps({"content":content,"allowed_mentions":{"parse":[]}}).encode(), headers={"Authorization":f"Bot {TOKEN}","Content-Type":"application/json","User-Agent":"Hermes-Kanban-Notifier/1.0"}, method="POST")
    with urllib.request.urlopen(req, timeout=20) as r:
        if r.status not in (200,201): raise RuntimeError(f"Discord returned HTTP {r.status}")
    time.sleep(0.2)

def main() -> int:
    if "--self-test" in sys.argv:
        assert describe("completed","Example",'{"summary":"tests passed"}')=="✅  **Example**\n*completed: tests passed*\n\n"
        assert describe("heartbeat","Example",'{"note":"deployed to Vercel"}')=="📊  **Example**\n*progress: deployed to Vercel*\n\n"
        assert describe("blocked","Example",'{"reason":"missing API key"}')=="⛔  **Example**\n*blocked: missing API key*\n\n"
        assert "\n" not in concise("line one\nline two")
        assert len(concise("x" * 200)) == 120
        print("self-test ok"); return 0
    if not DB.exists(): raise RuntimeError(f"Kanban DB not found: {DB}")
    STATE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    max_id = int(conn.execute("SELECT COALESCE(MAX(id),0) FROM task_events").fetchone()[0])
    if not STATE.exists():
        STATE.write_text(json.dumps({"last_event_id":max_id,"notify_count":0})+"\n"); return 0
    try:
        state = json.loads(STATE.read_text())
        last_id = int(state.get("last_event_id",0))
        notify_count = int(state.get("notify_count",0))
    except: last_id, notify_count = 0, 0
    rows = conn.execute("SELECT e.id,e.kind,e.payload,t.title,(SELECT tc.body FROM task_comments tc WHERE tc.task_id=t.id ORDER BY tc.id DESC LIMIT 1) FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE e.id>? ORDER BY e.id",(last_id,)).fetchall()
    conn.close()
    for event_id,kind,payload,title,last_comment in rows:
        send(describe(str(kind),str(title),payload,last_comment))
        notify_count += 1
        # Dashboard URL is pinned in the channel — no need to re-post periodically
        STATE.write_text(json.dumps({"last_event_id":int(event_id),"notify_count":notify_count})+"\n")
    return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as exc: print(f"Kanban notifier error: {exc}",file=sys.stderr); raise SystemExit(1)