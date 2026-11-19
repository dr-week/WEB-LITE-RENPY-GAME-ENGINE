"""Sync parsed story graph into developer-tools/image_audit.sqlite."""

from contextlib import closing
import json
from pathlib import Path
import sqlite3

from image_audit.database import DATABASE, GAME_ROOT
from image_audit.schema import SCHEMA_SQL
from .scanner import collect_story_graph


def sync_story_db(game_root: Path = GAME_ROOT, db_path: Path = DATABASE) -> dict:
    graph = collect_story_graph(game_root)
    with closing(sqlite3.connect(db_path)) as db, db:
        db.executescript(SCHEMA_SQL)
        for tbl in ("story_nodes", "story_choices", "story_image_links", "story_endings"):
            db.execute(f"DELETE FROM {tbl}")
        db.executemany("INSERT OR REPLACE INTO story_nodes VALUES (?, ?, ?, ?, ?, ?)", graph["nodes"])
        choice_rows = [(c[0], c[1], c[2], json.dumps(c[3]), c[4]) for c in graph["choices"]]
        db.executemany("INSERT OR REPLACE INTO story_choices VALUES (?, ?, ?, ?, ?)", choice_rows)
        db.executemany("INSERT OR IGNORE INTO story_image_links VALUES (?, ?, ?, ?)", graph["links"])
        db.executemany("INSERT OR REPLACE INTO story_endings VALUES (?, ?, ?, ?)", graph["endings"])
    return {
        "nodes": len(graph["nodes"]),
        "choices": len(graph["choices"]),
        "links": len(graph["links"]),
        "endings": len(graph["endings"]),
    }
