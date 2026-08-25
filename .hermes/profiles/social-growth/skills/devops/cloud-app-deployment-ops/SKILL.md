---
name: cloud-app-deployment-ops
description: "Use when setting up cloud provider CLIs, credentials, or deploying/troubleshooting hosted apps such as Vercel/static/Flask/Django projects."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [devops, cloud, cli, vercel, deployment, credentials, hosting]
    related_skills: [github-pr-workflow, software-quality-workflows]
---

# Cloud App Deployment Ops

## Overview

Use this umbrella for application delivery work that crosses local code, cloud provider CLIs, credentials, and hosted deployment platforms. It consolidates provider CLI setup and Vercel-oriented deployment/triage playbooks.

## Workflow

For Vercel portfolio audits, first load `references/vercel-portfolio-audit-pattern.md`; the user cares about primary alias vs latest deployment health and end-user product readiness, not just HTTP 200.
For GitHub/Vercel project renames and alias migrations, load `references/vercel-project-rename-and-alias-migration.md`; preserve the project ID and environment variables, verify aliases independently, diagnose SSO redirects as deployment protection, and never delete unrelated projects merely because a global alias is unavailable.
For anonymous likes/dislikes, reactions, or voting APIs on serverless deployments, load `references/serverless-anonymous-voting-and-rate-limits.md`; use signed identities, layered limits, shared atomic storage with TTLs for production, separate test-runner discovery, and deployed-alias mobile/API verification.

For Azure near-free backend/service planning, load `references/azure-free-tier-service-planning.md`; the user prefers service-owned `infra/` directories and explicit cost/security guardrails before deployment.
For Azure Terraform + GitHub Actions deployment setup, load `references/azure-terraform-github-actions-oidc.md`; use OIDC + GitHub Environment approval gates instead of long-lived Azure deploy secrets. If the user says “pim up,” start `az login --use-device-code` and give them the code/link.
For Azure service-account/persistent-login setup, load `references/azure-service-principal-persistent-login.md`; use GitHub OIDC for pipelines, a local service-principal helper outside repos for Hermes CLI sessions, and verify no paid resources were created by identity bootstrap.
For Azure Static Web Apps managed API fallback / no-quota MVP deployment, load `references/azure-static-webapps-managed-api-fallback.md`; use it when a separate Azure Functions/App Service Plan hits quota or the MVP can run as Static Web Apps Free + managed API.
For production Cosmos persistence behind a Static Web Apps managed API, load `references/azure-static-webapps-cosmos-production-wiring.md`; it covers OIDC-time app-setting injection, truthful dependency health gates, privacy-safe registration, the single-free-tier-account constraint, and the limits of trusting public RuneLite clients.
For Azure reusable Hermes deployment identities, persistent local service-principal login, GitHub OIDC, cost-safe roles, Azure tags, and resource-group portal links, load `references/azure-hermes-service-account-and-resource-governance.md`.
For public RuneLite/plugin telemetry APIs on Azure, load `references/azure-runelite-telemetry-api-security.md`; keep the website read-only, avoid static plugin secrets, batch telemetry, rate-limit aggressively, and use public static/sanitized snapshots for low-latency website analytics.

1. Identify provider/platform, target account/project, and deployment environment.
2. Verify CLI installation and authentication without printing secrets.
3. Inspect existing project configuration before changing build/output settings.
4. When the app needs durable serverless persistence and the user has authorized end-to-end setup, inspect the current hosting marketplace and attempt provider-managed database provisioning before asking the user to shuttle credentials. On Vercel, a marketplace integration such as Neon can attach directly to the project and inject `DATABASE_URL` into selected environments. Verify the current plan/region, connect production + preview + development deliberately, pull development env locally without printing values, execute checked-in migrations, and confirm real tables/queries before wiring application routes.
5. Deploy or redeploy with real command output.
5. Capture both the immutable deployment URL and the canonical production alias. Provider CLIs may print the one-off URL first and the alias only after completion; treat the alias as the customer-facing URL.
6. Verify the canonical alias directly: homepage, secondary routes, API behavior, remote media, browser console, and responsive/overflow state. Do not infer alias health from the immutable deployment URL.
7. When an optional production integration lacks credentials (for example Stripe), deploy the working non-secret portions only if the app fails honestly at that boundary; report the exact environment variable names and verify the live error path rather than fabricating success.
8. Record blockers: missing credentials, paid marketplace constraints, app protection, alias drift, or unsupported runtime.

