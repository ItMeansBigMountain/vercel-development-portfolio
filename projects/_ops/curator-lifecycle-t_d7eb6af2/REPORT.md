# Curator lifecycle and promotion controls — t_d7eb6af2

## Result

PASS. Curator remains enabled on the eight active profiles with a 168-hour evaluation interval, 2-hour idle gate, 30-day stale threshold, 90-day archive threshold, recoverable pre-run backups, and consolidation disabled. The retired `fitness` profile remains absent and was not recreated.

The final full cycle scanned 260 profile-local managed candidates and retained all 260. It marked 0 newly stale, archived 0, and reactivated 0. The audited promotion gate scanned two real unmanaged software-developer skills: `agent-reach-integration` passed and was promoted; `rtk-output-filter` failed closed and remains unmanaged with actionable static/security findings.

## Effective semantics

- Scheduler interval: `interval_hours: 168` means an automatic pass becomes eligible when elapsed time is greater than or equal to 168 hours. Manual `curator run` bypasses the interval gate.
- Idle gate: `min_idle_hours: 2` prevents an automatic background pass while the agent is not sufficiently idle; it does not change lifecycle age.
- Stale boundary: `anchor <= now - 30 days`, equivalently idle age greater than or equal to 30 days, marks an active managed skill stale.
- Archive boundary: `anchor <= now - 90 days`, equivalently idle age greater than or equal to 90 days, archives a non-pinned managed skill. Archive is recoverable; automatic deletion is not used.
- Activity anchor: latest view/use/patch timestamp, falling back to creation time. Pinned and cron-referenced skills are exempt. Newly encountered built-ins are seeded at first sight rather than aged from epoch.
- Dry-run: reports candidate count and predicted transitions but applies no skill state/archive/consolidation changes. It does update Curator run/report telemetry.
- Normal mode: creates a profile-local tar.gz snapshot first, then applies deterministic transitions. LLM consolidation remains off.

Boundary tests prove one second before 30/90 days does not transition, while exactly 30/90 days does.

## Configuration

Active config paths:

- default: `/opt/data/config.yaml`
- named profiles: `/opt/data/profiles/{software-developer,social-growth,trading-specialist,business-operator,personal,redteam,researcher}/config.yaml`

Effective Curator values on all eight active profiles:

    curator.enabled: true
    curator.interval_hours: 168
    curator.min_idle_hours: 2
    curator.stale_after_days: 30
    curator.archive_after_days: 90
    curator.consolidate: false (explicit on five profiles; safe runtime default on redteam/researcher)
    curator.backup.enabled: true
    curator.backup.keep: 5
    skills.guard_agent_created: true

The only semantic config change from the exact backups was `skills.guard_agent_created: false -> true` on each active profile. `config-verification.json` confirms 8/8 profiles have only that expected change. Thresholds already matched the intended values and were preserved rather than rewritten unnecessarily.

This guard applies the existing Hermes `skills_guard` scanner to agent-created skill writes. Adoption is additionally routed through `curator_audited_adopt.py`, which fails closed unless the candidate passes Hermes' existing name, new-skill frontmatter/60-character routing description, content-size, and `skills_guard` checks.

## Promotion evidence

Canonical command:

    python3 /opt/data/HeRmEz/projects/_ops/curator-lifecycle-t_d7eb6af2/curator_audited_adopt.py --profile PROFILE --dry-run --evidence EVIDENCE.json SKILL

Remove `--dry-run` only after reviewing the evidence. Do not use raw `hermes curator adopt` for agent-created candidates; it does not run the static checklist.

Observed:

- `agent-reach-integration`: dry-run passed; normal gated adoption exited 0; read-back shows `created_by: agent`, `state: active`, `pinned: false`. Promoted: 1.
- `rtk-output-filter`: rejected before adoption. Its description exceeds the 60-character new-skill routing budget, and `skills_guard` reported three actionable dangerous/caution patterns. Read-back remains unmanaged. Rejected: 1.
- A missing or ambiguous skill path also fails closed.

