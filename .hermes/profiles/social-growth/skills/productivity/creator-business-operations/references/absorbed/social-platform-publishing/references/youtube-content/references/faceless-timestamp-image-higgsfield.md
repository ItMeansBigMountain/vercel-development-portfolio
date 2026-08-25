# Faceless Timestamp-to-Image Video Workflow (Hermes + Higgsfield)

Use this when a user wants to reproduce the common Claude Code + Higgsfield faceless YouTube workflow, but with Hermes as the agent.

## Workflow shape

1. Human records the voiceover first. The referenced creator recommends human narration over AI voice to reduce demonetization/platform-quality risk.
2. User sends audio through a transcription tool such as Turboscribe and exports a transcript with timestamps.
3. Hermes parses each timestamped line into one image prompt.
4. Prompts must repeat the style constraint every time for consistency:
   - simple beginner-style MS Paint drawing
   - white background
   - black outline
   - minimal flat colors
   - slightly rough/human-drawn
   - no photorealism/cinematic realism/detailed shading
   - avoid text in-image unless required
5. Higgsfield generates one image per timestamp.
6. Save each image locally with a timestamp filename such as `0.00.png`, `7.00.png`, `14.50.png`.
7. In an editor, place each image at its timestamp and stretch until the next image begins. Optionally render the slideshow automatically with ffmpeg.

## Hermes implementation pattern

Project scaffold:

```text
videos/YYYY-MM-DD-short-title/
  audio/voiceover.wav
  transcript/timestamped.txt
  prompts/image_prompts.jsonl
  images/0.00.png
  exports/final.mp4
```

Useful scripts to create in a project:

- `create_video_workspace.py` — create the folder tree above.
- `build_image_prompts.py` — parse timestamped transcript lines into JSONL prompts.
- `generate_higgsfield_images.py` — run `higgsfield generate create <model> --prompt ... --wait --json`, download image URLs, rename to timestamps.
- `render_timestamp_slideshow.py` — optional ffmpeg concat render from timestamp-named images + voiceover.

## Higgsfield setup notes

The public Higgsfield CLI setup is:

```bash
npm install -g @higgsfield/cli
higgsfield auth login
npx skills add higgsfield-ai/skills
```

If global npm install is not writable, install under a user prefix instead:

```bash
mkdir -p ~/.local
npm install -g @higgsfield/cli --prefix ~/.local
~/.local/bin/higgsfield auth login
```

For Hermes project-local skill installation, `npx skills add higgsfield-ai/skills --skill higgsfield-generate --project --copy -y --full-depth` copies the Higgsfield generate skill into `.hermes/skills/` and `.agents/skills/`.

## Pitfalls

- YouTube transcript extraction from cloud/VPS IPs may be blocked. If the user already pasted the guide or transcript summary, proceed from that rather than requiring transcript fetch.
- Real Higgsfield generation requires user authentication; do not claim generation worked if `higgsfield auth token` or `higgsfield account status` says not authenticated.
- Preserve source attribution and avoid lazy reuploads; this workflow is for generating original visuals from a user's own script/voiceover.
- Do a dry run of the parser/generation command before spending Higgsfield credits.
