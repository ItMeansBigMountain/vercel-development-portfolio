# Portfolio Cleanup & Vercel Dehosting — Detailed Reference Pattern

Use this pattern when the user wants a full workspace audit, consolidation per a portfolio mandate (e.g., message.txt), and safe removal of stale deployments while preserving git history.

## Trigger
User says: "clean up", "remove unused", "consolidate projects", "dehost Vercel", "full system cleanup", or provides a portfolio mandate file.

## Core Workflow

### 1. Audit & Classify (single session)
```bash
# Find all git repos in workspace
find /opt/data/HeRmEz/projects -maxdepth 2 -type d -name ".git" | wc -l
# List them
find /opt/data/HeRmEz/projects -maxdepth 2 -type d -name ".git" | while read g; do echo "=== $(dirname $g) ==="; done

# Read existing deployment audits
cat /opt/data/HeRmEz/projects/VERCEL_DEPLOYMENT_REVIEW_2026-05-26.md
cat /opt/data/HeRmEz/projects/VERCEL_FREE_PLAN_AUDIT.md
cat /opt/data/HeRmEz/projects/DEPLOY_FINAL_URLS.md
```

### 2. Build Master Classification Card
Create one **master architecture card** (priority 220, operations-engineer) that contains:
- Source of truth (portfolio mandate file attached to portfolio card)
- **Canonical parent projects** (keep + CI/CD + active)
- **OSRS Plugin Hub track** (keep + CI/CD, no Vercel)
- **Keep GitHub-only** (learning/history, NO Vercel, NO CI/CD beyond lint)
- **Absorbed prototypes** (merged into canonical parents)
- **Duplicate/legacy trees** (archive)
- **DEHOST LIST** (Vercel projects to remove AFTER migration verification)

**Key fields:**
- `idempotency_key` = `full-system-cleanup-architecture-<date>`
- `--max-runtime` = `3h`
- `--json` for programmatic ID capture

### 3. Create Downstream CI/CD Cards (one per canonical parent)
Each gets its own card assigned to `software-developer` with:
- `idempotency_key` = `<project>-github-actions-ci-<date>`
- `parents=[master]` so they wait for master
- Explicit workflow requirements: build, preview, mobile, security, release
- Required secrets listed
- Must-pass dependencies (existing Kanban cards)

### 4. Create OSRS Plugin Hub Cards (2 cards)
1. **Boilerplate template** — Gradle CI/CD template for Plugin Hub compliance
2. **Validation sweep** — Apply template to all 26 plugin repos, verify builds

### 5. Create Operations Dehosting Card
Single card `t_7767afa3` (priority 180, operations-engineer):
- Dehosts Vercel projects **only after** master + reviewer pass
- **No git deletion** — only Vercel project removal
- Restart instructions documented per project
- Assigned to `operations-engineer` (not software-developer)

### 6. Create Reviewer Gate
Independent `reviewer` card (priority 100) with parents = [master, all CI/CD cards, ops]:
- Verifies classification matches mandate
- Verifies green CI/CD with correct environments/secrets
- Verifies OSRS validation complete
- Verifies dehost list accurate, no repo/history deleted
- Verifies no stray Vercel projects remain
- **Non-trivial deliverables require independent reviewer verification — implementers do not self-approve**

### 7. Schedule with Dependencies
```bash
# Master runs immediately
hermes kanban schedule <master> 'Immediate: defines all downstream work'

# Each downstream scheduled with reason
hermes kanban schedule <card> 'P0 after OAuth preview'      # tweetBetweenTheLines
hermes kanban schedule <card> 'P0 after Vercel blocker'    # CombatAtlas
hermes kanban schedule <card> 'P1 after P0'                # Coding School
# ... etc
hermes kanban schedule <reviewer> 'final gate'
```

### 8. Interactive User Polling (CRITICAL)
Before ANY destructive action (archive, dehost):
```python
clarify(
    question="Select which categories to ARCHIVE...",
    choices=["Learning/History only", "Absorbed prototypes", "Duplicate/legacy", "Keep all"]
)
clarify(
    question="Select which Vercel deployments to REMOVE...",
    choices=["Dehost all N", "Keep these M", "Keep these K", "Review individually"]
)
```
**Never execute without explicit user selection.** The polling pattern gives user time to answer and creates audit trail.

## Vercel Dehosting Execution

### Token Verification First
```bash
# Verify token works and shows projects
export VERCEL_TOKEN=<token>
curl -H "Authorization: Bearer $VERCEL_TOKEN" https://api.vercel.com/v9/projects

# If 0 projects returned:
# - Check teamId scope: ?teamId=<team_id>
# - Check personal scope: ?personal=true
# - Token may lack project:read scope or be scoped to wrong account
```

### Dehost Loop (per project)
```bash
# Get project ID by name
# Then: DELETE /v9/projects/<project_id>?teamId=<team_id>
# Verify 200, log success/failure
```

**If token fails:** Leave ops card in `todo`, note blocker in card comment, wait for credential refresh.

## Pitfalls & Lessons Learned (from 2026-08-25 session)

1. **Token scope mismatch** — Personal token may not see team projects. Must specify `teamId` or use team-scoped token. The May 2026 audit showed 55 projects; new token showed 0.

2. **Never delete git history** — Archive to `_archive/` instead. User explicitly: "I will NOT delete any git history — only move directories out of /opt/data/HeRmEz/projects/"

3. **Master card must be source of truth** — All downstream cards reference it. If classification changes, update master and recreate affected downstream.

4. **Reviewer gate is mandatory** — Per AGENT_TEAM.md: "Non-trivial deliverables require independent reviewer verification. Implementers do not self-approve."

5. **Idempotency keys prevent duplicates** — Use `<descriptive>-<date>` pattern on every create.

6. **Schedule with reasons, not just timing** — `schedule <id> 'reason'` creates audit trail for why card runs when it does.

7. **Ops card separate from dev cards** — Dehosting is operations work; assign to `operations-engineer`, not `software-developer`.

8. **Archive before dehost** — Local repos archived first (31 moved in this session). Vercel dehosting only after local cleanup verified.

9. **Absorbed prototypes stay until absorption verified** — `twitter-therapy-app`, `consumer-advocate-app`, `music-mood-app`, `local-meeting-transcriber`, `honda-tech-upgrade`, `store-code-content-studio`, `ticVoter/*` only dehosted AFTER canonical parent confirms absorption.

## File Structure Created
```
/opt/data/HeRmEz/projects/_archive/      # 31 archived repos (git history intact)
/opt/data/skills/devops/system-portfolio-cleanup/references/portfolio-cleanup-and-dehosting.md  # This file
```

## Kanban Card IDs from 2026-08-25 Session (reference)
- Master: `t_2b26c214`
- Reviewer: `t_71b30a9d`
- Ops dehost: `t_7767afa3`
- Canonical CI/CD: `t_85b7ca88` (tbtl), `t_1330a99f` (CombatAtlas), `t_06935372` (Coding School), `t_1302a372` (MusicAI), `t_e3b15c18` (Journal AI), `t_013a6276` (BurnoutBoyz), `t_f1628582` (TikTok), `t_a4e796ac` (Policy Pit), `t_b1b5f156` (Oyama), `t_7652b32e` (Social Publisher), `t_8ce48f85` (Viral Radar)
- OSRS: `t_ffc0b4ee` (boilerplate), `t_a04be41f` (validation)