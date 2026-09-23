"""Durable, project-local storage for metadata-only live usage events."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from aiops.models.domain import UsageEvent


class UsageStore:
    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS usage_events (
                    event_id TEXT PRIMARY KEY,
                    recorded_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )

    def _connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def list_events(self) -> list[UsageEvent]:
        with self._connection() as connection:
            rows = connection.execute("SELECT payload FROM usage_events ORDER BY recorded_at, event_id").fetchall()
        return [UsageEvent.model_validate(json.loads(row[0])) for row in rows]

    def insert(self, event: UsageEvent) -> bool:
        payload = json.dumps(event.model_dump(mode="json"), sort_keys=True)
        with self._connection() as connection:
            cursor = connection.execute(
                "INSERT OR IGNORE INTO usage_events(event_id, recorded_at, payload) VALUES (?, ?, ?)",
                (event.event_id, event.timestamp.isoformat(), payload),
            )
        return cursor.rowcount == 1
