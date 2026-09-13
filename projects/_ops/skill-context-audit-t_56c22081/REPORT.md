# Profile skill-context audit — t_56c22081

## Result

Profile catalogs were pruned by reversible `skills.disabled` configuration only. No skill source packages were deleted or archived. Skill Retriever source was the pinned trial checkout at commit `50daa5435ec3084985f58d2570a8703de4a10f7c`; the plugin was not installed in any live profile despite the parent card premise, so the audit imports its BM25 corpus loader directly and records that limitation rather than silently changing plugin enablement.

Token totals are deterministic estimates: UTF-8 bytes of `name: description` lines divided by four, rounded up. Exact character/byte counts and every indexed description are in `before.json` and `after.json`. Runtime index character counts come from `hermes --profile PROFILE prompt-size --platform discord --json`.

## Metrics

- default: 99 → 22 indexed; estimated description tokens 1950 → 439 (77.5% reduction); runtime index chars 11176 → 2923.
- software-developer: 101 → 59 indexed; estimated description tokens 1992 → 1145 (42.5% reduction); runtime index chars 11385 → 7068.
- social-growth: 99 → 33 indexed; estimated description tokens 1957 → 676 (65.5% reduction); runtime index chars 11201 → 4053.
- trading-specialist: 96 → 16 indexed; estimated description tokens 1888 → 310 (83.6% reduction); runtime index chars 10795 → 2053.
- business-operator: 95 → 23 indexed; estimated description tokens 1866 → 459 (75.4% reduction); runtime index chars 10698 → 2703.
- personal: 96 → 22 indexed; estimated description tokens 1885 → 433 (77.0% reduction); runtime index chars 10896 → 2729.
- fitness: 0 → 0 indexed; estimated description tokens 0 → 0 (0% reduction); runtime index chars 0 → 0.
- redteam: 97 → 17 indexed; estimated description tokens 1909 → 322 (83.1% reduction); runtime index chars 10997 → 2566.
- researcher: 95 → 17 indexed; estimated description tokens 1866 → 320 (82.9% reduction); runtime index chars 10813 → 2160.

## Decisions and disabled skills

### default

Retained scope: chief orchestration, routing, synthesis, and common coordination only.

Disabled (77): `affiliate-business-operations`, `agentmail`, `ai-coding-agents`, `api-ci-cd-onboarding`, `app-deploy-policy`, `axolotl`, `baoyu-article-illustrator`, `baoyu-comic`, `blocked-page-recovery`, `box`, `browser-assisted-personal-applications`, `browser-oauth-automation`, `claude-design`, `cloud-app-deployment-ops`, `codebase-inspection`, `coding-school-student-progress`, `competitor-news-monitor`, `creative-ideation`, `creative-production-systems`, `creator-business-operations`, `debugging-hermes-tui-commands`, `discord-redteam-workspace-setup`, `document-production-workflows`, `docx`, `dspy`, `email-inbox-triage`, `fine-tuning-with-trl`, `github-issue-to-pr`, `github-pr-workflow`, `github-workflows`, `godmode`, `hermes-email`, `hermes-memory-hygiene`, `hermes-s6-container-supervision`, `himalaya`, `inspecting-hermes-desktop-dom`, `intelbase`, `linear`, `macos-automation`, `media-source-ingestion`, `merge-reconciler`, `minecraft-modpack-server`, `mlops-model-tooling`, `music-and-audio-workflows`, `obliteratus`, `outlines`, `parrot-ai-creative-pipeline`, `pdf`, `petdex`, `pixel-art`, `plan`, `platform-device-integrations`, `pokemon-player`, `popular-web-designs`, `product-price-monitor`, `profile-consolidation-model`, `profile-consolidation-workflow`, `python-development-tools`, `robinhood-trading-operator`, `runelite-plugin-development`, `sdlc-review`, `secret-audit-and-precommit`, `social-video-cron-growth-loop`, `software-quality-workflows`, `system-portfolio-cleanup`, `test-driven-development`, `trap-chat`, `tweetbetweenthelines-deployment`, `unity-mcp-integration`, `unsloth`, `vercel-portfolio-evidence-gates`, `vercel-token-and-cleanup-patterns`, `visual-artifact-design`, `writing-plans`, `xlsx`, `youtube-automation-with-tts`, `youtube-quota-queue-management`

Rationale: each disabled entry is outside this profile’s stated ownership in `AGENT_TEAM.md`; role-critical entries are retained regardless of zero usage. Historical usage counters were reviewed only as supporting evidence because copied catalogs carry inherited counters.

### software-developer

Retained scope: software, infrastructure, release, CI/CD, Unity, technical document and automation support.

