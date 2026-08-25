# YouTube OAuth reauth callback exchange pattern

Use when the user sends Google OAuth localhost callback URLs for YouTube upload/read/analytics scopes.

## Scope set used for channel automation

Request all needed scopes at reauth time rather than incrementally layering stale tokens:

- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.force-ssl`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

Use `include_granted_scopes=false` and `prompt=consent` when replacing broken/missing scopes.

## Localhost callback exchange pitfall

If using `google-auth-oauthlib` to exchange a redirected `http://localhost:5000/?code=...&state=...` callback, set:

```bash
export OAUTHLIB_INSECURE_TRANSPORT=1
```

This is only for exchanging the local OAuth callback URI; it prevents `InsecureTransportError` for localhost redirects.

## Verification after exchange

After saving each token:

1. Run a token readiness check and verify `has_refresh_token=true`.
2. Verify the stored scopes exactly include upload, force-ssl, readonly, and analytics readonly.
3. Call `youtube.channels().list(part='id,snippet,statistics,status', mine=True)` and report the actual channel title/id.
4. Patch upload scripts to pass the intended token path explicitly; do not rely on a shared uploader default that might route uploads to the wrong channel.
5. Run an uploader dry-run using the target token before public uploads.

## Channel identity pitfall

A Google account can authenticate into the wrong YouTube channel/brand channel. Always verify channel title/id after exchange. If the token resolves to a different channel than expected, have the user reauth while selecting the correct YouTube channel in the consent flow.
