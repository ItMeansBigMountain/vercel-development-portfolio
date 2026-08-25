# VPS YouTube Clipping Delivery Notes

Use this for requests like: "pick a popular long-form podcast/science video, download it, clip it, and present MP4 files."

## Practical source fallback

Cloud/VPS IPs often hit YouTube bot checks even with current `yt-dlp` and pytubefix. When the user asks for a finished MP4 artifact and did not require a specific newly-posted source, search for a legitimate mirror of the same public YouTube video on Internet Archive:

```bash
python3 - <<'PY'
import json, urllib.request
for ident in ['youtube-VIDEO_ID']:
    data=json.load(urllib.request.urlopen(f'https://archive.org/metadata/{ident}', timeout=20))
    print(data.get('metadata',{}).get('title'))
    for f in data.get('files',[]):
        if f.get('name','').lower().endswith(('.mp4','.webm','.mkv','.vtt','.srt','.description')):
            print(f.get('name'), f.get('size'))
PY
```

Download resumably so long archive downloads can survive timeouts:

```bash
curl -L -C - --fail --retry 3 -o SOURCES/<slug>/<video_id>.mp4 \
  https://archive.org/download/youtube-<video_id>/<video_id>.mp4
```

Keep the original YouTube URL plus archive URL in `CLIP_PLANS/<candidate>/metadata.json` or `clip_manifest.json` for attribution and traceability.

## Segment selection

Use available VTT/SRT transcript to find high-signal segments by keyword. Good clip themes from long explanatory content:

- counterintuitive reframes ("dopamine is wanting, not pleasure")
- actionable behavioral tools (procrastination protocols, breathing, reward schedules)
- named concepts (reward prediction error, intermittent reinforcement)

Generate a manifest before rendering:

```json
{
  "source_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "archive_source": "https://archive.org/details/youtube-VIDEO_ID",
  "source_file": "SOURCES/<slug>/<video_id>.mp4",
  "clips": [
    {"file": "EXPORTS/<slug>/<name>.mp4", "start": "00:13:31", "end": "00:14:48", "hook": "..."}
  ]
}
```

## Captioned vertical exports

For Discord delivery, prefer finished captioned 9:16 MP4 files, not just raw cuts.

If the project has a manifest renderer (for example `scripts/render_clip_manifest.py` in `viral-clip-radar`), use it before hand-writing ad hoc ffmpeg commands. The robust pattern is:

```bash
python3 scripts/render_clip_manifest.py \
  CLIP_PLANS/<plan>/clip_manifest.json \
  --source SOURCES/<slug>/<video_id>.mp4 \
  --outdir EXPORTS/<slug>-captioned
```

Renderer expectations worth preserving in future implementations:

- Accept a `clip_manifest.json` with `source_file`, `clips[].start`, `clips[].end`, `clips[].file`, and `clips[].hook`.
- Burn in `CLIP_PLANS/<plan>/subtitles/<clip-stem>.srt` when present.
- If no subtitle exists, add a simple hook overlay so the export is not a raw crop.
- Verify each output is exactly `1080x1920` before reporting success.
- Run artifact cleanup before/after rendering unless the user explicitly needs to preserve local media.
- After all clips render successfully, delete the original downloaded source video from disposable project media folders (`SOURCES/`, `TMP/`, `DOWNLOADS/`, `RAW_VIDEO/`) so the VPS does not keep huge source files. Provide a `--keep-source` style escape hatch for debugging, and never auto-delete arbitrary user files outside those disposable folders.

Fallback one-off render shape:

```bash
ffmpeg -y -ss START -to END -i SOURCES/<slug>/<video_id>.mp4 \
  -vf "scale=-2:1920,crop=1080:1920,drawbox=x=0:y=0:w=iw:h=220:color=black@0.55:t=fill,drawtext=text='HOOK':fontcolor=white:fontsize=54:box=1:boxcolor=black@0.35:boxborderw=18:x=(w-text_w)/2:y=70,subtitles=clip.srt:force_style='FontName=DejaVu Sans,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H99000000,BorderStyle=3,Outline=2,Alignment=2,MarginV=170'" \
  -c:v libx264 -preset veryfast -crf 24 -c:a aac -b:a 128k -movflags +faststart \
  EXPORTS/<slug>/<name>-captioned.mp4
```

Verification before presenting:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -show_entries format=size -of default=nw=1 EXPORTS/<slug>/*.mp4
ffmpeg -y -ss 00:00:10 -i EXPORTS/<slug>/<name>.mp4 -frames:v 1 /tmp/preview.jpg
```

Inspect at least one preview frame to ensure the hook and subtitles are visible and not badly cut off.

## Cleanup / no-cloud-backup mode

If the user abandons a cloud backup idea and asks to keep working locally, remove the abandoned integration artifacts rather than leaving half-built cache projects around. For clipping projects on small VPS disks:

- Keep code, manifests, subtitles, transcripts, and clip-plan metadata in git.
- Keep generated media (`SOURCES/`, `EXPORTS/`, `TMP/`, `LOGS/`, `.ytvenv/`) ignored and disposable.
- Before deleting generated media, commit or bundle the nested clipping repo if it has no remote:

```bash
git add CLIP_PLANS/<plan>/clip_manifest.json CLIP_PLANS/<plan>/subtitles/*.srt
git commit -m "docs: add reviewed clip plan metadata"
mkdir -p /opt/data/HeRmEz/projects/_backups/<project>
git bundle create /opt/data/HeRmEz/projects/_backups/<project>/<project>.bundle --all
git bundle verify /opt/data/HeRmEz/projects/_backups/<project>/<project>.bundle
```

Then free disk with explicit local artifact deletion or the project cleaner. Re-check `du -sh` afterward; this workflow has reduced a clipping repo from hundreds of MB back to a tiny metadata/code repo without losing git-tracked plans.

## Reporting

If a real MP4 exists, deliver with `MEDIA:/absolute/path.mp4`. State the actual duration/dimensions from `ffprobe`. Do not over-explain the blocker if a working fallback succeeded; one concise note is enough (e.g. "YouTube direct was bot-blocked, so I used the Internet Archive mirror of the same source.").