Disabled (42): `affiliate-business-operations`, `agentmail`, `ai-coding-agents`, `alltrails-fitness-planner`, `baoyu-article-illustrator`, `baoyu-comic`, `box`, `browser-assisted-personal-applications`, `claude-design`, `coding-school-student-progress`, `competitor-news-monitor`, `creative-ideation`, `creative-production-systems`, `creator-business-operations`, `discord-redteam-workspace-setup`, `document-to-action-items`, `email-discussion-briefing`, `email-inbox-triage`, `godmode`, `grounded-citations`, `hermes-email`, `himalaya`, `intelbase`, `macos-automation`, `meeting-action-items`, `merge-reconciler`, `music-and-audio-workflows`, `parrot-ai-creative-pipeline`, `petdex`, `pixel-art`, `pokemon-player`, `popular-web-designs`, `product-price-monitor`, `professional-work`, `research-intelligence-sources`, `robinhood-trading-operator`, `session-librarian`, `social-video-cron-growth-loop`, `vercel-portfolio-evidence-gates`, `vercel-token-and-cleanup-patterns`, `weekly-review-planning`, `workspace-productivity-integrations`

Rationale: each disabled entry is outside this profile’s stated ownership in `AGENT_TEAM.md`; role-critical entries are retained regardless of zero usage. Historical usage counters were reviewed only as supporting evidence because copied catalogs carry inherited counters.

### social-growth

Retained scope: content strategy, creative production, publishing, analytics, and public-source recovery.

Disabled (66): `agentmail`, `ai-coding-agents`, `api-ci-cd-onboarding`, `app-deploy-policy`, `axolotl`, `box`, `browser-assisted-personal-applications`, `browser-oauth-automation`, `cloud-app-deployment-ops`, `codebase-inspection`, `coding-school-student-progress`, `debugging-hermes-tui-commands`, `discord-redteam-workspace-setup`, `document-to-action-items`, `dspy`, `email-discussion-briefing`, `email-inbox-triage`, `fine-tuning-with-trl`, `github`, `github-issue-to-pr`, `github-pr-workflow`, `github-repo-management`, `github-workflows`, `godmode`, `google-oauth-unified-2026-09`, `hermes-email`, `hermes-s6-container-supervision`, `himalaya`, `inspecting-hermes-desktop-dom`, `intelbase`, `kanban-orchestrator`, `linear`, `macos-automation`, `meeting-action-items`, `merge-reconciler`, `minecraft-modpack-server`, `mlops-model-tooling`, `native-mcp`, `obliteratus`, `outlines`, `petdex`, `plan`, `platform-device-integrations`, `pokemon-player`, `product-price-monitor`, `professional-work`, `project-portfolio-lifecycle`, `python-development-tools`, `robinhood-trading-operator`, `runelite-plugin-development`, `sdlc-review`, `secret-audit-and-precommit`, `session-librarian`, `software-project-delivery`, `software-quality-workflows`, `system-portfolio-cleanup`, `test-driven-development`, `trap-chat`, `tweetbetweenthelines-deployment`, `unity-mcp-integration`, `unsloth`, `vercel-portfolio-evidence-gates`, `vercel-token-and-cleanup-patterns`, `webhook-subscriptions`, `weekly-review-planning`, `writing-plans`

Rationale: each disabled entry is outside this profile’s stated ownership in `AGENT_TEAM.md`; role-critical entries are retained regardless of zero usage. Historical usage counters were reviewed only as supporting evidence because copied catalogs carry inherited counters.

### trading-specialist

Retained scope: broker operations, market evidence, risk records, and supporting documents only.

