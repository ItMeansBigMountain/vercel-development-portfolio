#!/usr/bin/env python3
"""Upload tweet_video_generator output.mp4 with the shared HeRmEz YouTube uploader."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SHARED_UPLOADER = Path('/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py')
PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_LOG = PROJECT_ROOT / 'UPLOADS' / 'youtube_uploads.jsonl'


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('video', nargs='?', default=str(PROJECT_ROOT / 'output.mp4'))
    p.add_argument('--title', default='Tweet Video Generator - Private Upload')
    p.add_argument('--description', default='Private upload from the repaired tweet_video_generator pipeline.')
    p.add_argument('--tags', default='tweets,automation,video')
    p.add_argument('--privacy', default='private', choices=['private', 'unlisted', 'public'])
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    video = Path(args.video)
    if not video.exists():
        raise SystemExit(f'Missing video file: {video}')
    cmd = [
        sys.executable, str(SHARED_UPLOADER), str(video),
        '--title', args.title,
        '--description', args.description,
        '--tags', args.tags,
        '--privacy', args.privacy,
        '--project', 'tweet_video_generator',
        '--log-jsonl', str(DEFAULT_LOG),
    ]
    if args.dry_run:
        cmd.append('--dry-run')
    return subprocess.call(cmd)


if __name__ == '__main__':
    raise SystemExit(main())