Promotion artifacts are under `promotion-evidence/`; they contain the exact command, return code, stdout/stderr, checklist and findings.

## Full-cycle evidence

For each active profile, the sequence was:

    hermes --profile PROFILE curator run --dry-run
    hermes --profile PROFILE curator run
    hermes --profile PROFILE curator status

Default used an explicit clean profile binding:

    env -u HERMES_PROFILE HERMES_HOME=/opt/data hermes curator run --dry-run
    env -u HERMES_PROFILE HERMES_HOME=/opt/data hermes curator run

Final normal-cycle results:

- default: scanned 35, retained 35, newly stale 0, archived 0
- software-developer: scanned 33, retained 33, newly stale 0, archived 0
- social-growth: scanned 34, retained 34, newly stale 0, archived 0
- trading-specialist: scanned 32, retained 32, newly stale 0, archived 0
- business-operator: scanned 31, retained 31, newly stale 0, archived 0
- personal: scanned 32, retained 32, newly stale 0, archived 0
- redteam: scanned 32, retained 32, newly stale 0, archived 0
- researcher: scanned 31, retained 31, newly stale 0, archived 0

Total: scanned 260; retained 260; marked stale 0; archived 0; rejected 1; promoted 1. Every dry-run, normal run, and status command exited 0. Each normal run reported a newly created snapshot before transitions.

## Artifacts

- `REPORT.md` — this report.
- `config-before/` — exact pre-change config bytes and modes for eight active profiles.
- `config-verification.json` — secret-safe semantic boundary proof and effective values.
- `curator_audited_adopt.py` — fail-closed promotion gate.
- `test_curator_audited_adopt.py` — promotion-gate tests.
- `test_curator_thresholds.py` — exact 30/90-day boundary tests.
- `promotion-evidence/` — one passing dry-run, one verified promotion, one rejected promotion.
- `final-cycle/summary.json` — machine-readable counts and return codes.
- `final-cycle/PROFILE/{dry-run,normal,status}.txt` — raw final-cycle outputs.
- `cycle-evidence/` — earlier before/dry/normal/after snapshots retained as additional evidence.

## Verification

    cd /opt/data/HeRmEz/projects/_ops/curator-lifecycle-t_d7eb6af2
    python3 -m unittest -v test_curator_audited_adopt.py test_curator_thresholds.py

Result: 7/7 tests passed. Config semantic check: 8/8 profiles only changed the intended guard. Final cycles: 24/24 commands passed (8 profiles × dry-run/normal/status). Promotion path exit codes were dry-run 0, promotion 0, expected rejection 1.

## Safety and exceptions

- No credentials, `.env` files, Discord routing, Kanban profile definitions, approval mode, gateway settings, or SSH/Hostinger policy were changed.
- No skill source was deleted. Normal Curator runs archived nothing.
- LLM consolidation stayed disabled to avoid opinionated merges and auxiliary-model mutation.
- `fitness` is retired with no live profile directory/config and was intentionally excluded.
- The static scanner is conservative and can flag legitimate operational documentation. A failure remains unpromoted; remediate the exact findings and rerun rather than bypassing the gate.

## Rollback and restoration

Restore all config files exactly from `config-before/` (default maps to `/opt/data/config.yaml`; named backups map to `/opt/data/profiles/PROFILE/config.yaml`). To reverse only this promotion without deleting content, restore the software-developer usage sidecar from the pre-promotion cycle evidence or use the Curator mutation ledger/rollback command after identifying the exact entry:

    hermes --profile software-developer curator ledger
    hermes --profile software-developer curator rollback --help

For any archived skill in a future cycle:

    hermes --profile PROFILE curator list-archived
    hermes --profile PROFILE curator restore SKILL

The normal-run snapshot paths are reported in each `final-cycle/PROFILE/normal.txt` and live under that profile's `skills/.curator_backups/`.

## Restart requirement

No gateway restart was performed. Fresh CLI/Kanban sessions read the updated configs immediately. Existing long-running gateway sessions require the normal Hostinger/SSH-managed restart only if immediate adoption of `skills.guard_agent_created` is required; do not restart the gateway locally.
