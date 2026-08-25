# MusicAI SoundCloud OAuth 2.1 + PKCE notes

Use this when enabling SoundCloud as a MusicAI provider.

## SoundCloud API facts

- Developer portal: `https://developers.soundcloud.com/`
- API base URL: `https://api.soundcloud.com`
- OAuth/auth base URL: `https://secure.soundcloud.com`
- Authorization endpoint: `https://secure.soundcloud.com/authorize`
- Token endpoint: `https://secure.soundcloud.com/oauth/token`
- Auth method: OAuth 2.1 with PKCE. Include `code_challenge` and `code_challenge_method=S256` on authorize, then include `code_verifier` when exchanging the authorization code.
- API request auth header after login: `Authorization: OAuth ACCESS_TOKEN`.
- SoundCloud docs currently indicate app/API-key registration requires a SoundCloud account with Artist Pro.

## MusicAI callback URLs

Production callback:

```txt
https://musicai-rouge.vercel.app/providers/soundcloud/callback
```

Local callback:

```txt
http://localhost:5000/providers/soundcloud/callback
```

## MusicAI environment variables

```txt
SOUNDCLOUD_CLIENT_ID=...
SOUNDCLOUD_CLIENT_SECRET=...
SOUNDCLOUD_CALLBACK_URL=https://musicai-rouge.vercel.app/providers/soundcloud/callback
```

Set the same callback URI in the SoundCloud app dashboard and Vercel env. The redirect URI must match exactly.

## Implementation pattern

1. On `/providers/soundcloud/connect`, generate a random PKCE `code_verifier`, store it in the Flask session, and send the SHA-256/base64url `code_challenge` to SoundCloud.
2. Include `client_id`, `redirect_uri`, `response_type=code`, `code_challenge`, `code_challenge_method=S256`, and CSRF `state` in the authorization URL.
3. On `/providers/soundcloud/callback`, validate state, retrieve the saved `code_verifier`, then POST form-encoded data to `/oauth/token` with `grant_type=authorization_code`, `client_id`, `client_secret`, `redirect_uri`, `code_verifier`, and `code`.
4. Fetch the profile from `https://api.soundcloud.com/me` with `Authorization: OAuth <access_token>`.
5. Link the SoundCloud provider identity into the existing one-account/multi-OAuth account via `token_store.resolve_account(...)`, then save encrypted provider tokens.

## Verification

Before real credentials exist, test only redirect construction:

- `/providers/soundcloud/connect` should return a 302 to `https://secure.soundcloud.com/authorize?...`.
- The `Location` URL should contain `code_challenge=`, `code_challenge_method=S256`, `state=`, and the exact URL-encoded `redirect_uri`.
- Live `/healthz` should report `providers.soundcloud: true` only after both `SOUNDCLOUD_CLIENT_ID` and `SOUNDCLOUD_CLIENT_SECRET` are configured and redeployed.

## Pitfalls

- Do not implement SoundCloud as old OAuth 2.0 without PKCE; current SoundCloud OAuth 2.1 docs require PKCE for authorization-code exchange.
- Do not confuse SoundCloud public API/client-credentials access with user-library access. MusicAI's one-account dashboard needs user OAuth.
- Do not commit or print client secrets. If secrets are pasted into chat, treat them as exposed and recommend rotation after setup.
