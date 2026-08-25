# VPS clipper self-cleaning pattern

Use this when setting up YouTube/video download + clipping on a small VPS where source media can exhaust disk or tmpfs-backed memory quickly. Treat the user's request for "memory" safety as both disk-space retention and avoiding large in-memory media buffers.

## Default retention model

- Keep code, clip manifests, transcripts, subtitle files, metadata, and upload logs.
- Treat downloaded source videos, temporary transcodes, partial downloads, logs, scratch frames, and final rendered clips as disposable once YouTube upload succeeds.
- Delete downloaded sources automatically after all requested clips render and pass verification; delete final rendered exports after the YouTube API returns a private upload ID unless the user explicitly asks to keep local files.
- Never delete arbitrary user-supplied paths. Only auto-delete files under known project cache directories such as `SOURCES/`, `TMP/`, `DOWNLOADS/`, `RAW_VIDEO/`, `LOGS/`, and `.ytvenv/`.
- Provide a `--keep-source` or `--no-cleanup` escape hatch for debugging.

## Safe cleanup mechanics

Recommended helper behavior for render/download scripts:

0. Stream downloads/transcodes through files on disk instead of keeping full videos in RAM; never load source videos into Python bytes/arrays just to pass them to ffmpeg. Put temp files under the allowlisted scratch roots so the cleaner can see them.
1. Resolve the candidate path with `Path.resolve()`.
2. Compare it against an allowlist of resolved disposable directory roots.
3. Refuse deletion unless the file is inside an allowed root.
4. Delete only after successful clip verification (`ffprobe` confirms output exists, duration is non-zero, and dimensions are `1080x1920` for vertical clips).
5. After deleting files, prune empty scratch directories bottom-up.
6. Log what was deleted and what was skipped.
7. Enforce a project-level byte cap (for example 3-5 GB on small VPSes) before and after batch renders; if the cap is exceeded, delete oldest disposable artifacts first and abort new downloads rather than filling the VPS.

Python sketch:

```python
from pathlib import Path

DISPOSABLE_DIRS = ("SOURCES", "TMP", "DOWNLOADS", "RAW_VIDEO", "LOGS")

def is_under(path: Path, root: Path) -> bool:
    path = path.resolve()
    root = root.resolve()
    return path == root or root in path.parents

def safe_delete(path: Path, project_root: Path, keep_source: bool = False) -> bool:
    if keep_source or not path.exists() or not path.is_file():
        return False
    allowed_roots = [(project_root / name).resolve() for name in DISPOSABLE_DIRS]
    if not any(is_under(path, root) for root in allowed_roots):
        print(f"skip cleanup outside disposable dirs: {path}")
        return False
    path.unlink()
    return True
```

## Project cleaner command

For a standalone cleaner, support a dry run first:

```bash
python3 scripts/cleanup_artifacts.py --dry-run --max-age-hours 24 --max-bytes 5000000000
python3 scripts/cleanup_artifacts.py --max-age-hours 24 --max-bytes 5000000000
```

Cleaner behavior should remove oldest scratch artifacts first until under the byte budget, but preserve final exports unless explicitly asked. If final exports are also disposable for a particular project, require an explicit flag like `--include-exports`.

## Reporting to the user

For Discord-style handoffs, be concise and state the safety guarantee:

- downloader/clipping is set up;
- clips are verified before reporting success;
- uploader/deploy scripts delete final rendered clips after successful YouTube upload;
- sources in scratch folders are auto-deleted after successful renders;
- `--keep-source` exists for debugging.
