# Azure Static Web Apps managed API + Cosmos production wiring

Use this pattern when a Free-tier Azure Static Web App hosts a managed Python API and Terraform already provisions Cosmos DB.

## Production wiring

1. Keep public web/read routes anonymous, but treat every write route as untrusted.
2. Add `azure-cosmos` to the API requirements.
3. Make storage mode explicit (`STORAGE_BACKEND=cosmos`); local tests may default to memory, but production health must never silently report memory as ready.
4. Configure backend application settings with `az staticwebapp appsettings set`. Settings become managed-API environment variables.
5. With GitHub OIDC, fetch the Cosmos endpoint/key at deploy time rather than storing the account key in GitHub:

```bash
cosmos_endpoint=$(az cosmosdb show --name "$AZURE_COSMOS_ACCOUNT_NAME" --resource-group "$AZURE_RESOURCE_GROUP" --query documentEndpoint -o tsv)
cosmos_key=$(az cosmosdb keys list --name "$AZURE_COSMOS_ACCOUNT_NAME" --resource-group "$AZURE_RESOURCE_GROUP" --type keys --query primaryMasterKey -o tsv)
az staticwebapp appsettings set --name "$AZURE_STATIC_WEB_APP_NAME" --setting-names STORAGE_BACKEND=cosmos COSMOS_ENDPOINT="$cosmos_endpoint" COSMOS_KEY="$cosmos_key" COSMOS_DATABASE="$COSMOS_DATABASE" COSMOS_CLANS_CONTAINER=clans >/dev/null
```

Managed identity + Cosmos data-plane RBAC is preferable when supported cleanly by the selected SWA managed-API environment; account-key injection is a fallback. Never expose the key to the plugin or website.

## API boundaries

- Generate a persistent installation UUID in the client.
- Hash installation IDs before persistence.
- Registration creates no leader authority by itself.
- Development role simulation must remain UI-only and must never be included in authority claims.
- Default member statistics to private.
- Sanitize public clan/member documents; never return internal installation hashes or auth/session fields.
- Use `Cache-Control: no-store` on writes, private responses, and errors.
- Keep worlds public only when that is the product policy; document this separately from player privacy.

## Deployment gate

Health must describe the actual backend, not a static marketing string:

```json
{"ok":true,"storage":"cosmos","productionReadyStorage":true}
```

After deployment, assert those exact dependency-readiness fields. Also test an invalid registration/write returns 4xx, public clan data contains no internal hashes, and an empty database stays truthfully empty—do not insert fake canary clans into production.

## Cost guardrails

Azure allows only one Cosmos Free Tier account per subscription. Do not define separate dev and prod accounts that both request free tier. Prefer a shared free-tier account with environment-separated databases/containers until scale or compliance justifies paid isolation.

## Important limitation

A public RuneLite client cannot cryptographically prove it is an untampered RuneLite client or that a claimed in-game rank is genuine. Installation tokens provide abuse control and continuity, not proof of leader status. High-impact leader writes need an explicit server-side capability/verification model, rate limiting, replay protection, idempotency, and audit records.
