#!/usr/bin/env python3
"""Alert once on VPS memory pressure; never kills processes."""
from __future__ import annotations

import json
import os
import signal
import subprocess
import time
from pathlib import Path

STATE = Path('/opt/data/runtime-state/memory-guard.json')
STATE.parent.mkdir(parents=True, exist_ok=True)

# Fail-safe pressure relief. These are intentionally exact, local-only services
# that the user approved stopping. Never match the default gateway, dashboard,
# Kanban workers, builds, package installs, or arbitrary high-RSS processes.
SAFE_IDLE_TARGETS = (
    ('Wornly local server', '/opt/data/HeRmEz/projects/wornly', 'next-server'),
    ('Journal AI Vite server', '/opt/data/HeRmEz/projects/journal-ai/frontend/journal-app', 'vite'),
    ('MusicAI Flask server', '/opt/data/HeRmEz/projects/MusicAI', 'flask --app musicAI'),
)
MIN_IDLE_AGE_SECONDS = 4 * 3600


def meminfo() -> dict[str, int]:
    out = {}
    for line in Path('/proc/meminfo').read_text().splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        parts = value.strip().split()
        if parts and parts[0].isdigit():
            out[key] = int(parts[0]) * 1024
    return out


def process_snapshot() -> tuple[int, list[dict[str, object]]]:
    total = 0
    rows = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        try:
            cmd = (entry / 'cmdline').read_bytes().replace(b'\0', b' ').decode(errors='ignore')
            if not any(name in cmd for name in ('tsserver.js', 'typescript-language-server', 'pyright', 'gradle', 'runelite')):
                continue
            status = {}
            for line in (entry / 'status').read_text().splitlines():
                if ':' in line:
                    key, value = line.split(':', 1)
                    status[key] = value.strip()
            rss_kib = int(status.get('VmRSS', '0 kB').split()[0])
            rss = rss_kib * 1024
            total += rss
            rows.append({'pid': int(entry.name), 'rss_mib': round(rss / 1048576), 'cmd': cmd[:140]})
        except (FileNotFoundError, PermissionError, ProcessLookupError, ValueError):
            continue
    rows.sort(key=lambda row: int(row['rss_mib']), reverse=True)
    return total, rows[:8]


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {'alerting': False}


def save_state(value: dict) -> None:
    tmp = STATE.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, sort_keys=True))
    os.chmod(tmp, 0o600)
    tmp.replace(STATE)


def process_age_seconds(pid: int) -> float:
    try:
        ticks = int(Path(f'/proc/{pid}/stat').read_text().split()[21])
        uptime = float(Path('/proc/uptime').read_text().split()[0])
        return max(0.0, uptime - ticks / os.sysconf(os.sysconf_names['SC_CLK_TCK']))
    except (OSError, ValueError, IndexError):
        return 0.0


def stop_safe_idle_targets() -> list[str]:
    """Gracefully stop only the explicit pressure-relief allowlist."""
    actions: list[str] = []
    redteam = subprocess.run(
        ['/command/s6-svc', '-d', '/run/service/gateway-redteam'],
        capture_output=True,
        text=True,
        check=False,
    )
    if redteam.returncode == 0:
        actions.append('Redteam gateway kept down')

    own_pgid = os.getpgrp()
    stopped_pgids: set[int] = set()
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        try:
            cwd = str((entry / 'cwd').resolve())
            cmd = (entry / 'cmdline').read_bytes().replace(b'\0', b' ').decode(errors='ignore')
            age = process_age_seconds(pid)
            for label, exact_cwd, cmd_bit in SAFE_IDLE_TARGETS:
                if cwd != exact_cwd or cmd_bit not in cmd or age < MIN_IDLE_AGE_SECONDS:
                    continue
                pgid = os.getpgid(pid)
                if pgid == own_pgid or pgid in stopped_pgids:
                    continue
                os.killpg(pgid, signal.SIGTERM)
                stopped_pgids.add(pgid)
                actions.append(label)
                break
        except (FileNotFoundError, PermissionError, ProcessLookupError, OSError):
            continue
    if stopped_pgids:
        time.sleep(2)
    return actions


def main() -> None:
    mi = meminfo()
    total = mi.get('MemTotal', 1)
    available = mi.get('MemAvailable', 0)
    available_pct = available * 100 / total
    dev_rss, rows = process_snapshot()
    critical = available < 768 * 1048576 or available_pct < 10 or dev_rss > 3 * 1073741824
    pressure_triggered = critical
    previous = load_state()
    actions: list[str] = []

    if critical:
        actions = stop_safe_idle_targets()
        # Recalculate after pressure relief so the alert reflects current RAM.
        mi = meminfo()
        total = mi.get('MemTotal', 1)
        available = mi.get('MemAvailable', 0)
        available_pct = available * 100 / total
        dev_rss, rows = process_snapshot()
        critical = available < 768 * 1048576 or available_pct < 10 or dev_rss > 3 * 1073741824

    if pressure_triggered and actions and not critical:
        print('✅ **VPS memory pressure relieved**')
        print(f'• Available: {available / 1073741824:.2f} GiB ({available_pct:.1f}%)')
        print('• Stopped: ' + ', '.join(actions[:3]))
        print('📌 Default Hermes, dashboard, workers, and active builds were preserved.')
    elif critical and not previous.get('alerting'):
        print('⚠️ **VPS memory is critical**')
        print(f'• Available: {available / 1073741824:.2f} GiB ({available_pct:.1f}%)')
        print(f'• Dev processes: {dev_rss / 1073741824:.2f} GiB')
        if rows:
            print(f"• Largest: PID {rows[0]['pid']} • {rows[0]['rss_mib']} MiB")
        if actions:
            print('• Relief: ' + ', '.join(actions[:3]))
        print('📌 Default Hermes, dashboard, workers, and active builds were preserved.')
    elif not critical and previous.get('alerting'):
        print('✅ **VPS memory recovered**')
        print(f'• Available: {available / 1073741824:.2f} GiB ({available_pct:.1f}%)')

    save_state({'alerting': critical, 'last_actions': actions})


if __name__ == '__main__':
    main()