Disabled (80): `affiliate-business-operations`, `agentmail`, `ai-coding-agents`, `api-ci-cd-onboarding`, `app-deploy-policy`, `axolotl`, `baoyu-article-illustrator`, `baoyu-comic`, `box`, `browser-assisted-personal-applications`, `claude-design`, `cloud-app-deployment-ops`, `codebase-inspection`, `coding-school-student-progress`, `creative-ideation`, `creative-production-systems`, `creator-business-operations`, `debugging-hermes-tui-commands`, `discord-redteam-workspace-setup`, `document-production-workflows`, `docx`, `dspy`, `email-discussion-briefing`, `email-inbox-triage`, `fine-tuning-with-trl`, `github`, `github-issue-to-pr`, `github-pr-workflow`, `github-repo-management`, `github-workflows`, `godmode`, `hermes-email`, `hermes-s6-container-supervision`, `himalaya`, `inspecting-hermes-desktop-dom`, `intelbase`, `kanban-orchestrator`, `linear`, `macos-automation`, `meeting-action-items`, `merge-reconciler`, `minecraft-modpack-server`, `mlops-model-tooling`, `music-and-audio-workflows`, `native-mcp`, `obliteratus`, `outlines`, `parrot-ai-creative-pipeline`, `petdex`, `pixel-art`, `plan`, `platform-device-integrations`, `pokemon-player`, `popular-web-designs`, `product-price-monitor`, `professional-work`, `project-portfolio-lifecycle`, `python-development-tools`, `runelite-plugin-development`, `sdlc-review`, `secret-audit-and-precommit`, `session-librarian`, `social-video-cron-growth-loop`, `software-project-delivery`, `software-quality-workflows`, `system-portfolio-cleanup`, `test-driven-development`, `trap-chat`, `tweetbetweenthelines-deployment`, `unity-mcp-integration`, `unsloth`, `vercel-portfolio-evidence-gates`, `vercel-token-and-cleanup-patterns`, `visual-artifact-design`, `webhook-subscriptions`, `weekly-review-planning`, `workspace-productivity-integrations`, `writing-plans`, `youtube-automation-with-tts`, `youtube-quota-queue-management`

Rationale: each disabled entry is outside this profile’s stated ownership in `AGENT_TEAM.md`; role-critical entries are retained regardless of zero usage. Historical usage counters were reviewed only as supporting evidence because copied catalogs carry inherited counters.

### business-operator

Retained scope: offers, revenue, sales, client delivery, research, and business documents only.

Disabled (72): `agentmail`, `ai-coding-agents`, `api-ci-cd-onboarding`, `app-deploy-policy`, `axolotl`, `baoyu-article-illustrator`, `baoyu-comic`, `box`, `browser-oauth-automation`, `claude-design`, `cloud-app-deployment-ops`, `codebase-inspection`, `coding-school-student-progress`, `creative-ideation`, `creative-production-systems`, `debugging-hermes-tui-commands`, `discord-redteam-workspace-setup`, `document-to-action-items`, `dspy`, `email-inbox-triage`, `fine-tuning-with-trl`, `github`, `github-issue-to-pr`, `github-pr-workflow`, `github-repo-management`, `github-workflows`, `godmode`, `hermes-email`, `hermes-s6-container-supervision`, `himalaya`, `inspecting-hermes-desktop-dom`, `intelbase`, `kanban-orchestrator`, `macos-automation`, `merge-reconciler`, `minecraft-modpack-server`, `mlops-model-tooling`, `music-and-audio-workflows`, `native-mcp`, `obliteratus`, `outlines`, `parrot-ai-creative-pipeline`, `petdex`, `pixel-art`, `plan`, `platform-device-integrations`, `pokemon-player`, `popular-web-designs`, `project-portfolio-lifecycle`, `python-development-tools`, `robinhood-trading-operator`, `runelite-plugin-development`, `sdlc-review`, `secret-audit-and-precommit`, `session-librarian`, `social-video-cron-growth-loop`, `software-project-delivery`, `software-quality-workflows`, `system-portfolio-cleanup`, `test-driven-development`, `trap-chat`, `tweetbetweenthelines-deployment`, `unity-mcp-integration`, `unsloth`, `vercel-portfolio-evidence-gates`, `vercel-token-and-cleanup-patterns`, `visual-artifact-design`, `webhook-subscriptions`, `weekly-review-planning`, `writing-plans`, `youtube-automation-with-tts`, `youtube-quota-queue-management`

Rationale: each disabled entry is outside this profile’s stated ownership in `AGENT_TEAM.md`; role-critical entries are retained regardless of zero usage. Historical usage counters were reviewed only as supporting evidence because copied catalogs carry inherited counters.

### personal

Retained scope: personal planning, Workspace/email administration, professional development, and fitness planning.

