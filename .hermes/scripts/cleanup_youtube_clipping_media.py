#!/usr/bin/env python3
"""Automatic cleanup for generated YouTube clipping media.

Safety rules:
- Never touch code, manifests, metadata, logs, subtitles, analytics, or upload ledgers.
- Never delete media inside Viral Radar retry/hold queues.
- Remove paused faceless generated-video media after 2 days.
- Remove Viral Radar source/render media after 7 days.
- Stay silent when nothing is deleted (suitable for no-agent cron).
"""
from __future__ import annotations

import argparse
import os
import time
from pathlib import Path

MEDIA_EXTENSIONS = {
    ".mp4", ".mkv", ".webm", ".mov", ".avi",
    ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ts",
    ".part", ".ytdl",
}

TARGETS = (
    (Path("/opt/data/HeRmEz/projects/faceless-youtube-channel/videos"), 2),
    (Path("/opt/data/HeRmEz/projects/viral-clip-radar/SOURCES"), 7),
    (Path("/opt/data/HeRmEz/projects/viral-clip-radar/OUTPUTS"), 7),
    (Path("/opt/data/HeRmEz/projects/viral-clip-radar/videos"), 7),
    (Path("/opt/data/HeRmEz/projects/viral-clip-radar/TMP"), 7),
)

PROTECTED_PARTS = {
    "UPLOAD_QUEUE", "UPLOAD_QUEUE_HOLD", "UPLOADS", "STATE", "CLIP_PLANS",
    "ANALYTICS", "LOGS", ".git",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--now", type=float, default=time.time(), help=argparse.SUPPRESS)
    args = parser.parse_args()

    removed_files = 0
    removed_bytes = 0
    touched_roots: set[Path] = set()

    for root, retention_days in TARGETS:
        if not root.is_dir():
            continue
        cutoff = args.now - retention_days * 86400
        for dirpath, dirnames, filenames in os.walk(root):
            current = Path(dirpath)
            dirnames[:] = [d for d in dirnames if d not in PROTECTED_PARTS]
            if any(part in PROTECTED_PARTS for part in current.parts):
                continue
            for filename in filenames:
                path = current / filename
                if path.suffix.lower() not in MEDIA_EXTENSIONS:
                    continue
                try:
                    stat = path.stat()
                except FileNotFoundError:
                    continue
                if stat.st_mtime >= cutoff:
                    continue
                removed_files += 1
                removed_bytes += stat.st_size
                touched_roots.add(root)
                if not args.dry_run:
                    path.unlink(missing_ok=True)

    if not args.dry_run:
        for root in touched_roots:
            for dirpath, _, _ in os.walk(root, topdown=False):
                path = Path(dirpath)
                if path == root:
                    continue
                try:
                    path.rmdir()  # only succeeds when empty
                except OSError:
                    pass

    if removed_files:
        mode = "Would remove" if args.dry_run else "Removed"
        print(f"✅ **YouTube cleanup:** {mode.lower()} {removed_files} files • {removed_bytes / 1024**3:.2f} GiB freed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
