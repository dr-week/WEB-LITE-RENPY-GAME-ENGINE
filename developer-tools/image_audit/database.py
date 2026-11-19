"""Persist image audit inventory, quality metrics, and missing reference queries."""

from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3

from image_quality import inspect_image
from .schema import SCHEMA_SQL

DATABASE = Path(__file__).resolve().parents[1] / "image_audit.sqlite"
GAME_ROOT = Path(__file__).resolve().parents[2] / "game"


def _ensure_schema(db: sqlite3.Connection) -> None:
    cols = {row[1] for row in db.execute("PRAGMA table_info(image_assets)")}
    if cols and "quality_score" not in cols:
        db.execute("DROP TABLE image_assets")
    db.executescript(SCHEMA_SQL)


def _asset_row(rel_path: str, size: int, game_root: Path) -> tuple:
    full = game_root / rel_path
    category = Path(rel_path).parts[1] if len(Path(rel_path).parts) > 2 else ""
    digest = hashlib.sha256(full.read_bytes()).hexdigest() if full.is_file() else ""
    qc = inspect_image(full) if full.is_file() else {"width": 0, "height": 0, "quality_score": 0, "flags": ["missing"]}
    return (
        rel_path,
        size,
        digest,
        category,
        qc["width"],
        qc["height"],
        qc["quality_score"],
        json.dumps(qc["flags"]),
    )


def create_database(assets, references, aliases, alias_refs,
                    db_path: Path = DATABASE, game_root: Path = GAME_ROOT) -> None:
    with closing(sqlite3.connect(db_path)) as db, db:
        _ensure_schema(db)
        db.execute("DELETE FROM image_references")
        db.execute("DELETE FROM alias_references")
        db.execute("DELETE FROM image_aliases")
        existing_paths = {row[0] for row in db.execute("SELECT path FROM image_assets")}
        current_paths = {path for path, _ in assets}
        for stale in existing_paths - current_paths:
            db.execute("DELETE FROM image_assets WHERE path = ?", (stale,))
        for rel_path, size in assets:
            row = _asset_row(rel_path, size, game_root)
            db.execute("""
                INSERT INTO image_assets (path, bytes, sha256, category, width, height, quality_score, quality_flags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    bytes=excluded.bytes, sha256=excluded.sha256, category=excluded.category,
                    width=excluded.width, height=excluded.height,
                    quality_score=excluded.quality_score, quality_flags=excluded.quality_flags,
                    updated_at=CURRENT_TIMESTAMP
            """, row)
        db.executemany("INSERT OR IGNORE INTO image_references VALUES (?, ?, ?, ?)", references)
        db.executemany("INSERT INTO image_aliases VALUES (?, ?, ?)",
                       [(name, *location) for name, location in aliases.items()])
        db.executemany("INSERT OR IGNORE INTO alias_references VALUES (?, ?, ?, ?)",
                       [(source, line, name, int(name in aliases)) for source, line, name in alias_refs])


def query_missing(db_path: Path = DATABASE):
    with closing(sqlite3.connect(db_path)) as db:
        missing_images = list(db.execute("SELECT source, line, target_path FROM missing_images"))
        missing_aliases = list(db.execute("SELECT source, line, alias FROM missing_aliases"))
    return missing_images, missing_aliases


def query_low_quality(threshold: int = 75, db_path: Path = DATABASE):
    with closing(sqlite3.connect(db_path)) as db:
        return list(db.execute(
            "SELECT path, width, height, quality_score, quality_flags FROM image_assets "
            "WHERE path LIKE 'images/%' AND quality_score < ? ORDER BY quality_score ASC",
            (threshold,),
        ))
