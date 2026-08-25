# Newsletter batch upload: natural storytelling, semantic visuals, and transient retry

Use this when processing the user's fareed320/personal-secondary newsletter backlog into public Sosai/Trapiistan YouTube uploads.

## User correction captured

The user explicitly wants each newsletter video to feel like a charismatic person telling a story around one topic, not a rigid outline. The script should flow naturally and avoid sounding like sections or a lecture.

Apply this before rendering/uploading:

- One email = one video = one core topic/story.
- Use the actual newsletter facts as the core content, not as loose receipts for the assistant's own take.
- Do **not** add advice, self-improvement morals, "build one proof today" style calls-to-action, or unrelated opinions unless the source email itself says that.
- Relay the newsletter message in a personified human voice: conversational, expressive, and natural, but still faithful to the source.
- Avoid spoken outline markers such as `intro`, `here are the three points`, `operator angle`, `in conclusion`, or overly repeated beat labels.
- Captions can be punchy, but the voiceover should sound like one monologue.
- Match tone to topic: AI/tech can be witty, security urgent/news-anchor tense, finance skeptical/follow-the-money, Stoic/fitness grounded — but never drift away from the newsletter content.

## Visual correction captured

The user emphasized: use multiple background images/videos, and make them actually align with what the script is saying — not random stock footage.

Implementation requirements:

- Derive visual queries per scene from the newsletter subject/body and the narration beat.
- Include company/product/category terms where useful, plus mood/context terms.
- Mix multiple assets: stock videos, photos, product/category imagery, dashboards, security ops, finance/payment scenes, gym/discipline/stoic scenes, etc.
- Preserve `visual_manifest.json` for QA.
- Do not treat a video as final if it is mostly unrelated generic office/laptop footage or one repeated background.

## Operational pattern that worked

- Process eligible newsletters in batches, then re-run discovery until `remaining_count` is zero.
- Use the Hermes venv Python when running the project pipeline if system Python lacks Google libraries.
- Each successful upload must return `status: UPLOADED`, a `video_id`, and a public URL before trashing the source Gmail message.
- If Google TTS returns transient 429/500/502/503/504, retry with backoff. The durable lesson is the retry pattern, not that TTS is broken.
- After a transient TTS failure, retry the exact failed `--message <gmail_id>` after patching/adding retries.

## Verification checklist

- `py_compile` passes for edited renderer scripts.
- `ffprobe` confirms 1080x1920 and audio stream.
- Upload log contains source Gmail id and YouTube video id.
- Gmail discovery returns zero remaining eligible source emails when the backlog target is complete.
