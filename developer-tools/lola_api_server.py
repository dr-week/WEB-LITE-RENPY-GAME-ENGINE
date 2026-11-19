"""Lightweight FastAPI bridge between LOLA game/workbench, SQLite DB, and agents."""

from contextlib import closing
import datetime
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

from image_audit.database import DATABASE, GAME_ROOT
from image_audit.schema import SCHEMA_SQL
from prompt_batch import MAX_BATCH, build_prompt_batch, mark_dispatched
from replace_low_quality import apply_replacements, find_replacements
from story_db import sync_story_db

app = FastAPI(title="LOLA Studio API", version="1.0.0")


class FeedbackIn(BaseModel):
    asset_path: str
    rating: str
    reason: str = ""
    scene_label: str = ""


@app.get("/health")
def health():
    with closing(sqlite3.connect(DATABASE)) as db:
        assets = db.execute("SELECT COUNT(*) FROM image_assets").fetchone()[0]
        nodes = db.execute("SELECT COUNT(*) FROM story_nodes").fetchone()[0]
        flagged = db.execute("SELECT COUNT(*) FROM flagged_assets").fetchone()[0]
    return {"ok": True, "assets": assets, "story_nodes": nodes, "flagged": flagged}


@app.get("/prompts/next")
def next_prompts(limit: int = MAX_BATCH, kind: str = "all", dispatch: bool = False):
    batch = build_prompt_batch(limit=limit, kind=kind)
    if dispatch and batch:
        mark_dispatched(batch)
    return {"count": len(batch), "max_batch": MAX_BATCH, "prompts": batch}


@app.get("/story/evaluate")
def story_evaluate():
    stats = sync_story_db(GAME_ROOT, DATABASE)
    with closing(sqlite3.connect(DATABASE)) as db:
        unhealthy = db.execute(
            "SELECT node_id, asset_path, quality_score, asset_status FROM v_story_image_health "
            "WHERE asset_status IN ('needs_regen', 'missing') OR quality_score < 80"
        ).fetchall()
    return {"stats": stats, "unhealthy_links": len(unhealthy)}


@app.post("/feedback")
def post_feedback(item: FeedbackIn):
    rating = item.rating.lower()
    if rating not in ("up", "down"):
        return {"ok": False, "error": "rating must be 'up' or 'down'"}
    now = datetime.datetime.now().isoformat(timespec="seconds")
    with closing(sqlite3.connect(DATABASE)) as db, db:
        db.executescript(SCHEMA_SQL)
        db.execute(
            "INSERT OR IGNORE INTO image_feedback (asset_path, rating, reason, scene_label, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (item.asset_path, rating, item.reason, item.scene_label, now),
        )
        db.execute("UPDATE image_assets SET status=? WHERE path=?",
                   ("needs_regen" if rating == "down" else "approved", item.asset_path))
    return {"ok": True, "asset_path": item.asset_path, "rating": rating}


@app.post("/replace-low-quality")
def replace_low_quality(apply: bool = False, min_score: int = 85):
    plans = find_replacements(GAME_ROOT, DATABASE, min_score=min_score)
    applied = apply_replacements(plans, DATABASE) if (apply and plans) else 0
    return {"candidates": len(plans), "applied": applied}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
