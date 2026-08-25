# YouTube high-ticket leverage project pattern

Use this reference when creating a durable workspace for a content channel that is intended to validate or feed a future high-ticket offer.

## Trigger

The user asks to manage a YouTube/TikTok/Instagram channel, public transformation log, content system, or high-ticket leverage project.

## Principle

Do not create an empty notes folder. Create a content operating system with reusable templates, storyboards, and a script helper so the project can keep producing episodes.

## Recommended folder shape

```text
README.md
PRODUCT_DIRECTION.md
STORY_BANK/master_timeline.md
CHANNEL_STRATEGY/content_pillars.md
CHANNEL_STRATEGY/publishing_system.md
STORYBOARDS/000_storyboard_flowchart_template.md
STORYBOARDS/001_<origin_story>.md
VIDEO_SCRIPTS/long_form/
VIDEO_SCRIPTS/shorts/short_hooks_bank.md
VIDEO_SCRIPTS/weekly_reset_template.md
OFFER/high_ticket_offer_hypotheses.md
CONTENT_CALENDAR/30_day_public_log.md
EPISODES/
scripts/new_episode.py
.gitignore
```

## Flowchart storyboard template

```text
Cold open / hook
|
V
Current moment
|
V
Memory trigger
|
V
Conflict
|
V
Consequence
|
V
Turning point
|
V
System / lesson
|
V
Proof / receipts
|
V
Audience mirror
|
V
CTA
```

## Helper script behavior

`scripts/new_episode.py` should:

- accept an episode number and title
- slugify the title
- create `EPISODES/<number>-<slug>/`
- copy/fill the weekly reset outline into `outline.md`
- create empty `notes.md` and `clips.md`
- print the created folder path

## Verification

After scaffolding:

1. Run the helper once to create a sample/planned episode workspace.
2. Confirm the generated files exist.
3. Initialize/commit the project if the user asked for a real workspace.
4. If the project lives under the user's project workspace and is a standalone repo, ensure the parent workspace won't accidentally swallow it if that matters in the current setup.

## Guardrails

- Keep family/relationship stories anonymized for public content.
- Capture raw story in `STORY_BANK/`, but publish only lesson-focused versions.
- Treat offer docs as hypotheses until audience response validates demand.
- Avoid writing guru-flavored copy when the project is built on an unfinished public transformation.
