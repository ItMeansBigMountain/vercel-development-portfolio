# Faceless newsletter avatar storytelling, visual variety, and Parrot AI notes

Use this when generating or revising the user's fareed320 → Trapiistan/Sosai Oyama newsletter videos.

## User correction: scripts must feel like an avatar, not a structure

The user corrected the script direction after several iterations: even improved beat labels can still sound too structured. The desired feel is **a charismatic avatar/personality sharing news as a compelling story**, not an intro/body/conclusion or scripted lecture.

Apply these rules:

- Spoken narration should be one continuous, natural monologue.
- Captions may use punchy labels, but the voiceover should not announce or imply sections.
- Avoid templated phrases such as `the signal`, `operator angle`, `move first`, `in conclusion`, or obvious outline language.
- Open like a personality saying “wait, did you see this?”
- Build curiosity, stakes, irony/twist, and payoff naturally.
- Match the newsletter’s tone: AI/tech can be witty; security urgent/practical; finance skeptical/follow-the-money; fitness/Stoic grounded and motivational.
- Humor is good when appropriate, but never trivialize harm, breaches, layoffs, injuries, or real-world victims.
- End with a practical takeaway that feels earned, not bolted on.

Bad:

> Introduction: AI is changing. Body: tools are useful. Conclusion: build one proof.

Better:

> AI had another weird little plot twist. Somewhere, a roadmap just got rewritten in panic font. The tools are not the whole story anymore — the real story is whether these demos are turning into workflows people can actually ship with.

## User correction: expand stock footage variety

The user explicitly wants much more visual variety and fewer repeated generic stock clips.

Implementation rules:

- Prefer 8–10 visual segments when the script supports it.
- Derive visual queries from company names, products, category, emotion, and scene mood.
- Mix offices, product/app shots, city scenes, server rooms, dashboards, hands on keyboard, teams, late-night founder desk, abstract data, and relevant company/category images.
- Do not let every video become “person on laptop” footage.
- Maintain a visual asset URL history so future renders avoid reusing the same stock URLs where possible.
- Save `visual_manifest.json` and inspect it when QAing variety.

## Parrot AI integration findings

The user has lifetime access to Parrot AI and wants to experiment with using familiar/entertainment-style voices for an edge.

Observed in browser:

- Login works at `https://www.tryparrotai.com` with email/password.
- Web app has AI Voice, AI Music, History, voice library, community voices, and an Audio only toggle.
- New UI text limit observed: 500 characters.
- Classic UI text limit observed: 300 characters.
- Voices include entertainment-character-style voices such as SpongeBob-style entries.
- The site appears to use Firebase auth and AppCheck; no public documented API was found.
- Internal frontend endpoints observed: `/api/create`, `/api/create-public`, `/api/create-voice-preview`, `/api/get-voice-preview`, `/api/save-voice-preview`.

Recommended integration path:

1. Start semi-automated, not fully batch, until export is reliable.
2. Split avatar narration into <=500-character chunks if needed.
3. Use authenticated browser automation to select a voice/persona and generate audio-only output.
4. Capture/download generated audio from result/history.
5. Save as `voice_parrot.mp3` (or equivalent) in the video workspace.
6. Feed that audio into the existing renderer.
7. Only promote to batch upload after one complete exported audio file is reliably captured.

## Public channel safety note

For public YouTube uploads, prefer original/parody-inspired personas rather than explicitly branding the content as an exact celebrity or protected character impersonation. Safer creative direction examples:

- `hyper energetic nautical cartoon tech host`
- `sarcastic animated sponge-style startup reporter`
- `chaotic Saturday-morning-cartoon AI news anchor`
- `movie-trailer finance guy`

The goal is familiar energy and retention, not dependency on exact protected-character branding.
