# Hermes Command Center

Read-only dashboard plugin for the canonical Hostinger Hermes dashboard.

Canonical production URL: https://hermes-agent-xbit.srv1646785.hstgr.cloud/command-center

Data sources

- `/opt/data/kanban.db`: task counts, active work, attachment metadata.
- `/opt/data/cron/jobs.json`: schedule and health summaries (prompts/errors excluded).
- `projects/_ops/active-app-deployment-inventory.json`: canonical deployment links and classifications.
- `/opt/data/config.yaml`: primary/fallback model names only (credentials excluded).

Deployment

The existing s6-supervised dashboard loads user plugins from `/opt/data/plugins`. Deploy by linking or copying this project as `/opt/data/plugins/command-center`, then restart only the existing `dashboard` s6 service. Never start another dashboard or gateway.

Rollback

Remove `/opt/data/plugins/command-center` and restart only the `dashboard` service. No databases, cron jobs, model routing, gateways, or canonical source files are mutated.
