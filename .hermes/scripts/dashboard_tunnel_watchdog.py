#!/usr/bin/env python3
"""Keep the authenticated Kanban tunnel supervised and announce URL changes."""
from __future__ import annotations

import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path('/opt/data/dashboard-proxy')
STATE = Path('/opt/data/runtime-state/dashboard-tunnel-watchdog.json')
SERVICES = ('dashboard-proxy', 'dashboard-tunnel')


def service_pid(name: str) -> int | None:
    try:
        raw = (Path('/run/service') / name / 'supervise' / 'pid').read_text().strip()
        return int(raw) if raw.isdigit() else None
    except Exception:
        return None


def ensure_services() -> None:
    runtime = Path('/run/service')
    runtime.mkdir(parents=True, exist_ok=True)
    changed = False
    for name in SERVICES:
        service = runtime / name
        service.mkdir(parents=True, exist_ok=True)
        run_link = service / 'run'
        target = BASE / 's6' / name / 'run'
        if run_link.is_symlink() and run_link.resolve() == target.resolve():
            continue
        if run_link.exists() or run_link.is_symlink():
            run_link.unlink()
        run_link.symlink_to(target)
        changed = True
    if changed or any(service_pid(name) is None for name in SERVICES):
        subprocess.run(['/command/s6-svscanctl', '-a', '/run/service'], check=False)
        time.sleep(3)


def latest_url() -> str | None:
    try:
        text = (BASE / 'tunnel.log').read_text(errors='ignore')
    except FileNotFoundError:
        return None
    urls = re.findall(r'https://[a-z0-9-]+\.trycloudflare\.com', text)
    return urls[-1] if urls else None


def status(url: str) -> int | None:
    try:
        with urllib.request.urlopen(url + '/kanban', timeout=15) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception:
        return None


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {}


def save_state(data: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, sort_keys=True))
    os.chmod(tmp, 0o600)
    tmp.replace(STATE)


def main() -> None:
    ensure_services()
    for _ in range(6):
        url = latest_url()
        if url and status(url) == 401:
            break
        time.sleep(3)
    else:
        url = latest_url()

    old = load_state()
    healthy = bool(url and status(url) == 401)
    changed = bool(healthy and url != old.get('url'))
    recovered = bool(healthy and old.get('healthy') is False)
    failed = bool(not healthy and old.get('healthy') is not False)

    if changed:
        subprocess.run([
            '/opt/data/.local/bin/hermes', 'config', 'set',
            'dashboard.public_url', url,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        print('✅ **Kanban dashboard link updated**')
        print('• ' + url + '/kanban')
    elif recovered:
        print('✅ **Kanban dashboard recovered**')
        print('• ' + url + '/kanban')
    elif failed:
        print('⚠️ **Kanban dashboard unavailable**')
        print('🔄 s6 is retrying automatically.')

    save_state({'url': url, 'healthy': healthy})


if __name__ == '__main__':
    main()
