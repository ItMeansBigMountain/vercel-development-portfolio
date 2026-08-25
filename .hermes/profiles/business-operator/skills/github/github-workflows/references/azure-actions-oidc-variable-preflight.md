# Azure GitHub Actions OIDC variable preflight

Use when an Azure GitHub Actions workflow fails at `azure/login` with missing values, or when bootstrapping repo/environment variables for Azure OIDC.

## Recognize the failure

Typical log:

```text
Using auth-type: SERVICE_PRINCIPAL. Not all values are present.
Ensure 'client-id' and 'tenant-id' are supplied.
ARM_CLIENT_ID:
ARM_TENANT_ID:
ARM_SUBSCRIPTION_ID:
```

This usually means the workflow is structurally correct but required GitHub variables are missing or scoped to the wrong environment.

## Check current GitHub state

Use the GitHub API/gh to inspect:

- repo variables,
- environment variables,
- environments.

Required environments for split Azure deployments commonly look like:

```text
infra-dev
app-dev
infra-prod
app-prod
```

Required variables for Terraform infra:

```text
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
TFSTATE_RESOURCE_GROUP
TFSTATE_STORAGE_ACCOUNT
TFSTATE_CONTAINER
```

Required variables for app deploy:

```text
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
AZURE_RESOURCE_GROUP
AZURE_FUNCTIONAPP_NAME
AZURE_STATIC_WEB_APP_NAME
```

## Recommended workflow guard

Add a preflight step before `azure/login` so the failure is explicit:

```yaml
- name: Preflight required GitHub variables
  shell: bash
  env:
    AZURE_CLIENT_ID: ${{ vars.AZURE_CLIENT_ID }}
    AZURE_TENANT_ID: ${{ vars.AZURE_TENANT_ID }}
    AZURE_SUBSCRIPTION_ID: ${{ vars.AZURE_SUBSCRIPTION_ID }}
  run: |
    missing=0
    for name in AZURE_CLIENT_ID AZURE_TENANT_ID AZURE_SUBSCRIPTION_ID; do
      if [ -z "${!name}" ]; then
        echo "::error::$name is not set. Configure it as a repository/environment variable before running this workflow."
        missing=1
      fi
    done
    exit "$missing"
```

Extend the variable list for Terraform state or app deploy names as needed.

## Bootstrap sequence

1. Create GitHub environments first so OIDC subjects can target them.
2. Use Azure CLI after device-code login to create an Entra app/service principal.
3. Add one federated credential per environment subject:

```text
repo:<OWNER>/<REPO>:environment:infra-dev
repo:<OWNER>/<REPO>:environment:app-dev
repo:<OWNER>/<REPO>:environment:infra-prod
repo:<OWNER>/<REPO>:environment:app-prod
```

4. Set GitHub variables.
5. Re-run the workflow.

## Pitfalls

- Environment-scoped variables are only visible to jobs that declare that exact `environment:`.
- Repo variables can be easier during bootstrap; environment variables provide tighter scoping later.
- `azure/login` error text mentions service principal even for OIDC because the OIDC flow still uses an Entra app/client ID.
- Node 20 deprecation warnings are usually non-fatal; fix explicit `node-version: '20'` when present, but missing Azure variables are the real blocker in this failure mode.