Disabled (74): `affiliate-business-operations`, `agentmail`, `ai-coding-agents`, `api-ci-cd-onboarding`, `app-deploy-policy`, `axolotl`, `baoyu-article-illustrator`, `baoyu-comic`, `box`, `browser-oauth-automation`, `claude-design`, `cloud-app-deployment-ops`, `codebase-inspection`, `coding-school-student-progress`, `competitor-news-monitor`, `creative-ideation`, `creative-production-systems`, `creator-business-operations`, `debugging-hermes-tui-commands`, `discord-redteam-workspace-setup`, `document-to-action-items`, `dspy`, `fine-tuning-with-trl`, `github`, `github-issue-to-pr`, `github-pr-workflow`, `github-repo-management`, `github-workflows`, `godmode`, `hermes-email`, `hermes-s6-container-supervision`, `himalaya`, `inspecting-hermes-desktop-dom`, `intelbase`, `kanban-orchestrator`, `linear`, `macos-automation`, `merge-reconciler`, `minecraft-modpack-server`, `mlops-model-tooling`, `music-and-audio-workflows`, `native-mcp`, `obliteratus`, `outlines`, `parrot-ai-creative-pipeline`, `petdex`, `pixel-art`, `plan`, `platform-device-integrations`, `pokemon-player`, `popular-web-designs`, `project-portfolio-lifecycle`, `python-development-tools`, `research-intelligence-sources`, `robinhood-trading-operator`, `runelite-plugin-development`, `sdlc-review`, `secret-audit-and-precommit`, `social-video-cron-growth-loop`, `software-project-delivery`, `software-quality-workflows`, `system-portfolio-cleanup`, `test-driven-development`, `trap-chat`, `tweetbetweenthelines-deployment`, `unity-mcp-integration`, `unsloth`, `vercel-portfolio-evidence-gates`, `vercel-token-and-cleanup-patterns`, `visual-artifact-design`, `webhook-subscriptions`, `writing-plans`, `youtube-automation-with-tts`, `youtube-quota-queue-management`

Rationale: each disabled entry is outside this profile’s stated ownership in `AGENT_TEAM.md`; role-critical entries are retained regardless of zero usage. Historical usage counters were reviewed only as supporting evidence because copied catalogs carry inherited counters.

### fitness

Retained scope: retired profile; no installed catalog and no config created.

Disabled (0): (none).

Rationale: each disabled entry is outside this profile’s stated ownership in `AGENT_TEAM.md`; role-critical entries are retained regardless of zero usage. Historical usage counters were reviewed only as supporting evidence because copied catalogs carry inherited counters.

### redteam

Retained scope: authorized defensive/adversarial review, Mantis, evidence, repository inspection, and secret auditing.

Disabled (80): `affiliate-business-operations`, `agentmail`, `ai-coding-agents`, `api-ci-cd-onboarding`, `app-deploy-policy`, `axolotl`, `baoyu-article-illustrator`, `baoyu-comic`, `box`, `browser-assisted-personal-applications`, `browser-oauth-automation`, `claude-design`, `cloud-app-deployment-ops`, `coding-school-student-progress`, `competitor-news-monitor`, `creative-ideation`, `creative-production-systems`, `creator-business-operations`, `debugging-hermes-tui-commands`, `discord-redteam-workspace-setup`, `document-production-workflows`, `document-to-action-items`, `docx`, `dspy`, `email-discussion-briefing`, `email-inbox-triage`, `fine-tuning-with-trl`, `github-issue-to-pr`, `github-pr-workflow`, `github-workflows`, `google-workspace`, `hermes-email`, `hermes-s6-container-supervision`, `himalaya`, `inspecting-hermes-desktop-dom`, `kanban-orchestrator`, `linear`, `macos-automation`, `meeting-action-items`, `merge-reconciler`, `minecraft-modpack-server`, `mlops-model-tooling`, `music-and-audio-workflows`, `obliteratus`, `outlines`, `parrot-ai-creative-pipeline`, `pdf`, `petdex`, `pixel-art`, `plan`, `platform-device-integrations`, `pokemon-player`, `popular-web-designs`, `product-price-monitor`, `professional-work`, `project-portfolio-lifecycle`, `python-development-tools`, `robinhood-trading-operator`, `runelite-plugin-development`, `sdlc-review`, `session-librarian`, `social-video-cron-growth-loop`, `software-project-delivery`, `software-quality-workflows`, `system-portfolio-cleanup`, `test-driven-development`, `trap-chat`, `tweetbetweenthelines-deployment`, `unity-mcp-integration`, `unsloth`, `vercel-portfolio-evidence-gates`, `vercel-token-and-cleanup-patterns`, `visual-artifact-design`, `webhook-subscriptions`, `weekly-review-planning`, `workspace-productivity-integrations`, `writing-plans`, `xlsx`, `youtube-automation-with-tts`, `youtube-quota-queue-management`

Rationale: each disabled entry is outside this profile’s stated ownership in `AGENT_TEAM.md`; role-critical entries are retained regardless of zero usage. Historical usage counters were reviewed only as supporting evidence because copied catalogs carry inherited counters.

### researcher

Retained scope: external research, citations, source recovery, documents, transcripts, and monitoring.

