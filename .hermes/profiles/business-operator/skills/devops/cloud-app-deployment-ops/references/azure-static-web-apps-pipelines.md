# Azure Static Web Apps + GitHub pipeline lessons

Use when deploying the user's near-free Azure service/site stack with Azure Static Web Apps, managed APIs, Terraform, and GitHub Actions.

## Pipeline path filters

Keep deployment workflows path-scoped:

- Infra workflow should run on `infra/**` and its own workflow file only, plus manual `workflow_dispatch`.
- App workflow should run on actual deployed app inputs only: `api/**`, `web/**`, `staticwebapp.config.json`, `web/staticwebapp.config.json`, and its own workflow file, plus manual `workflow_dispatch`.
- Do not trigger app deployment just because `tests/**` changes unless tests are deployed/runtime inputs. Tests should run as part of app deployment when app inputs change, not drive deployment by themselves.

## Static Web Apps route config location

For clean client-side routes like `/clans`, `/fights`, `/leaderboard`, `/results`, place `staticwebapp.config.json` in the deployed app root when the workflow deploys `web/` as `app_location`:

```text
web/staticwebapp.config.json
```

A copy only at repo root may not be included in the deployed app artifact, causing direct route URLs to 404 even though `/` works.

Recommended config pattern:

```json
{
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/api/*", "/*.{css,scss,js,png,gif,ico,jpg,svg,webp,avif}"]
  },
  "routes": [
    { "route": "/api/*", "allowedRoles": ["anonymous"] }
  ],
  "responseOverrides": {
    "404": { "rewrite": "/index.html", "statusCode": 200 }
  },
  "globalHeaders": {
    "X-Content-Type-Options": "nosniff"
  }
}
```

Verify direct routes with real HTTP checks after deployment:

```bash
base='https://<app>.azurestaticapps.net'
for path in / /clans /fights /leaderboard /results; do
  code=$(curl -sS -o /tmp/page.html -w '%{http_code}' "$base$path")
  test "$code" = "200" || exit 1
done
```

## Azure resource naming/tags

Avoid recreating free-tier-sensitive resources just to rename them. Cosmos DB free tier is constrained, and resource replacement can create downtime or surprise costs. Prefer safe live tagging and Terraform tag defaults unless a rename is explicitly worth replacement.

Standard Clan War Board/Hermes tags:

```text
AppName=ClanWarBoard
AppSlug=clan-war-board
Project=ClanWarBoard
Service=clan-war-board
ManagedBy=Terraform
DeployedBy=HermesAgent
DeploymentTool=HermesAgent
IaC=Terraform
Repository=ItMeansBigMountain/clan-war-board-service
CostGuard=near-free
```

Also tag shared Terraform state with:

```text
Environment=shared
Purpose=TerraformState
```

## Service account pattern

Use GitHub OIDC for workflows; avoid GitHub client secrets. A local Azure service-principal login helper can exist outside repos for agent operations, but never print or commit its secret.

For Clan War Board, the non-human deploy identity is documented in the service docs and is used by GitHub OIDC. Roles were intentionally minimal for current use: Contributor on subscription plus Storage Blob Data Contributor on Terraform state storage.

## Verification sequence

After changes:

1. Parse workflow YAML.
2. Run service tests.
3. If Terraform changed: `terraform fmt -recursive -check` and `terraform validate`.
4. Commit and push child repo.
5. Wait for the GitHub Actions run matching the pushed SHA.
6. Verify live API and direct website routes.
7. Update/push the parent submodule pointer.
