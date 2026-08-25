# Profile-scoped Gateway Routing Notes

Use this when a user asks whether one gateway conversation/channel can use a specialist Hermes profile while other conversations keep the default profile.

## Core model

Hermes profiles isolate config, secrets, memory, skills, sessions, and cron state. A gateway turn only runs inside a non-default profile when the inbound `SessionSource.profile` is stamped and `gateway.multiplex_profiles` is enabled. Otherwise the gateway uses the active/default profile.

Known routing mechanisms in Hermes gateway code:

- `gateway.multiplex_profiles: true` enables profile-scoped session keys and per-turn profile runtime scope.
- HTTP/webhook/API-style entrypoints can route via `/p/<profile>/...` URL prefixes.
- Secondary profile platform adapters can stamp inbound events with their owning profile.
- Same-platform credential collisions are refused: two profiles should not poll the same Discord bot token concurrently.

## Discord-specific operational guidance

Do not assume Discord has built-in per-channel profile routing. If the user asks for `#security-redteam` to use a redteam profile and other channels to use default, the durable pattern is:

1. Keep the normal/default Discord bot on the default profile.
2. Configure a separate Discord bot token under the redteam profile; do not reuse the default bot token.
3. Enable profile multiplexing on the gateway if using one multiplexer process, or run the specialist gateway/profile directly if the environment uses foreground/container gateways.
4. Restrict the redteam bot to the redteam/security channel with `discord.allowed_channels <channel_id>` and/or Discord server permissions.
5. Invite the redteam bot to the server/channel only after config is in place.
6. Verify the redteam profile uses its intended provider/model, and verify the default profile is unchanged.

A session-level `/model` switch can change the model for a chat if the model is available in that profile, but it is not full profile isolation: memory, skills, config, and credentials remain those of the current profile.

### Practical setup sequence for a separate Discord bot

Use these commands as a template, substituting profile/channel values and never echoing secrets back to chat:

```bash
# Store the token in the specialist profile env/config scope. Prefer user-side paste or a secure secret path.
hermes -p <profile> config set DISCORD_BOT_TOKEN '<token>'

# Limit where that bot can respond. Use the target channel id, not the old/default home channel.
hermes -p <profile> config set discord.allowed_channels <channel_id>
hermes -p <profile> config set discord.require_mention false   # only if the channel is tightly scoped
hermes -p <profile> config set discord.auto_thread false
hermes -p <profile> config set discord.reply_to_mode off

# In Docker/container installs, `gateway start` may report service start is not applicable.
# Use a tracked foreground process instead, or the container's normal supervisor if configured.
hermes -p <profile> gateway run
```

Invite URL shape:

```text
https://discord.com/oauth2/authorize?client_id=<client_id>&permissions=117760&integration_type=0&scope=bot%20applications.commands
```

If using a Discord bot token, the client/application id is typically the first dot-separated token segment decoded from base64url as an integer. Do not print or store the full token in notes. If the token was pasted into chat, tell the user to rotate it after the bot is confirmed working, then update the profile env with the new token.

Expected pre-invite log/status: the gateway may connect but fail to send with `403 Forbidden: Missing Access` until the bot is invited and granted channel access. Treat that as an access/invite blocker, not a model/profile failure.

## Verification checklist

- `hermes profile list` shows the specialist profile and default profile separately.
- Specialist profile config references secrets by env var name only, e.g. `${VENICE_API_KEY}`; never print secret values.
- A live smoke test proves the specialist profile can answer with its configured provider/model.
- Default profile still reports its normal provider/model after the specialist setup.
- Gateway logs/status show served profiles when multiplexing is used.
