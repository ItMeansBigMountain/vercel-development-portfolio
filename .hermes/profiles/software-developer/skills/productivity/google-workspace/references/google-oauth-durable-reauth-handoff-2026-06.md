# Google OAuth reauth durability and persistent handoff — 2026-06

Use this when the user asks for all Google auth URLs, asks that auth "never expire," or wants a persistent file/workflow for reauth.

## What to say about expiration

Authoritative Google OAuth guidance: request offline access and save refresh tokens in secure long-term storage, but refresh tokens are not literally guaranteed to live forever. They can still expire or be revoked due to user revocation, security events, testing-mode limits, inactivity, password changes involving Gmail scopes, or Google policy.

So phrase the target as: **long-lived + monitored + easy to regenerate**, not "impossible to expire."

## URL generation pattern

Use the unified helper and generate one fresh URL per lane/profile. It stores isolated pending PKCE state per profile/channel and uses `access_type=offline` + `prompt=consent`.

```bash
python3 /opt/data/scripts/google_reauth_workflow.py inventory
python3 /opt/data/scripts/google_reauth_workflow.py workspace-auth-url personal-secondary
python3 /opt/data/scripts/google_reauth_workflow.py workspace-auth-url trapiistan
python3 /opt/data/scripts/google_reauth_workflow.py workspace-auth-url classicalechos
python3 /opt/data/scripts/google_reauth_workflow.py workspace-auth-url burner
python3 /opt/data/scripts/google_reauth_workflow.py workspace-auth-url personal-main
python3 /opt/data/scripts/google_reauth_workflow.py youtube-auth-url trapiistan
python3 /opt/data/scripts/google_reauth_workflow.py youtube-auth-url classicalechos
```

## Persistent handoff file

When producing a batch of URLs, save a non-secret handoff under the workspace ops area, currently:

```text
/opt/data/HeRmEz/projects/_ops/google-oauth-reauth-current.md
```

Include:

- generated timestamp;
- expiration/durability note above;
- each URL grouped by profile/channel;
- exact callback prefix format;
- find/regenerate/exchange/verify commands.

## Callback handling

Tell the user localhost failure is expected. They should return each full address-bar URL with its prefix, for example:

```text
workspace:trapiistan: http://localhost:1/?code=...
youtube:trapiistan: http://localhost:5000/?code=...
```

Exchange and verify:

```bash
python3 /opt/data/scripts/google_reauth_workflow.py workspace-exchange <profile> '<full localhost URL>'
python3 /opt/data/scripts/google_reauth_workflow.py youtube-exchange <profile> '<full localhost URL>'
python3 /opt/data/scripts/google_reauth_workflow.py verify workspace <profile>
python3 /opt/data/scripts/google_reauth_workflow.py verify youtube <profile>
```

Never paste token JSON, refresh tokens, access tokens, client secrets, private keys, or full credential files into chat or docs.
