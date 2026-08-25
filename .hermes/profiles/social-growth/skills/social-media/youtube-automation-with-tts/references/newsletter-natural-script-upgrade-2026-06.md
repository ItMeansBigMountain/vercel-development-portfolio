# Newsletter video natural-script upgrade — 2026-06

Use this when the user asks to turn newsletter emails into videos and complains that scripts are not catchy or natural enough.

## User correction

The user wants **one video per newsletter email**, but the spoken script should sound like a catchy, natural host monologue — not a rigid outline, lecture card, or templated operator summary.

## Durable scripting rules

- Hook immediately with the strangest, strongest, or most visual idea from the email.
- Keep the narration as one continuous story. Captions can be punchy labels, but the voiceover should not announce sections.
- Avoid generic recurring phrases such as `the signal`, `operator angle`, `move first`, `in conclusion`, or unrelated motivational lines.
- Do not append generic advice/morals unless the newsletter itself says it.
- Use actual newsletter facts as receipts; strip citation artifacts, sender mechanics, headings, sponsor boilerplate, and emoji clutter from narration.
- Match the topic voice:
  - AI/tech: energetic plot-twist / workflow-change framing.
  - Finance/crypto: follow money, liquidity, market behavior, and why the headline is only half the story.
  - Security: direct warning-label energy without sensationalizing harm.
  - Fitness/martial arts: visual, practical, training-energy narration.
  - Stoic/self-improvement: quieter, earned takeaway; no fake guru cadence.
- Visuals should change with the story beat and remain semantically aligned with each sentence/scene.

## Implementation pattern

When editing the local newsletter renderer, prefer a `tone_pack` style map by source type/topic that returns:

1. A natural opener written like a host saw the email and had to tell someone.
2. Conversational transitions for the rest of the facts.
3. Short stock-query keywords derived from subject/body terms for each scene.

Keep display captions separate from spoken text. Never feed caption labels into TTS.

## QA checklist

Before rendering/uploading:

- Read the generated narration aloud mentally: would a sharp human host say this?
- Does the first sentence create curiosity without saying “welcome” or naming the source mechanics?
- Are there 6–10 distinct visual beats for a normal short/newsletter video?
- Does every spoken claim come from the source email/body/snippet or safe contextual rewrite?
- Are generic motivational overlays removed unless topic-appropriate?
