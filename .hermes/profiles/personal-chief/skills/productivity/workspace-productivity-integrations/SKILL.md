---
name: workspace-productivity-integrations
description: "Use when operating productivity/workspace systems such as Airtable, Notion, Obsidian, maps/geocoding, or Teams meeting pipelines. Umbrella for data, notes, location, and meeting automations."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [productivity, airtable, notion, obsidian, maps, teams, automation]
    related_skills: [google-workspace, operator-morning-reports]
---

# Workspace Productivity Integrations

## Overview

Use this umbrella when the task is to read, write, synchronize, or summarize information in a productivity system. It consolidates workspace data tools, note systems, location utilities, and meeting-summary pipelines into one discoverable entry point.

## Choose the Integration

| User intent | Integration |
|---|---|
| CRUD structured records, filters, upserts | Airtable |
| Manage pages/databases/blocks | Notion |
| Search/create/edit local markdown notes | Obsidian |
| Geocode, find POIs, routes, time zones | Maps/OSM/OSRM |
| Operate Teams meeting summary pipeline | Teams meeting pipeline |

## Operating Rules

1. Identify the target workspace/database/vault/location/pipeline before writing.
2. Prefer read/preview operations before destructive updates.
3. Preserve source identifiers: record IDs, page IDs, note paths, coordinates, route endpoints, meeting IDs, and channel IDs.
4. For writes, summarize the exact target and fields/content changed.
5. For recurring reports, make output delta-oriented and concise.
6. When helping the user organize Discord/workspace channels, go one channel at a time if requested: give the channel name, purpose, and copy-paste channel topic/prompt only; wait for “next” before continuing.

## Discord Channel Routing for This User

Use this when Discord/server organization or channel-topic prompts come up:

- `#general` — global commands, orchestration, cron/admin, morning/operator reports.
- `#coding` — dev, repos, debugging, GitHub, deployments, PRs, tests, logs, and project implementation.
- `#personal` — personal life, family, goals, and private coaching context.
- YouTube automation deserves its own channel when present: faceless/newsletter videos, Viral Radar clips, upload queues/limits, channel-token routing, titles/descriptions/hashtags, and creator clipping.
- Trading deserves its own channel when present: Robinhood, portfolio scans, orders/positions, P/L, power-hour monitors, watchlists, earnings, and trading cron outputs.
- Business can absorb school/career if the user says so: affiliate marketing, TikTok/Shopify/Stripe, creator monetization, Jared/kids coding tutoring as a business, parent-facing progress reports, pricing/packages, outreach, and income-oriented career growth.
- Gaming can separate OSRS/RuneLite, game servers, Minecraft/modpacks, Pokémon emulator tasks, mobile game ideas, and game MVPs.
- Security/redteam can separate pentest/adversarial/security-review work.
- Ops-alerts can separate noisy cron/watchdog/backup/error notifications if the server gets cluttered.

## Re-homed Playbooks

Former tool-specific skills are preserved as references:

- `references/airtable/original-skill.md` — Airtable REST CRUD, filtering, and upsert patterns.
- `references/notion/original-skill.md` plus block-type references for Notion pages/databases.
- `references/obsidian/original-skill.md` — Obsidian vault search, note creation, and edits.
- `references/maps/original-skill.md` plus map client script for geocoding, POI, routing, and time zones.
- `references/teams-meeting-pipeline/original-skill.md` — Teams meeting summary pipeline operation.
- `references/discord-channel-routing-2026-07.md` — this user's Discord channel routing, one-by-one channel prompt format, and copy/paste topic templates.

## Pitfalls

- Do not guess IDs for workspace writes; discover or ask when the target cannot be retrieved.
- Do not overwrite rich document structures when a block/record-level patch is safer.
- Do not treat geocoding/routing results as exact without noting provider/source and ambiguity.
- Do not expose credentials or tokens in reports.

## Verification Checklist

- [ ] Target workspace/object/location was resolved.
- [ ] Read-before-write was performed for stateful changes.
- [ ] Write operations report object IDs and changed fields/paths.
- [ ] Location results include enough coordinates/source detail to reproduce.
- [ ] Meeting/report outputs distinguish transcript facts from generated summaries.
