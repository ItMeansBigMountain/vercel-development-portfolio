# IBM Cloud CLI user-local install

Session-derived pattern for installing IBM Cloud CLI when `ibmcloud` is missing and the agent user lacks write access to `/usr/local/bin`.

## Trigger

- User wants an IBM Cloud action such as `ibmcloud login ...`.
- `command -v ibmcloud` fails.
- Environment is Linux x86_64 and `/opt/data` is user-writable.

## Install recipe

```bash
set -euo pipefail
mkdir -p /opt/data/bin /opt/data/ibmcloud-cli

meta=$(mktemp)
curl -fsSL https://download.clis.cloud.ibm.com/ibm-cloud-cli-metadata-dn/all_versions.json -o "$meta"

python3 - <<PY > /tmp/ibmcli_info.env
import json
j=json.load(open('$meta'))
latest=j[0]
b=latest['archives']['linux64']
print('VERSION='+latest['version'])
print('URL='+b['url'])
print('SHA256='+b.get('sha256_checksum',''))
PY

. /tmp/ibmcli_info.env
echo "Downloading IBM Cloud CLI $VERSION"
curl -fL "$URL" -o /tmp/IBM_Cloud_CLI_linux_amd64.tgz
printf '%s  %s\n' "$SHA256" /tmp/IBM_Cloud_CLI_linux_amd64.tgz | sha256sum -c -
tar -tzf /tmp/IBM_Cloud_CLI_linux_amd64.tgz | head -50

rm -rf /opt/data/ibmcloud-cli/IBM_Cloud_CLI
tar -xzf /tmp/IBM_Cloud_CLI_linux_amd64.tgz -C /opt/data/ibmcloud-cli
chmod +x /opt/data/ibmcloud-cli/IBM_Cloud_CLI/ibmcloud
ln -sf /opt/data/ibmcloud-cli/IBM_Cloud_CLI/ibmcloud /opt/data/bin/ibmcloud

/opt/data/bin/ibmcloud --version
/opt/data/bin/ibmcloud plugin list || true
```

## Why use metadata archives?

IBM's public Linux installer script fetches metadata and can install system-wide. In constrained agent environments, use the metadata JSON directly and select `archives.linux64`, which is a portable `.tgz` containing `IBM_Cloud_CLI/ibmcloud`. This avoids assuming sudo/root while still using IBM's current published version and checksum.

Metadata endpoints used:

- `https://download.clis.cloud.ibm.com/ibm-cloud-cli-metadata-dn/info.json`
- `https://download.clis.cloud.ibm.com/ibm-cloud-cli-metadata-dn/all_versions.json`

## Login notes

Check supported flags before login:

```bash
/opt/data/bin/ibmcloud login --help | sed -n '1,100p'
```

For a one-time passcode flow supplied by the user, run:

```bash
/opt/data/bin/ibmcloud login -a https://cloud.ibm.com -u passcode -p '<fresh-passcode>'
```

IBM CLI help warns that `-p` can expose passwords in shell history/processes. Treat pasted passcodes as sensitive; if the user pasted one before setup completed, ask for a fresh passcode rather than reusing the exposed one.

## Verification observed

A known-good verification sequence prints a version like:

```text
ibmcloud 2.43.0 (...)
Listing installed plug-ins...
Plugin Name   Version   Status   Private endpoints supported
```

The version will change over time; do not hard-code it except when recording what is already installed in memory.
