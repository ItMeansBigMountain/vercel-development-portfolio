# Discord channel routing, cron delivery, and profile gateway autostart

Use this when the user is reorganizing a Discord server into topical Hermes lanes or wants profile gateways/cron reports to follow that routing.

## Channel routing pattern

When the user says to route work by Discord channel, first capture the channel semantics, then ask for/verify concrete Discord channel IDs before changing cron delivery.

Current user routing learned from the Discord reorg session:

- `#general` — global commands, orchestration, cron/admin, morning/operator reports.
- `#coding` — development, repositories, debugging, GitHub, deployments, implementation-heavy project work.
- `#personal` — personal life plus gaming/game-dev topics when no separate gaming channel is wanted.
- Business channel `<#1524172425393340516>` — business, monetization, affiliate/shopify/Stripe, Jared kids coding tutoring, and school/career work tied to income.
- `#youtube-automation` — faceless newsletter videos, Viral Radar, Shorts, upload queues/limits, channel-token issues, content calendars.
- `#trading` — Robinhood, market scans, power-hour monitor, portfolio reports, trade-account monitors.

Do not assume a plain channel name is a valid deliver target. Ask the user to paste a channel mention/ID such as `<#123...>` or inspect platform config if available.

## Cron delivery update sequence

1. `cronjob(action="list")` and map each job to a channel by domain.
2. Present the proposed mapping and explicitly confirm before write operations.
3. Update jobs with exact `job_id`; never guess IDs.
4. For watchdog/no-agent jobs, keep empty stdout silent where possible and route only actual failures/noisy summaries.
5. Run one representative job manually after a delivery rewrite if it is safe, or report the next scheduled verification time.

Common mapping:

- Global/admin: backups, email sorting, morning operator report -> `#general` unless user chooses ops-alerts.
- YouTube/content: faceless, Viral Radar, YouTube auth/channel watchdog, social-video metrics -> `#youtube-automation`.
- Trading: Robinhood scans and market monitors -> `#trading`.
- Business/tutoring/affiliate reminders -> business channel.

## Profile gateway autostart after Docker/container reset

Preferred official/s6 path: if the container uses s6 profile services, register each profile gateway and let boot reconciliation restore profile services whose `gateway_state.json` says `running`.

For this user's current container (`/bin/zsh /entrypoint.sh` as PID 1), patch `/entrypoint.sh` directly after the default gateway block so redteam starts as a background process too:

```zsh
if [[ -f /opt/data/config.yaml ]]; then
  if ! pgrep -f "hermes -p redteam gateway run" >/dev/null 2>&1; then
    gosu hermes nohup hermes -p redteam gateway run >>/opt/data/logs/gateway-redteam.log 2>&1 </dev/null &
  fi
fi
```

A reusable idempotent patch helper is saved at `/opt/data/scripts/patch_entrypoint_redteam_autostart.sh`; run it as a user that can write `/entrypoint.sh` after any image/container recreation.

Fallback path for non-s6/root-entrypoint containers when `/entrypoint.sh` cannot be patched: if the default gateway starts from `/entrypoint.sh` but additional profile gateways do not, create a persistent, silent watchdog script under `/opt/data/scripts/` and a `no_agent=true` cron. The script should:

- Check whether the profile gateway process already exists.
- Remove stale profile `gateway.pid`/`gateway.lock` only when no matching process is running.
- Start the profile gateway in the background using the Hermes launcher and profile flag.
- Sleep briefly and verify the process exists.
- Print nothing on success; print structured JSON and exit non-zero only when start fails.

Minimal pattern:

```bash
#!/usr/bin/env bash
set -euo pipefail
LOG=/opt/data/logs/gateway-redteam.log
mkdir -p /opt/data/logs
if pgrep -f 'hermes -p redteam gateway run' >/dev/null 2>&1; then
  exit 0
fi
rm -f /opt/data/profiles/redteam/gateway.pid /opt/data/profiles/redteam/gateway.lock 2>/dev/null || true
nohup /opt/data/.local/bin/hermes -p redteam gateway run >>"$LOG" 2>&1 </dev/null &
sleep 5
if pgrep -f 'hermes -p redteam gateway run' >/dev/null 2>&1; then
  exit 0
fi
echo '{"status":"redteam_gateway_start_failed","log":"/opt/data/logs/gateway-redteam.log"}'
exit 1
```

Then create a script-only cron:

```text
name: Ensure redteam profile gateway is running
schedule: every 1m
script: ensure_redteam_gateway.sh
no_agent: true
```

After creating it, run the script directly and run the cron once. Verify both `hermes gateway run` and `hermes -p redteam gateway run` are present.
