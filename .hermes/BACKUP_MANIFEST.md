# Hermes home backup manifest

Last backup: 2026-08-25T03:00:45Z
Source: /opt/data
Destination: /opt/data/HeRmEz/.hermes

This is a sanitized snapshot. Excluded intentionally:

- /opt/data/HeRmEz itself, to avoid recursive backups
- .env, .git-credentials, .gitconfig
- auth.json and auth.lock
- OAuth/keyring files
- files whose names contain secret, token, or credential
- private key material (*.pem, *.key, *.p12, *.pfx, id_rsa*, id_ed25519*)
- runtime locks, pids, sockets, common cache/build directories, session logs, local SDKs/CLIs, and generated installs
- downloaded package stores/SDKs (.nuget, .dotnet, node_modules, virtualenvs)
- Kanban scratch workspaces, sandboxes, generated media, and provider/deployment caches
- runtime databases, journals, corruption snapshots, and OAuth pending callback state
- nested .git directories

Future project folders should live under /opt/data/HeRmEz/projects.
