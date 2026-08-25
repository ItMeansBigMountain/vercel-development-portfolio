# MusicAI persistent YouTube auth pattern

## Problem observed

A Flask/Vercel MusicAI app can successfully store YouTube OAuth tokens in durable Postgres but still appear to "forget" YouTube login when the user later opens `/Dashboard`. The root cause is often not token storage; it is the browser/app session. If Flask uses its default non-permanent session cookie, the durable provider token remains in the DB but the browser loses the internal `musicai_user_id`, so the dashboard has no account ID to look up.

## Durable auth model

Use two layers:

1. **Browser app session** — stores only the internal MusicAI account ID and lightweight display metadata.
2. **Durable provider token store** — stores encrypted provider tokens, refresh tokens, scopes, expiry, and provider account IDs in Postgres/Neon.

The session should keep the user linked to the internal account for a reasonable period, while provider access tokens should be refreshed from the durable refresh token until Google revokes/invalidates it.

## Flask session setup

```py
from datetime import timedelta

application.secret_key = os.getenv('FLASK_SECRET_KEY')
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
    days=int(os.getenv('MUSICAI_SESSION_DAYS', '30'))
)
application.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
application.config['SESSION_COOKIE_SECURE'] = bool(os.getenv('VERCEL'))
```

When OAuth succeeds:

```py
def _set_musicai_session(user_id, provider=None, display_name=None):
    flask.session.permanent = True
    flask.session['musicai_user_id'] = user_id
    flask.session['user_id'] = user_id
    flask.session['musicai_login_at'] = time.time()
    if provider:
        flask.session['last_provider'] = provider
    if display_name:
        flask.session['username'] = display_name
```

## Store enough Google token metadata

On the YouTube callback, store:

```py
token_data = token_res.json()
token_data['expires_at'] = time.time() + token_data.get('expires_in', 3600)
token_data['provider_account_id'] = provider_account_id
```

Persist with `save_provider_token(..., expires_at=token_data['expires_at'])`.

## Refresh guard for dashboard and playlist routes

Every route that needs YouTube data should go through a token guard instead of directly reading `access_token`:

```py
def _refresh_youtube_token(refresh_token):
    response = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }, timeout=20)
    if response.status_code >= 400:
        return None
    return response.json()


def _ensure_youtube_token(user_id, youtube_token_data):
    access_token = youtube_token_data.get('access_token')
    expires_at = youtube_token_data.get('expires_at')
    if access_token and not is_token_expired(expires_at):
        return access_token, youtube_token_data

    refresh_token = youtube_token_data.get('refresh_token')
    refreshed = _refresh_youtube_token(refresh_token)
    if not refreshed:
        return None, youtube_token_data

    merged = dict(youtube_token_data)
    merged.update(refreshed)
    merged['refresh_token'] = refreshed.get('refresh_token') or refresh_token
    merged['expires_at'] = time.time() + refreshed.get('expires_in', 3600)
    token_store.save_provider_token(user_id, 'youtube_music', merged, expires_at=merged['expires_at'])
    return merged.get('access_token'), merged
```

Use it from `/Dashboard`, `/youtube/playlist/<playlist_id>/analysis`, and API equivalents.

## Verification

- Unit check: `_set_musicai_session(...)` makes `flask.session.permanent is True` and stores `musicai_user_id`.
- Unit check: expired YouTube token + valid refresh token calls `_refresh_youtube_token`, persists the merged result, and returns the new access token.
- Smoke check: unauthenticated `/Dashboard` still redirects to `/`, while an authenticated browser should keep the session across browser restarts until `MUSICAI_SESSION_DAYS` or revoked Google refresh token.

## Pitfalls

- Durable token storage alone does not keep a user logged in if there is no durable/resumable internal app session.
- Do not store provider access tokens directly in the Flask session; use the session to identify the internal account, then load encrypted provider tokens from durable storage.
- Google may not issue a new refresh token on every login. Preserve the existing refresh token when refreshing and when merging token payloads.
- If the fix changes cookie behavior, the current browser may need one fresh OAuth login to receive the new persistent cookie.
