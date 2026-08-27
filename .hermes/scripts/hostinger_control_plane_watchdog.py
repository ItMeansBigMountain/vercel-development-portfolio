#!/usr/bin/env python3
"""Stateful, read-only Hostinger control-plane watchdog for this Hermes VPS.

Silent when healthy. It never restarts/stops/deletes/redeploys anything.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://developers.hostinger.com/api/vps/v1"
VM_ID = 1646785
PROJECT = "hermes-agent-xbit"
STATE = Path("/opt/data/runtime-state/hostinger-control-plane-watchdog.json")
REPEAT_SECONDS = 6 * 3600
CPU_WARN = 95.0
MEMORY_WARN = 85.0
BACKUP_MAX_AGE_HOURS = 192  # eight days; Hostinger weekly backups get one-day grace.


def token() -> str:
    return os.getenv("HOSTINGER_API_TOKEN") or os.getenv("hostinger_api_key") or ""


def get(path: str):
    request = urllib.request.Request(
        API + path,
        headers={
            "Authorization": f"Bearer {token()}",
            "Accept": "application/json",
            "User-Agent": "Hermes-Hostinger-Watchdog/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def save_state(value: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=STATE.name + ".", suffix=".tmp", dir=STATE.parent)
    tmp = Path(name)
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(value, handle, sort_keys=True, indent=2)
            handle.write("\n")
        os.chmod(tmp, 0o600)
        tmp.replace(STATE)
    finally:
        tmp.unlink(missing_ok=True)


def parse_time(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> int:
    now = int(time.time())
    old = load_state()
    reasons: list[str] = []
    details: dict[str, object] = {"checked_at": now, "mode": "read_only"}

    if not token():
        reasons.append("Hostinger API token is missing from the container environment")
    else:
        try:
            vms = get("/virtual-machines")
            vm = next((v for v in vms if int(v.get("id", -1)) == VM_ID), None)
            vm_state = (vm or {}).get("state", "missing")
            details["vm_state"] = vm_state
            if vm_state != "running":
                reasons.append(f"Hostinger reports VPS state `{vm_state}`")

            projects = get(f"/virtual-machines/{VM_ID}/docker")
            project = next((p for p in projects if p.get("name") == PROJECT), None)
            project_state = (project or {}).get("state", "missing")
            details["project_state"] = project_state
            if project_state != "running":
                reasons.append(f"Docker project `{PROJECT}` is `{project_state}`")

            containers = get(f"/virtual-machines/{VM_ID}/docker/{PROJECT}/containers") if project else []
            running = [c for c in containers if c.get("state") == "running"]
            details["container_count"] = len(containers)
            details["running_containers"] = len(running)
            if not running:
                reasons.append("Hostinger reports no running Hermes container")
            if len(running) != len(containers):
                reasons.append(f"{len(containers) - len(running)} Hermes project container(s) are not running")
            unhealthy = [c for c in running if str(c.get("health") or "").lower() == "unhealthy"]
            if unhealthy:
                reasons.append(f"{len(unhealthy)} Hermes project container(s) report unhealthy")
            if running:
                cpu = max(float((c.get("stats") or {}).get("cpu_percentage") or 0) for c in running)
                memory = max(float((c.get("stats") or {}).get("memory_percentage") or 0) for c in running)
                details.update({"cpu_percentage": cpu, "memory_percentage": memory})
                high_now = cpu >= CPU_WARN or memory >= MEMORY_WARN
                high_count = int(old.get("high_resource_count", 0)) + 1 if high_now else 0
                details["high_resource_count"] = high_count
                if high_count >= 2:
                    if cpu >= CPU_WARN:
                        reasons.append(f"container CPU remained high at {cpu:.1f}%")
                    if memory >= MEMORY_WARN:
                        reasons.append(f"container memory remained high at {memory:.1f}%")

            backups_payload = get(f"/virtual-machines/{VM_ID}/backups")
            backups = backups_payload.get("data", []) if isinstance(backups_payload, dict) else backups_payload
            details["backup_count"] = len(backups)
            if not backups:
                reasons.append("Hostinger reports no VPS backups")
            else:
                newest = max(parse_time(b["created_at"]) for b in backups if b.get("created_at"))
                age_hours = (dt.datetime.now(dt.timezone.utc) - newest).total_seconds() / 3600
                details["newest_backup_age_hours"] = round(age_hours, 1)
                if age_hours > BACKUP_MAX_AGE_HOURS:
                    reasons.append(f"newest Hostinger VPS backup is {age_hours / 24:.1f} days old")
        except urllib.error.HTTPError as exc:
            reasons.append(f"Hostinger API returned HTTP {exc.code}")
            details["api_http_status"] = exc.code
        except Exception as exc:
            reasons.append(f"Hostinger monitoring failed: {type(exc).__name__}")
            details["api_error_type"] = type(exc).__name__

    # Normalize changing measurements so the six-hour dedupe remains stable.
    signature = "|".join(re.sub(r"\d+(?:\.\d+)?", "#", reason) for reason in reasons)
    last_signature = old.get("signature", "")
    last_alert = int(old.get("last_alert", 0))
    recovered = not reasons and bool(last_signature)
    emit = bool(reasons) and (signature != last_signature or now - last_alert >= REPEAT_SECONDS)
    details.update({
        "signature": signature,
        "last_alert": now if emit else last_alert,
        "healthy": not reasons,
    })
    try:
        save_state(details)
    except Exception as exc:
        print("⚠️ Needs attention")
        print(f"• Hostinger watchdog state write failed: {type(exc).__name__}")
        print("📌 Read-only monitor; no VPS or container action was taken.")
        return 0

    if emit:
        print("⚠️ Needs attention")
        for reason in reasons[:3]:
            print(f"• {reason}")
        print("📌 Read-only monitor; no VPS or container action was taken.")
    elif recovered:
        print("✅ Done")
        print("• Hostinger reports the VPS, Hermes project, container, and backups healthy again.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
