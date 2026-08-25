# Azure GitHub Actions pipeline preflight and bootstrap lessons

Use when setting up Azure Terraform/app deployment workflows with GitHub OIDC and environment approval gates.

## Symptom

`azure/login@v2` fails with:

```text
Using auth-type: SERVICE_PRINCIPAL. Not all values are present. Ensure 'client-id' and 'tenant-id' are supplied.
```

The workflow log shows empty values:

```text
ARM_CLIENT_ID:
ARM_TENANT_ID:
ARM_SUBSCRIPTION_ID:
```

## Cause

The workflow is structurally valid, but GitHub repository/environment variables have not been bootstrapped yet. This is common before the first `pim up` Azure device-code login and OIDC setup.

Required infra variables:

```text
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
TFSTATE_RESOURCE_GROUP
TFSTATE_STORAGE_ACCOUNT
TFSTATE_CONTAINER
```

Required app deploy variables after infra exists:

```text
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
AZURE_RESOURCE_GROUP
AZURE_FUNCTIONAPP_NAME
AZURE_STATIC_WEB_APP_NAME
```

## Fix pattern

Add an explicit preflight step before `azure/login` so failures are actionable:

```yaml
- name: Preflight required GitHub variables
  shell: bash
  env:
    AZURE_CLIENT_ID: ${{ vars.AZURE_CLIENT_ID }}
    AZURE_TENANT_ID: ${{ vars.AZURE_TENANT_ID }}
    AZURE_SUBSCRIPTION_ID: ${{ vars.AZURE_SUBSCRIPTION_ID }}
    TFSTATE_RESOURCE_GROUP: ${{ vars.TFSTATE_RESOURCE_GROUP }}
    TFSTATE_STORAGE_ACCOUNT: ${{ vars.TFSTATE_STORAGE_ACCOUNT }}
    TFSTATE_CONTAINER: ${{ vars.TFSTATE_CONTAINER }}
  run: |
    missing=0
    for name in AZURE_CLIENT_ID AZURE_TENANT_ID AZURE_SUBSCRIPTION_ID TFSTATE_RESOURCE_GROUP TFSTATE_STORAGE_ACCOUNT TFSTATE_CONTAINER; do
      if [ -z "${!name}" ]; then
        echo "::error::$name is not set. Configure it as a repository/environment variable before running this workflow."
        missing=1
      fi
    done
    if [ "$missing" -ne 0 ]; then
      echo "See docs/github-actions-setup.md for the bootstrap sequence."
      exit 1
    fi
```

For app deployment, check `AZURE_RESOURCE_GROUP` and `AZURE_FUNCTIONAPP_NAME` too.

## Bootstrap sequence

1. User says `pim up`.
2. Run `az login --use-device-code` and give them the device URL/code.
3. Create Terraform state RG/storage/container.
4. Create Entra app/service principal.
5. Add federated credentials for each GitHub environment subject.
6. Create GitHub environments (`infra-dev`, `app-dev`, `infra-prod`, `app-prod`).
7. Write non-secret GitHub variables.
8. Run infra workflow, then set app variables from Terraform outputs.

## Node runner note

GitHub began deprecating Node 20 actions/runtime warnings. When explicitly setting Node in workflows, prefer current LTS/supported versions (e.g. Node 24 where available) instead of preserving Node 20 unless a dependency requires it.
