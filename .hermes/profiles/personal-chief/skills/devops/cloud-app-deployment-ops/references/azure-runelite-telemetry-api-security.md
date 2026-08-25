# Azure near-free RuneLite telemetry API security pattern

Use this when planning/deploying an Azure backend for a public RuneLite plugin that collects game telemetry or competition data.

## Core split

- RuneLite plugin: authenticated write client for leader actions and telemetry observations.
- Azure Functions API: validation, rate limits, append-only event ingestion, aggregation/materialization.
- Cosmos DB Free Tier: clans, availability posts, fight applications, confirmed fights, observations, public summaries.
- Static Web Apps Free: website and public completed analytics; for MVP/no-quota deployments, use Static Web Apps managed API for read-only/public API routes instead of a separate Function App.
- Public website: read-only. It must not receive tokens or endpoints capable of creating fights, accepting fights, submitting events, or editing results.

## Do not rely on a static plugin secret

A RuneLite plugin is a public Java client. Any embedded static API key can be extracted. Prefer layered controls:

- plugin install registration and rotatable install tokens,
- timestamp/request-id replay protection,
- rate limiting by install/player/clan/IP/endpoint/fight,
- leader/rank authorization for management actions,
- append-only telemetry events,
- corroboration before publishing derived fight facts,
- anomaly and confidence scoring.

## High traffic / near-free guardrails

- Public website reads should use cached/sanitized endpoints or generated static JSON snapshots.
- Batch telemetry events from the plugin; avoid per-tick HTTP writes.
- Keep public polling low-frequency and use ETags/cache headers later.
- Partition Cosmos data by clan/fight keys for hot operations.
- Add app-level rate limiting before public launch instead of starting with paid API Management.
- Only introduce Azure Storage Queue/materializer Functions when write bursts require buffering.
- Do not add Front Door, App Gateway, Premium Functions, AKS, or VMs without explicit cost approval.

## GitHub Actions deployment shape

Use two workflows in the same service repo:

- `infra-terraform.yml`: Terraform plan/apply under `infra/terraform`, GitHub OIDC, environment gates `infra-dev`/`infra-prod`.
- `app-deploy.yml`: tests/package/deploy Function App and web assets, GitHub OIDC, environment gates `app-dev`/`app-prod`.

Keep Terraform state in a separate resource group/storage account from app resources.

## Public privacy defaults

Public before fight: clan names, broad time window, size target, war type, verification status.

Private before/during fight: exact world, hotspot/location, rally/fallback details, leader notes, live player positions.

Public after fight: completed sanitized analytics, confidence/caveats, aggregate metrics; avoid player-level detail until consent/product policy is finalized.