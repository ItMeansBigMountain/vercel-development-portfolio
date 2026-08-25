---
name: platform-device-integrations
description: "Use when operating specialized external integrations from Hermes: Yuanbao (元宝) group/DM workflows and Philips Hue/OpenHue smart-home control."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [integrations, yuanbao, 元宝, group, dm, mention, smart-home, hue, openhue, lights, automation]
    related_skills: []
prerequisites:
  commands: [openhue]
---

# Platform & Device Integrations

This is the umbrella for specialized non-code integrations that Hermes operates directly through gateway tools or local CLIs. Load it when the user asks to interact with Yuanbao groups/users or Philips Hue lights/rooms/scenes.

## Routing

| User intent | Section |
|---|---|
| `@mention` someone in Yuanbao, query a Pai/group, list/find Yuanbao members, send Yuanbao DM/private message | [Yuanbao group and DM workflows](#yuanbao-group-and-dm-workflows) |
| Turn lights on/off, dim a room, set Hue colors/scenes, schedule lighting | [Philips Hue via OpenHue](#philips-hue-via-openhue) |

---

## Yuanbao group and DM workflows

### Critical delivery model

**Your normal assistant reply is the message delivered to the group/user by the gateway.** Do not claim you cannot send messages or @mention users. Do not tell the user to do it manually. Reply with the exact concise text that should be sent.

When your reply includes `@nickname`, the Yuanbao gateway converts it to a real @mention that notifies the user.

### Available Yuanbao tools

| Tool | Use |
|---|---|
| `yb_query_group_info` | Query group name, owner, member count |
| `yb_query_group_members` | Find a user, list bots, list all members, or obtain exact nickname for @mention |
| `yb_send_dm` | Send a private/direct message (DM / 私信) to a user, optionally with media files |

### @Mention workflow

1. Extract `group_code` from the current chat id: `group:328306697` → `328306697`.
2. Call `yb_query_group_members` with `action="find"`, `name="<target name>"`, and `mention=true`.
3. Use the exact nickname from the response.
4. Reply with `@nickname <message>`; the gateway handles the actual mention.

Example user request: `帮我艾特元宝`

Tool call shape:
```json
{ "group_code": "328306697", "action": "find", "name": "元宝", "mention": true }
```

Final reply/message:
```text
@元宝 你好，有人找你！
```

Rules:
- Query members first; do not guess the nickname.
- Use `@nickname` with surrounding text naturally.
- Keep the final group message short and natural; do not explain the mechanism unless asked.

### Send DM / private message workflow

Use `yb_send_dm`, not the generic `send_message` tool, for Yuanbao DMs.

```json
{ "group_code": "535168412", "name": "用户aea3", "message": "hello" }
```

With media:
```json
{
  "group_code": "535168412",
  "name": "用户aea3",
  "message": "Here is the image",
  "media_files": [{"path": "/tmp/photo.jpg"}]
}
```

Rules:
- If `user_id` is already known, pass it directly to skip lookup.
- If multiple users match, ask the user to clarify.
- Supported media: images (`.jpg`, `.png`, `.gif`, `.webp`, `.bmp`) as image messages; other files as documents.

### Query group information and members

```json
yb_query_group_info({ "group_code": "328306697" })
yb_query_group_members({ "group_code": "328306697", "action": "list_bots" })
yb_query_group_members({ "group_code": "328306697", "action": "find", "name": "target", "mention": true })
```

Yuanbao groups are called `派 (Pai)`. Member roles may include `user`, `yuanbao_ai`, and `bot`.

---

## Philips Hue via OpenHue

Use the `openhue` CLI to control Philips Hue lights, rooms, and scenes through a Hue Bridge on the same local network.

### Prerequisites

Install OpenHue if missing:

```bash
# Linux pre-built binary
curl -sL https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 -o ~/.local/bin/openhue && chmod +x ~/.local/bin/openhue

# macOS
brew install openhue/cli/openhue-cli
```

First pairing requires pressing the Hue Bridge button. The bridge must be on the same local network as Hermes.

### Discover exact names first

Hue names are case-sensitive. Before acting on a room/light/scene name the user has not recently confirmed, list resources:

```bash
openhue get light
openhue get room
openhue get scene
```

### Control lights

```bash
# Turn on/off
openhue set light "Bedroom Lamp" --on
openhue set light "Bedroom Lamp" --off

# Brightness (0-100)
openhue set light "Bedroom Lamp" --on --brightness 50

# Color temperature, warm to cool: 153-500 mirek
openhue set light "Bedroom Lamp" --on --temperature 300

# Color by name or RGB hex, only for color-capable bulbs
openhue set light "Bedroom Lamp" --on --color red
openhue set light "Bedroom Lamp" --on --rgb "#FF5500"
```

### Control rooms

```bash
openhue set room "Bedroom" --off
openhue set room "Bedroom" --on --brightness 30
```

### Scenes

```bash
openhue set scene "Relax" --room "Bedroom"
openhue set scene "Concentrate" --room "Office"
```

### Common presets

```bash
# Bedtime: dim warm
openhue set room "Bedroom" --on --brightness 20 --temperature 450

# Work mode: bright cool
openhue set room "Office" --on --brightness 100 --temperature 250

# Movie mode: dim
openhue set room "Living Room" --on --brightness 10
```

### Notes and pitfalls

- Colors only work on color-capable bulbs; white-only bulbs support brightness and color temperature.
- For scheduled lighting, use Hermes cron jobs with an explicit, self-contained prompt or a small script invoking `openhue`.
- If pairing or discovery fails, verify the machine running Hermes is on the same LAN as the Hue Bridge and that the bridge authorization button was pressed during first setup.
