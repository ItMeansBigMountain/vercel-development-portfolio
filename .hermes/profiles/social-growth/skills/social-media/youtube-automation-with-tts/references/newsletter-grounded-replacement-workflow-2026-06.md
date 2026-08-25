# Grounded newsletter replacements: user correction and workflow

Use this when regenerating newsletter-to-video uploads after the user says the narration drifted into advice, opinion, or unrelated motivational framing.

## User correction

The user does **not** want newsletter videos to sound like the assistant's take on the news. The narration should:

- Go deeper into the newsletter's actual content.
- Relay the newsletter message in a personified, human voice.
- Avoid robotic phrasing, but remain faithful to the source.
- Avoid advice/moralizing such as “build one proof today,” “your move,” “turn this into a workflow,” “do one hard thing,” or generic self-improvement calls-to-action unless the newsletter itself says that.
- Avoid “My read:” framing in public metadata for newsletter videos.

## Script guardrail pattern

Before rendering/uploading, assert the combined narration + description does not contain prior drift phrases, for example:

```python
bad = [
    'build one proof',
    'your move',
    'turn this into',
    'so the move is simple',
    'do not just consume',
    'my read:',
]
joined = (script.get('narration','') + ' ' + script.get('description','')).lower()
hits = [b for b in bad if b in joined]
if hits:
    raise RuntimeError(f'grounding guard failed: {hits}')
```

## Replacement workflow that worked

1. Locate the original workdir under the project `videos/` folder and load `source_email.json`.
2. Rebuild the script with the corrected grounded newsletter narration.
3. Use concise, proven stock search terms for visuals instead of long sentence-like queries. Long free-form queries caused provider failures. Good generic security/news stock terms include:
   - `cyber security`
   - `server room`
   - `data center`
   - `hacker`
   - `computer security`
   - `security operations center`
   - `cyber attack`
   - `laptop alert`
   - `network security`
   - `ransomware`
4. Render the corrected video in a `corrected-<slug>` workdir.
5. Upload as a new public replacement video.
6. Append a source marker to the upload log with `replacement_for` and `correction='grounded_newsletter_relay_no_advice'`.

## Important pitfall

Do not let failed physical Gmail cleanup turn a verified YouTube upload into a failed process result. For read-only Gmail profiles, write the upload/source marker first, then attempt trashing in a best-effort `try/except` and store `cleanup_error` if it fails.

## Verification

- `py_compile` passes after renderer changes.
- Guardrail phrase scan passes before upload.
- Upload returns `status: UPLOADED` and a `video_id`.
- Upload log contains the new video URL and the old URL in `replacement_for`.
