from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Destination:
    id: str
    platform: str
    immutable_account_id: str
    handle: str
    display_name: str
    service_url: str
    enabled: bool


class Ledger:
    def __init__(self, path: str | Path):
        self.path = str(path)
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self):
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS destinations (
                    id TEXT PRIMARY KEY,
                    platform TEXT NOT NULL,
                    immutable_account_id TEXT NOT NULL,
                    handle TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    service_url TEXT NOT NULL,
                    enabled INTEGER NOT NULL,
                    verified_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS publication_attempts (
                    attempt_id TEXT PRIMARY KEY,
                    idempotency_key TEXT NOT NULL UNIQUE,
                    destination_id TEXT NOT NULL,
                    requested_visibility TEXT NOT NULL,
                    status TEXT NOT NULL,
                    postiz_post_id TEXT,
                    platform_post_id TEXT,
                    url TEXT,
                    response_json TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(destination_id) REFERENCES destinations(id)
                );
                """
            )

    def save_destination(self, destination: Destination):
        values = asdict(destination)
        values["enabled"] = int(values["enabled"])
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO destinations
                (id, platform, immutable_account_id, handle, display_name, service_url, enabled)
                VALUES (:id, :platform, :immutable_account_id, :handle, :display_name, :service_url, :enabled)
                ON CONFLICT(id) DO UPDATE SET
                platform=excluded.platform,
                immutable_account_id=excluded.immutable_account_id,
                handle=excluded.handle,
                display_name=excluded.display_name,
                service_url=excluded.service_url,
                enabled=excluded.enabled,
                verified_at=CURRENT_TIMESTAMP""",
                values,
            )

    def get_destination(self, destination_id: str) -> Destination | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM destinations WHERE id = ?", (destination_id,)
            ).fetchone()
        if row is None:
            return None
        return Destination(
            id=row["id"],
            platform=row["platform"],
            immutable_account_id=row["immutable_account_id"],
            handle=row["handle"],
            display_name=row["display_name"],
            service_url=row["service_url"],
            enabled=bool(row["enabled"]),
        )

    def begin_attempt(self, attempt_id: str, key: str, destination_id: str, visibility: str):
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO publication_attempts
                (attempt_id, idempotency_key, destination_id, requested_visibility, status)
                VALUES (?, ?, ?, ?, 'submitting')""",
                (attempt_id, key, destination_id, visibility),
            )

    def finish_attempt(
        self,
        attempt_id: str,
        *,
        status: str,
        response: Any = None,
        error: str | None = None,
        postiz_post_id: str | None = None,
        platform_post_id: str | None = None,
        url: str | None = None,
    ):
        response_json = json.dumps(response, sort_keys=True) if response is not None else None
        with self._connect() as connection:
            connection.execute(
                """UPDATE publication_attempts SET status=?, response_json=?, error=?,
                postiz_post_id=?, platform_post_id=?, url=?, updated_at=CURRENT_TIMESTAMP
                WHERE attempt_id=?""",
                (status, response_json, error, postiz_post_id, platform_post_id, url, attempt_id),
            )

    def get_attempt(self, attempt_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM publication_attempts WHERE attempt_id = ?", (attempt_id,)
            ).fetchone()
        return self._row_to_attempt(row)

    def get_by_idempotency_key(self, key: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM publication_attempts WHERE idempotency_key = ?", (key,)
            ).fetchone()
        return self._row_to_attempt(row)

    @staticmethod
    def _row_to_attempt(row) -> dict[str, Any] | None:
        if row is None:
            return None
        result = dict(row)
        result["response"] = json.loads(result.pop("response_json")) if result["response_json"] else None
        return result
