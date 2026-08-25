---
name: cloud-provider-cli-setup
description: "Use when installing, configuring, or verifying cloud provider CLIs in constrained agent environments without assuming sudo/root access. Covers user-local installs, checksum verification, PATH handling, and secure credential/passcode workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [cloud, cli, setup, credentials, devops]
    related_skills: [github-auth, vercel-app-deployments]
---

# Cloud Provider CLI Setup

## Overview

Use this skill when a task requires a cloud provider command-line tool that is missing, outdated, or not on PATH. The default approach is to install into a user-writable location, verify the binary, and then run the requested cloud action with the least credential exposure possible.

This skill is intentionally provider-agnostic. Store provider-specific details in `references/cloud-provider-cli-setup/` so the umbrella stays class-level and future sessions can add AWS/GCP/Azure/IBM quirks without creating narrow one-off skills.

Provider references:

- `references/cloud-provider-cli-setup/ibmcloud-user-local-install.md` — IBM Cloud CLI install from metadata archives without sudo, including checksum verification and passcode login notes.
- `references/cloud-provider-cli-setup/ibm-watson-nlu-credentials.md` — IBM Watson NLU credential discovery, redacted service-key behavior, creating a usable service API key, and verifying it with a harmless analyze call.
- `references/cloud-provider-cli-setup/ibm-watson-nlu-app-integration.md` — Pattern for repairing multiple app integrations that use Watson NLU/Tone Analyzer-style wrappers, including credential fallback, compatibility helpers, smoke tests, and deployment env-var updates.

## When to Use

- User asks to run a cloud CLI command and the CLI is missing or unconfigured.
- User asks to set up a provider CLI before providing credentials.
- Environment lacks root/sudo access or `/usr/local/bin` is not writable.
- A provider install script assumes system-wide writes, but an archive or portable binary is available.
- You need to verify a provider CLI install before performing account operations.

Don't use for:

- Application deployment once the provider CLI is already installed and authenticated; use the deployment-specific skill.
- GitHub authentication; use `github-auth`.
- Hermes Agent configuration; use `hermes-agent`.

## Secure Setup Workflow

1. **Check prerequisites first.**
   - OS and architecture: `uname -a`
   - Tool availability: `command -v <cli>`, `command -v curl`, `command -v tar`, etc.
   - Write access: prefer `$HOME/bin`, `/opt/data/bin`, or another user-owned directory.

2. **Prefer user-local installation when root is unavailable.**
   - Create a durable bin directory such as `/opt/data/bin` or `$HOME/bin`.
   - Extract provider archives under a user-owned directory such as `/opt/data/<provider>-cli/`.
   - Symlink the CLI into the bin directory.
   - If the bin directory is not on PATH, invoke by absolute path and tell the user.

3. **Verify downloads.**
   - Use provider metadata when available.
   - Verify SHA-256 checksums before extraction or execution.
   - Inspect archive contents (`tar -tzf`, `unzip -l`) before placing files.

4. **Verify installation.**
   - Run `<absolute-cli-path> --version`.
   - Run a harmless inspection command such as plugin/list/help/status if available.

5. **Handle credentials carefully.**
   - Do not ask users to paste long-lived secrets unless necessary.
   - If a user pastes a one-time code or passcode publicly, treat it as exposed and ask for a fresh one.
   - Avoid command-line password flags for long-lived passwords because shell history and process lists can expose them.
   - For one-time passcodes, use them promptly and avoid echoing them back.
   - If provider CLI output redacts existing API keys, do not present redacted values as usable; create a new key into a protected local file and verify it.

6. **Complete the original requested action after setup.**
   - If the user asked to set up first and provide credentials later, stop after verified install and give the exact next command form with a placeholder.
   - Once credentials are supplied, run the login/action immediately using the verified CLI path.

## User-Local Install Pattern

```bash
set -euo pipefail
mkdir -p /opt/data/bin /opt/data/<provider>-cli
# download archive to /tmp
# verify checksum
# extract under /opt/data/<provider>-cli
# symlink /opt/data/bin/<cli> -> extracted binary
/opt/data/bin/<cli> --version
```

If `/opt/data/bin` is not on PATH and profile files are protected, do not force PATH changes. Use the absolute path for subsequent commands and state that clearly.

## Credential Hygiene

- Treat passcodes, API keys, and tokens as sensitive even when the user shares them casually.
- Warn when a previously shared code should be considered exposed.
- Prefer `--apikey @file` or environment-variable routes for long-lived credentials when supported.
- Use `--help` to confirm the provider's supported secure auth flags before inventing syntax.
- Never save tokens/passcodes in memory or skills.

## Common Pitfalls

1. **Running install scripts blindly.** Install scripts often attempt system-wide writes. Read or inspect the script first, or use the archive path if root is unavailable.

2. **Capturing environment-specific failure as a durable rule.** `command not found`, unwritable `/usr/local/bin`, or missing PATH entries are setup state, not permanent limitations. Capture the install/config fix instead.

3. **Forgetting PATH reality.** Verifying `/opt/data/bin/<cli>` works does not mean `command -v <cli>` will work in later shells. Record or communicate the absolute path when PATH is not updated.

4. **Using stale one-time credentials.** If a passcode was pasted before the CLI was ready, assume it should be replaced before login.

5. **Skipping verification.** A successful download/extract is not enough. Always run the CLI version command and at least one harmless command.

## Verification Checklist

- [ ] OS/architecture and required tools checked.
- [ ] Install target is user-writable or user approved system-level writes.
- [ ] Download source came from provider metadata/docs.
- [ ] Checksum verified where available.
- [ ] Binary path and version verified.
- [ ] PATH/absolute-path behavior communicated.
- [ ] Credentials were not stored, echoed unnecessarily, or added to memory.
- [ ] Original requested cloud action is completed or the user has the exact next command form.
