# Credential Model

- Use official OAuth wherever available; browser passwords are last-resort and MFA remains interactive.
- Platform app secrets belong in the deployment secret store, not frontend code or Git.
- User access/refresh tokens are encrypted at rest by the publishing host and never copied into prompts.
- Keep non-secret account metadata locally: platform, brand lane, expected account/user/channel ID, scopes, expiry, health, and last verification.
- Refresh proactively and atomically; if a platform rotates its refresh token, persist the returned replacement before considering refresh successful.
- Before every publish, query account identity and compare it with the expected destination.
- Reauthorization reports contain only platform/account label, missing scopes, and a safe authorization URL—never token values.
- The Hermes adapter receives only a narrow Postiz API credential stored under `/opt/data/secrets/social/postiz/` mode `600`.
- Revocation, deletion, and account disconnect actions require an explicit user request.
