#!/usr/bin/env python3
"""Silent, stateful VPS resource-pressure watchdog. Never terminates processes."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import time

STATE = Path('/opt/data/tmp/resource-health-watchdog-state.json')
MIN_AVAILABLE = 1024 * 1024 * 1024
DISK_WARN_PERCENT = 82
PSI_MEMORY_FULL_10 = 2.0
REPEAT_SECONDS = 6 * 3600


def meminfo() -> dict[str, int]:
    out = {}
    for line in Path('/proc/meminfo').read_text().splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        fields = value.split()
        if fields and fields[0].isdigit():
            out[key] = int(fields[0]) * (1024 if len(fields) > 1 and fields[1] == 'kB' else 1)
    return out


def pressure_full_avg10() -> float:
    try:
        for line in Path('/proc/pressure/memory').read_text().splitlines():
            if line.startswith('full '):
                return float(dict(item.split('=') for item in line.split()[1:])['avg10'])
    except (OSError, ValueError, KeyError):
        pass
    return 0.0


def oom_kills() -> int:
    try:
        for line in Path('/sys/fs/cgroup/memory.events').read_text().splitlines():
            key, value = line.split()
            if key == 'oom_kill':
                return int(value)
    except (OSError, ValueError):
        pass
    return 0


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def main() -> int:
    now = int(time.time())
    mem = meminfo()
    available = mem.get('MemAvailable', 0)
    total = mem.get('MemTotal', 0)
    psi = pressure_full_avg10()
    disk = shutil.disk_usage('/opt/data')
    disk_percent = round(disk.used * 100 / disk.total)
    kills = oom_kills()
    old = load_state()
    reasons = []
    if available < MIN_AVAILABLE:
        reasons.append(f'available RAM is {available / 1073741824:.2f} GiB (threshold 1.00 GiB)')
    if psi >= PSI_MEMORY_FULL_10:
        reasons.append(f'memory full PSI avg10 is {psi:.2f}% (threshold 2.00%)')
    if disk_percent >= DISK_WARN_PERCENT:
        reasons.append(f'disk usage is {disk_percent}% (threshold {DISK_WARN_PERCENT}%)')
    if kills > int(old.get('oom_kills', kills)):
        reasons.append(f'cgroup OOM-kill counter increased from {old.get("oom_kills")} to {kills}')
    signature = '|'.join(reasons)
    last_signature = old.get('signature', '')
    last_alert = int(old.get('last_alert', 0))
    emit = bool(reasons) and (signature != last_signature or now - last_alert >= REPEAT_SECONDS)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({
        'checked_at': now, 'last_alert': now if emit else last_alert,
        'signature': signature, 'oom_kills': kills,
        'available_bytes': available, 'total_bytes': total,
        'memory_full_psi_avg10': psi, 'disk_percent': disk_percent,
        'action': 'alert_only',
    }, indent=2) + '\n')
    if emit:
        print('⚠️ **VPS resources need attention**')
        for reason in reasons[:3]:
            print(f'• {reason}')
        print('📌 No processes stopped. Review active work before cleanup.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
