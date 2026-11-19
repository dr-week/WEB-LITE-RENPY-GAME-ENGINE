"""Sync in-game image feedback JSON into the persistent SQLite database."""

from contextlib import closing
import json
from pathlib import Path
import sqlite3

from .database import DATABASE, GAME_ROOT
from .schema import SCHEMA_SQL

FEEDBACK_JSON = GAME_ROOT / "data" / "image_feedback.json"


def sync_feedback_file(feedback_path: Path = FEEDBACK_JSON, db_path: Path = DATABASE) -> dict:
    """Import ratings from game/data/image_feedback.json into SQLite and update asset statuses."""
    if not feedback_path.is_file():
        return {"imported": 0, "flagged": 0, "approved": 0, "relocated": 0, "removed": 0}
    raw = json.loads(feedback_path.read_text(encoding="utf-8-sig"))
    entries = raw.get("ratings", []) if isinstance(raw, dict) else []
    imported = flagged = approved = relocated = removed = 0
    with closing(sqlite3.connect(db_path)) as db, db:
        db.executescript(SCHEMA_SQL)
        for entry in entries:
            asset = _normalize_path(str(entry.get("asset_path", "")))
            rating = str(entry.get("rating", "")).lower()
            disposition = str(entry.get("disposition", "replace")).lower()
            if not asset or rating not in {"up", "down"}:
                continue
            cur = db.execute("""
                INSERT OR IGNORE INTO image_feedback (asset_path, rating, reason, scene_label, prompt_hint, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                asset,
                rating,
                str(entry.get("reason", "")),
                str(entry.get("scene_label", "")),
                disposition,
                str(entry.get("created_at", "")),
            ))
            imported += cur.rowcount
            if rating == "up":
                new_status = "approved"
                approved += 1
            elif disposition == "relocate":
                new_status = "relocate"
                relocated += 1
            elif disposition == "remove":
                new_status = "removed"
                removed += 1
            else:
                new_status = "needs_regen"
                flagged += 1

            db.execute("UPDATE image_assets SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE path = ?",
                       (new_status, asset))
    return {
        "imported": imported,
        "flagged": flagged,
        "approved": approved,
        "relocated": relocated,
        "removed": removed
    }


def get_flagged_assets(db_path: Path = DATABASE) -> list[dict]:
    """Return all assets marked needs_regen or low quality for prompt regeneration."""
    if not db_path.is_file():
        return []
    with closing(sqlite3.connect(db_path)) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute("SELECT * FROM flagged_assets ORDER BY quality_score ASC").fetchall()
        return [dict(row) for row in rows]


def get_relocatable_assets(db_path: Path = DATABASE) -> list[dict]:
    """Return good assets that are marked to be placed in another scene instead."""
    if not db_path.is_file():
        return []
    with closing(sqlite3.connect(db_path)) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute("SELECT * FROM image_assets WHERE status = 'relocate' ORDER BY path ASC").fetchall()
        return [dict(row) for row in rows]


def _normalize_path(path: str) -> str:
    cleaned = path.replace("\\", "/").lstrip("/")
    return cleaned if cleaned.startswith("images/") else f"images/{cleaned}"
