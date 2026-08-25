# Split Infra/App GitHub Actions Path Filters

Use when one repo contains both Terraform infrastructure and deployable app code.

## Goal

Keep infrastructure and app deployments independent:

- Terraform infra workflow runs only for infra/IaC changes or manual dispatch.
- App deployment workflow runs only for API/frontend/deploy-config changes or manual dispatch.
- Test-only/doc-only changes should not deploy unless they are intentionally included in the path filters.

## Recommended workflow split

Infra workflow:

```yaml
on:
  pull_request:
    paths:
      - 'infra/**'
      - '.github/workflows/infra-terraform.yml'
  push:
    branches: [main]
    paths:
      - 'infra/**'
      - '.github/workflows/infra-terraform.yml'
  workflow_dispatch:
```

App workflow:

```yaml
on:
  pull_request:
    paths:
      - 'api/**'
      - 'web/**'
      - 'staticwebapp.config.json'
      - '.github/workflows/app-deploy.yml'
  push:
    branches: [main]
    paths:
      - 'api/**'
      - 'web/**'
      - 'staticwebapp.config.json'
      - '.github/workflows/app-deploy.yml'
  workflow_dispatch:
```

## Approval environments

Use separate GitHub environments for each lane:

```text
infra-dev
infra-prod
app-dev
app-prod
```

Federated credential subjects should match the environment names exactly:

```text
repo:<owner>/<repo>:environment:infra-dev
repo:<owner>/<repo>:environment:app-dev
repo:<owner>/<repo>:environment:infra-prod
repo:<owner>/<repo>:environment:app-prod
```

## Pitfalls

- Including `tests/**` in the app deployment path filter means changing tests can deploy the app. Include tests in CI-only workflows, not deploy workflows, unless the user explicitly wants test edits to redeploy.
- Changing a workflow file should trigger that workflow so syntax/preflight changes are exercised.
- Always add preflight checks for required GitHub variables before `azure/login`; blank `AZURE_CLIENT_ID`/`AZURE_TENANT_ID` errors are otherwise confusing.
