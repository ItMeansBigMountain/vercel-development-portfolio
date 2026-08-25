# Azure CLI device-code bootstrap from Hermes

Use when the user says `pim up` or asks Hermes to authenticate to Azure for Terraform/GitHub Actions bootstrap.

## Preferred flow

1. Ensure Azure CLI is available in the Hermes environment.
2. Start device-code login in a PTY so the code is emitted promptly:

```bash
/opt/data/home/.local/share/uv/tools/azure-cli/bin/python -m azure.cli login --use-device-code --allow-no-subscriptions
```

If `--allow-no-subscriptions` crashes during subscription selection, retry without it:

```bash
/opt/data/home/.local/share/uv/tools/azure-cli/bin/python -m azure.cli login --use-device-code
```

3. Give the user exactly the URL and code shown, e.g. `https://login.microsoft.com/device` plus the code.
4. Keep the background process running while the user authenticates.
5. After it exits successfully, verify account state:

```bash
az account list -o table
az account show --query '{tenantId:tenantId, subscriptionId:id, name:name}' -o table
```

## uv install pattern

If Azure CLI is not installed and `uv` is available, install a modern CLI explicitly. Do not rely on the package's unpinned default resolver, which may install an obsolete Azure CLI incompatible with modern Python.

```bash
uv python install 3.12
uv tool install 'azure-cli==2.76.0' --python 3.12 --with 'setuptools<81' --prerelease=allow --force
```

Then invoke the module directly if the `az` wrapper points at the wrong interpreter:

```bash
/opt/data/home/.local/share/uv/tools/azure-cli/bin/python -m azure.cli --version
/opt/data/home/.local/share/uv/tools/azure-cli/bin/python -m azure.cli login --use-device-code
```

## Pitfalls

- `az` wrapper scripts may resolve to `/usr/bin/python` or another interpreter without the `azure` package. If so, invoke the uv tool Python directly.
- Old `azure-cli==2.0.67` can fail on modern Python with `time.clock` errors. Pin a current Azure CLI version instead of debugging that legacy install.
- Some Azure CLI versions require `--prerelease=allow` because they depend on prerelease Azure packages.
- Device-code login may need `pty=true`; without a PTY, the login prompt/code can be delayed or not surfaced.
- Do not save or print tokens. Device codes are temporary and safe to show to the user for the login flow.