## Re-homed Playbooks

- `references/cloud-provider-cli-setup/original-skill.md` plus provider credential/setup references.
- `references/vercel-app-deployments/original-skill.md` plus Vercel deployment, OAuth, database, static shell, alias, and project-decommission references.
- `references/vercel-live-portfolio-audit-2026-06-29.md` — live Vercel portfolio audit pattern: compare primary aliases, configured aliases, and latest deployment URLs; distinguish alias drift from actual app breakage.
- `references/azure-near-free-serverless-backend.md` — Azure MVP pattern for low/near-free hosted services using Static Web Apps Free, Functions Consumption, and Cosmos DB Free Tier with budget/cost guardrails.
- `references/azure-near-free-serverless-backend.md` — Azure MVP pattern for low/near-free hosted services using Static Web Apps Free, Functions Consumption, and Cosmos DB Free Tier with budget/cost guardrails.
- `references/azure-terraform-github-actions-oidc.md` — service-owned Terraform layout, GitHub OIDC setup, environment-gated federated credentials, split infra/app workflows, and `pim up` Azure device-code login convention.
- `references/azure-service-principal-persistent-login.md` — service-principal deployer identity pattern for GitHub OIDC plus local Hermes CLI/Terraform persistent login, including secret-safe helper scripts and free/cost guardrails.
- `references/azure-static-webapps-managed-api-fallback.md` — fallback from separate Function App/App Service Plan to Static Web Apps Free managed API when Azure quota blocks Functions Consumption or a lower-quota MVP is preferred.
- `references/azure-static-webapps-managed-api-oidc.md` — end-to-end near-free Azure Static Web Apps managed API pattern with Terraform remote state, GitHub OIDC, app/infra workflow split, SWA token retrieval, Hermes Agent tags, and portal URL return format.

## References

- `references/azure-static-webapps-terraform-near-free.md` captures the Azure Static Web Apps managed-API fallback, GitHub OIDC/service-principal pattern, Terraform state/tagging conventions, path-scoped pipeline triggers, and no-surprise-cost guardrails used for near-free Azure app deployments.

## Azure Static Web Apps / pipeline support notes

- See `references/azure-static-web-apps-pipelines.md` for Static Web Apps app-root routing config, path-scoped GitHub Actions triggers, Hermes Agent Azure tags, OIDC/service-account deployment pattern, and live route verification commands.

## Pitfalls

- Do not install cloud CLIs globally when a user-local install is safer.
- Do not print tokens, API keys, or credential file contents.
- Do not claim deployment success until the live app or provider deployment status is checked.
- Do not assume Vercel marketplace databases are free or available; verify current plan constraints.

## Azure Static Web Apps Free Pattern

For near-free Azure website/API deployments, see `references/azure-static-webapps-free-python-api.md`. It covers Static Web Apps managed Python APIs, clean-route config placement, GitHub OIDC pipelines, free-tier cost guardrails, service-principal login handling, and resource tagging conventions.

## Related References

- `references/azure-static-webapps-free-tier-pattern.md` — Azure Static Web Apps Free + managed API deployment, OIDC service account, path-scoped pipelines, cost guardrails, route fallback config, and Hermes tagging.

## Verification Checklist

- [ ] CLI installed/authenticated or blocker reported.
- [ ] Project/build settings inspected.
- [ ] Deployment command output captured.
- [ ] Live URL/provider status verified.
- [ ] Credential handling was secret-safe.

## Workflow Enhancement: Cross-Project Continuity

When Vercel deployment tasks are complete and no blockers exist, transition to the next project in the user's priority queue rather than waiting for new instructions. The Robinhood trading system is a natural next step when infrastructure work is done.

### Example transition path:
1. Complete all Vercel project deployments and verifications.
2. Confirm no credential/API blockers remain.
3. Identify next priority project (e.g., Agentic Robinhood trading system).
4. Run the relevant monitoring/cron job or fetch account/portfolio status to verify operational state.

This keeps momentum and provides immediate value without idle time.
