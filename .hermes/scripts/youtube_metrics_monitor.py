#!/usr/bin/env python3
"""Collect YouTube performance metrics for the active Viral Radar lane.

The paused faceless/newsletter lane is intentionally excluded. Reads Viral Radar
upload logs, fetches video statistics using the same OAuth account that uploaded
each video, and writes durable performance learnings for future clipping runs.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path("/opt/data/HeRmEz/projects")
PROJECTS = {
    "viral-clip-radar": ROOT / "viral-clip-radar" / "UPLOADS" / "youtube_uploads.jsonl",
}
EXTRA_LOGS: dict[str, list[Path]] = {}
# Default token for each upload lane. Rows may override this with token_path,
# youtube_token_path, upload_token_path, or uploader_token_path.
PROJECT_TOKENS = {
    "viral-clip-radar": Path("/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json"),
}
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]
LEARNINGS = ROOT / "_ops" / "social-growth" / "PERFORMANCE_LEARNINGS.md"


def load_dotenv(path: Path = Path("/opt/data/.env")) -> None:
    if not path.exists():
        return
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def read_uploads(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            row = json.loads(line)
        except Exception:
            continue
        # Normalize newsletter logs that use youtube_video_id.
        if row.get("youtube_video_id") and not row.get("video_id"):
            row["video_id"] = row.get("youtube_video_id")
        if row.get("video_id"):
            rows.append(row)
    return rows


def token_for_row(project: str, row: dict[str, Any]) -> Path | None:
    for key in ("token_path", "youtube_token_path", "upload_token_path", "uploader_token_path"):
        if row.get(key):
            return Path(str(row[key])).expanduser()
    env_token = os.getenv(f"YOUTUBE_TOKEN_{project.upper().replace('-', '_')}")
    if env_token:
        return Path(env_token).expanduser()
    return PROJECT_TOKENS.get(project)


def load_youtube_client(token_path: Path):
    creds = Credentials.from_authorized_user_file(str(token_path), scopes=SCOPES)
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json(), encoding="utf-8")
        os.chmod(token_path, 0o600)
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def chunks(xs: list[str], n: int = 50):
    for i in range(0, len(xs), n):
        yield xs[i:i+n]


def fetch_stats_by_uploader(project_rows: dict[str, list[dict[str, Any]]]) -> tuple[dict[str, dict[str, Any]], dict[str, str], dict[str, str]]:
    """Fetch stats with the same token/account configured for each upload row.

    Returns stats_by_video_id, token_label_by_video_id, errors_by_token.
    """
    ids_by_token: dict[Path, set[str]] = defaultdict(set)
    token_project: dict[Path, set[str]] = defaultdict(set)
    for project, rows in project_rows.items():
        for row in rows:
            vid = row.get("video_id")
            token = token_for_row(project, row)
            if vid and token:
                ids_by_token[token].add(vid)
                token_project[token].add(project)

    stats: dict[str, dict[str, Any]] = {}
    token_for_video: dict[str, str] = {}
    errors: dict[str, str] = {}
    for token, ids in ids_by_token.items():
        label = str(token)
        if not token.exists():
            errors[label] = "token file missing"
            continue
        try:
            yt = load_youtube_client(token)
            # Verify/account label: this keeps the same-account contract explicit.
            channel_resp = yt.channels().list(part="snippet", mine=True).execute()
            channel_title = "unknown channel"
            channel_id = "unknown"
            if channel_resp.get("items"):
                ch = channel_resp["items"][0]
                channel_id = ch.get("id", "unknown")
                channel_title = ch.get("snippet", {}).get("title", "unknown channel")
            label = f"{channel_title} ({channel_id}) via {token}"
            for batch in chunks(sorted(ids)):
                resp = yt.videos().list(part="snippet,statistics,status", id=",".join(batch)).execute()
                for item in resp.get("items", []):
                    vid = item.get("id")
                    if not vid:
                        continue
                    stats[vid] = item
                    token_for_video[vid] = label
        except Exception as exc:
            errors[str(token)] = f"{type(exc).__name__}: {exc}"
    return stats, token_for_video, errors


def words(text: str) -> list[str]:
    stop = {"shorts", "the", "and", "you", "your", "this", "that", "with", "from", "public", "viral"}
    return [w for w in re.findall(r"[a-zA-Z]{4,}", text.lower()) if w not in stop]


def is_public_row(row: dict[str, Any], item: dict[str, Any] | None) -> bool:
    if item:
        return item.get("status", {}).get("privacyStatus") == "public"
    return row.get("privacy") == "public" or row.get("privacy") is None


def summarize(project_rows: dict[str, list[dict[str, Any]]], stats: dict[str, dict[str, Any]], token_for_video: dict[str, str], token_errors: dict[str, str]) -> str:
    now = dt.datetime.now(dt.UTC).isoformat()
    lines = ["# Viral Radar Performance Learnings", "", f"Last updated: `{now}`", ""]
    lines += [
        "## Metrics status",
        "",
        "- Live YouTube metrics are fetched with OAuth tokens from the same upload lane/account, not a generic API key.",
        "- This preserves private/unlisted visibility and prevents mixing channel accounts.",
    ]
    if token_errors:
        lines.append("- Token/account errors:")
        for token, err in token_errors.items():
            lines.append(f"  - `{token}`: {err}")
    lines.append("")

    for project, rows in project_rows.items():
        metric_rows = [r for r in rows if is_public_row(r, stats.get(r.get("video_id")))]
        lines += [f"## {project}", "", f"- Uploads logged: {len(rows)} total; {len(metric_rows)} public/metric-eligible."]
        scored = []
        for row in metric_rows:
            item = stats.get(row.get("video_id"))
            if not item:
                continue
            st = item.get("statistics", {})
            views = int(st.get("viewCount", 0) or 0)
            likes = int(st.get("likeCount", 0) or 0)
            comments = int(st.get("commentCount", 0) or 0)
            score = views + likes * 5 + comments * 12
            title = row.get("title") or item.get("snippet", {}).get("title")
            row = {**row, "title": title, "description": row.get("description") or item.get("snippet", {}).get("description", "")}
            scored.append((score, views, likes, comments, row))
        scored.sort(reverse=True, key=lambda x: x[0])
        if scored:
            median_views = statistics.median([x[1] for x in scored])
            lines.append(f"- Median public views in latest snapshot: {median_views}.")
            lines.append("- Current winners to study:")
            for score, views, likes, comments, row in scored[:5]:
                vid = row.get("video_id")
                account = token_for_video.get(vid, "unknown uploader account")
                lines.append(f"  - {views} views / {likes} likes / {comments} comments — {row.get('title')} — {row.get('url') or 'https://youtu.be/' + vid} — metrics account: {account}")
            counter = Counter()
            for _, _, _, _, row in scored[:10]:
                counter.update(words((row.get("title") or "") + " " + (row.get("description") or "")))
            if counter:
                lines.append("- Hook/title words showing up in better performers: " + ", ".join(w for w, _ in counter.most_common(12)) + ".")
        elif metric_rows:
            lines.append("- Live metrics unavailable for metric-eligible videos in this snapshot; inspect token/account errors above.")
        lines.append("")
    lines += [
        "## Operating rule for future Viral Radar runs",
        "",
        "- Before clipping the next influencer video, read this file and avoid repeating low-signal titles/hooks.",
        "- Double down on topics whose public videos beat the channel median views and comments.",
        "- Treat missing metrics as a setup issue, not as proof the content failed.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    load_dotenv()
    project_rows = {name: read_uploads(path) for name, path in PROJECTS.items()}
    for project, paths in EXTRA_LOGS.items():
        project_rows.setdefault(project, [])
        for path in paths:
            project_rows[project].extend(read_uploads(path))

    stats, token_for_video, token_errors = fetch_stats_by_uploader(project_rows)
    snapshot_at = dt.datetime.now(dt.UTC).isoformat()
    for project, rows in project_rows.items():
        out = ROOT / project / "ANALYTICS" / "youtube_metrics.jsonl"
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("a", encoding="utf-8") as f:
            for row in rows:
                vid = row.get("video_id")
                if vid in stats:
                    f.write(json.dumps({"snapshot_at": snapshot_at, "project": project, "upload": row, "metrics_account": token_for_video.get(vid), "youtube": stats[vid]}, separators=(",", ":")) + "\n")
    LEARNINGS.parent.mkdir(parents=True, exist_ok=True)
    LEARNINGS.write_text(summarize(project_rows, stats, token_for_video, token_errors), encoding="utf-8")
    payload = {
        "status": "ok",
        "oauth_metrics": True,
        "video_ids_seen": len({r["video_id"] for rows in project_rows.values() for r in rows if r.get("video_id")}),
        "stats_fetched": len(stats),
        "token_errors": token_errors,
        "learnings": str(LEARNINGS),
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    elif token_errors:
        print('⚠️ **Viral Radar metrics need attention**')
        print(f'• Videos checked: {payload["video_ids_seen"]} | stats fetched: {payload["stats_fetched"]}')
        print(f'• OAuth errors: {len(token_errors)}')
        print(f'📌 Details: `{LEARNINGS}`')
    else:
        print('✅ **Viral Radar metrics updated**')
        print(f'• Videos checked: {payload["video_ids_seen"]} | stats fetched: {payload["stats_fetched"]}')
        print(f'📌 Learnings: `{LEARNINGS}`')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
