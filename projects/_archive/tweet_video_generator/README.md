# tweet_video_generator

Tweet-to-video automation project.

## Role in YouTube automation portfolio

This is now an **active repair lane** rather than just a credential archive.

Goal:

```text
Tweet/X source material → generated tweet-card video → shared YouTube uploader → private review upload
```

## Current repair status

- Old local YouTube pickle token is no longer trusted because it failed with Google's `deleted_client` error.
- YouTube uploads now route through the canonical shared HeRmEz uploader:

```text
/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py
```

- Local wrapper:

```bash
python3 upload_output_to_youtube.py output.mp4 \
  --title "Top Tweets from @handle" \
  --description "Private tweet video for review" \
  --privacy private
```

- Upload logs write to:

```text
UPLOADS/youtube_uploads.jsonl
```

## Credential rule

Twitter/X credentials must come from environment variables, not hardcoded source:

```bash
export TWITTER_CONSUMER_KEY="..."
export TWITTER_CONSUMER_SECRET="..."
export TWITTER_ACCESS_KEY="..."
export TWITTER_ACCESS_SECRET="..."
```

YouTube OAuth credentials/tokens live outside this repo under:

```text
/opt/data/secrets/youtube-main/
```

## Private upload policy

Private YouTube uploads do not need an additional approval step. The user will review in YouTube Studio and manually make videos public if desired.
