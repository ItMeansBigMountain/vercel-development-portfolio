# Azure OIDC Environment Gates for GitHub Actions

Use this when operating GitHub Actions for Azure deployments.

## Key lesson

For Azure deployments, prefer GitHub OIDC + Azure federated identity credentials over storing long-lived `AZURE_CREDENTIALS` or `AZURE_CLIENT_SECRET` secrets.

## Environments as trust boundary

When a workflow job declares a GitHub Environment, Azure federated credentials can bind to that exact environment subject:

```text
repo:<OWNER>/<REPO>:environment:infra-dev
repo:<OWNER>/<REPO>:environment:app-dev
repo:<OWNER>/<REPO>:environment:infra-prod
repo:<OWNER>/<REPO>:environment:app-prod
```

This makes required reviewers/approval gates part of Azure auth rather than just a UI pause.

## Two workflows in one repo

Use separate workflow files and path filters:

```text
.github/workflows/infra-terraform.yml
.github/workflows/app-deploy.yml
```

Infra workflow:

- watches `infra/**`
- runs Terraform format/init/validate/plan
- applies only on `workflow_dispatch` with `apply=true`
- targets `infra-dev` or `infra-prod` environment

App workflow:

- watches `api/**`, `web/**`, `tests/**`
- tests and deploys app code only
- targets `app-dev` or `app-prod` environment

## Required workflow auth

```yaml
permissions:
  id-token: write
  contents: read

- uses: azure/login@v2
  with:
    client-id: ${{ vars.AZURE_CLIENT_ID }}
    tenant-id: ${{ vars.AZURE_TENANT_ID }}
    subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

These are variables, not secrets. Azure app/runtime secrets still belong in GitHub secrets or Azure Key Vault.

## Pitfalls

- Do not combine Terraform apply and app code deployment in one broad push-to-main workflow for services with approval gates. It blurs blast radius and makes it hard to approve infra separately from ordinary code changes.
- Add preflight checks for required GitHub variables before `azure/login`; missing variables surface as blank `ARM_CLIENT_ID` / `ARM_TENANT_ID` and `azure/login` errors like “Not all values are present”. A simple Bash loop over required vars gives a clearer failure.
- If a failed Terraform apply leaves `state blob is already locked`, verify no active workflow is still using it before force-unlocking; often the Azure blob lock clears shortly after the failed runner exits.