Disabled (78): `affiliate-business-operations`, `agentmail`, `ai-coding-agents`, `api-ci-cd-onboarding`, `app-deploy-policy`, `axolotl`, `baoyu-article-illustrator`, `baoyu-comic`, `box`, `browser-assisted-personal-applications`, `claude-design`, `cloud-app-deployment-ops`, `codebase-inspection`, `coding-school-student-progress`, `creative-ideation`, `creative-production-systems`, `creator-business-operations`, `debugging-hermes-tui-commands`, `discord-redteam-workspace-setup`, `document-production-workflows`, `dspy`, `email-discussion-briefing`, `email-inbox-triage`, `fine-tuning-with-trl`, `github`, `github-issue-to-pr`, `github-pr-workflow`, `github-repo-management`, `github-workflows`, `godmode`, `hermes-email`, `hermes-s6-container-supervision`, `himalaya`, `inspecting-hermes-desktop-dom`, `kanban-orchestrator`, `linear`, `macos-automation`, `meeting-action-items`, `merge-reconciler`, `minecraft-modpack-server`, `mlops-model-tooling`, `music-and-audio-workflows`, `native-mcp`, `obliteratus`, `outlines`, `parrot-ai-creative-pipeline`, `petdex`, `pixel-art`, `plan`, `platform-device-integrations`, `pokemon-player`, `popular-web-designs`, `professional-work`, `project-portfolio-lifecycle`, `python-development-tools`, `robinhood-trading-operator`, `runelite-plugin-development`, `sdlc-review`, `secret-audit-and-precommit`, `session-librarian`, `social-video-cron-growth-loop`, `software-project-delivery`, `software-quality-workflows`, `system-portfolio-cleanup`, `test-driven-development`, `trap-chat`, `tweetbetweenthelines-deployment`, `unity-mcp-integration`, `unsloth`, `vercel-portfolio-evidence-gates`, `vercel-token-and-cleanup-patterns`, `visual-artifact-design`, `webhook-subscriptions`, `weekly-review-planning`, `workspace-productivity-integrations`, `writing-plans`, `youtube-automation-with-tts`, `youtube-quota-queue-management`

Rationale: each disabled entry is outside this profile’s stated ownership in `AGENT_TEAM.md`; role-critical entries are retained regardless of zero usage. Historical usage counters were reviewed only as supporting evidence because copied catalogs carry inherited counters.

## Exact operation and restoration

Audit/re-index:

    /opt/hermes/.venv/bin/python /opt/data/HeRmEz/projects/_ops/skill-context-audit-t_56c22081/audit_profile_skills.py snapshot --label verification

The supported interactive command for a named profile is `hermes --profile PROFILE skills config` (the card’s `hermes skills config --profile` ordering is not accepted by this CLI). Because workers are headless and the command requires a TTY, the script invokes the same public `hermes_cli.skills_config.save_disabled_skills` writer with a profile-scoped Hermes home. This produced only `skills.disabled` semantic changes.

Per-profile UI review example:

    hermes --profile software-developer skills config

Curator evidence (safe preview only; this run same approach was run for all nine profiles):

    hermes --profile software-developer curator run --dry-run

Restore one profile:

    cp /opt/data/HeRmEz/projects/_ops/skill-context-audit-t_56c22081/config-backup/PROFILE-config.yaml /opt/data/profiles/PROFILE/config.yaml

Restore default:

    cp /opt/data/HeRmEz/projects/_ops/skill-context-audit-t_56c22081/config-backup/default-config.yaml /opt/data/config.yaml

No fitness config existed before or after. A full rollback is exact because backups preserve the pre-change bytes and modes.

## Validation

- All nine catalogs were passed through Skill Retriever’s recursive, profile-aware loader before and after.
- All eight active profiles retain `hermes-agent` and the shared self-review/Kanban operating capabilities appropriate to dispatched work.
- Specialist role checks passed against the explicit retained sets in `audit_profile_skills.py`.
- `config-safety-check.json` proves `skills` was the only changed top-level key for each changed profile; fitness remained config-less.
- Curator was run dry-run only. No archive/delete/consolidation mutation occurred; lifecycle tuning remains in dependent card t_d7eb6af2.
- No credential/env files, Discord routing, Kanban definitions, approvals, gateway policy, tools, or plugin enablement changed.
- No gateway restart was performed. New sessions read the configs immediately; the running Hostinger gateway requires its normal SSH-managed restart only if immediate gateway-session adoption is desired.

## Artifacts

- `before.json`: baseline corpus, descriptions, usage evidence, exact counts.
- `after.json`: re-indexed retained corpus.
- `summary.json`: machine-readable reductions.
- `config-safety-check.json`: semantic change boundary proof.
- `config-backup/`: exact rollback inputs.
- `curator-dry-runs/`: one report per profile.
- `audit_profile_skills.py`: reproducible audit/config writer.
