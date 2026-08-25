# Email sorting agent + particle-video style notes

Use this reference when operating the user's Hermes-level email manager and newsletter-to-video workflow.

## Email sorting ownership model

The user wants a designated email sorting agent that runs before the morning report and keeps the visible Inbox clean while preserving content sources for later use.

Workflow:

1. Scan all profile-scoped Google accounts with Gmail API.
2. Match known newsletter/source senders: TLDR, Daily Stoic, Kino Body.
3. Apply durable Gmail labels/folders such as:
   - `Hermes/Source/TLDR`
   - `Hermes/Source/Daily Stoic`
   - `Hermes/Source/Kino Body`
   - `Hermes/Source/Newsletter Queue`
4. Remove matched source newsletters from `INBOX` after confident classification.
5. Do **not** trash/delete newsletter source emails until their one-email→one-video output has a verified YouTube `video_id`.
6. Keep important/account/security/billing/human emails visible for the morning operator report.

Local implementation from the session:

- Sorter script: `/opt/data/scripts/email_sorting_agent.py`
- Silent cron wrapper: `/opt/data/scripts/email_sorting_agent_apply.sh`
- Morning cron: `Morning email sorting agent`, scheduled before the operator report.

Future agents should treat this as Hermes operating behavior, not as a project-specific app email rule.

## ElevenLabs key alias

The user's environment may expose the ElevenLabs key as `EllevenLabsKey` — intentionally spelled with two leading Ls. Video/TTS scripts should check this in addition to conventional names:

- `ELEVENLABS_API_KEY`
- `XI_API_KEY`
- `ELEVEN_API_KEY`
- `EllevenLabsKey`

A key being present is not sufficient: run a live `/v1/user` or TTS probe before uploading.

## Snapshot-inspired visual style

The user supplied Shorts screenshots as style inspiration. Encode this into prompts/storyboards for Daily Stoic, Kino Body, and TLDR videos:

- Vertical 9:16 composition.
- Black/near-black background with bright white forms.
- Monochrome particle/digital-sand visuals.
- Lone figure, tunnel/void, rain-like human silhouette, emergence/transformation.
- Large bold white hook text near the top.
- Short centered caption over the visual; never paragraph captions.
- Rapid cuts: roughly 1.5–3 seconds per shot.
- Mood: dark, cinematic, masculine, intense, motivational.

Prompt vocabulary that works well:

`monochrome`, `high contrast`, `particle storm`, `digital sand`, `white light points`, `void`, `tunnel`, `lone warrior silhouette`, `emergence`, `transformation`, `disciplined solitude`, `rain of light`, `black background`.

## Newsletter lanes

- **Daily Stoic**: turn the actual lesson into a Stoic reflection. Visuals: lone dawn runner, notebook, ancient statue fragments, disciplined solitude, cold street walk, particle silhouette becoming upright.
- **Kino Body**: testosterone, men's health, warrior fitness, getting shredded while living well. Visuals: gym shadows, chalk/sweat, warrior silhouette, body recomposition, morning sunlight, disciplined meal prep.
- **TLDR**: bleeding-edge tech/AI/dev/security/news signals. Visuals: data storm, code tunnel, security operations center, AI agents, payments rails, futuristic city/workflow shots.

## Pitfalls

- Do not combine several newsletters into one generic trend clip.
- Do not upload static text-slide placeholders.
- Do not disclose AI/automation/source email/ElevenLabs/pipeline details in public metadata.
- Do not delete source newsletters after sorting; deletion only happens after verified upload.
