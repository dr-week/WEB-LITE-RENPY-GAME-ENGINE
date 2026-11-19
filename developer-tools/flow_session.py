"""Track Google Flow generation session counts and outcomes in image_audit.sqlite."""

import argparse
from contextlib import closing
import datetime
from pathlib import Path
import sqlite3

from image_audit.database import DATABASE

SESSION_SQL = """
CREATE TABLE IF NOT EXISTS flow_sessions (
    session_id TEXT PRIMARY KEY,
    project_name TEXT DEFAULT 'lolagame',
    prompts_sent INTEGER DEFAULT 0,
    images_generated INTEGER DEFAULT 0,
    images_downloaded INTEGER DEFAULT 0,
    notes TEXT DEFAULT '',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def _connect(db_path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(db_path)
    db.executescript(SESSION_SQL)
    return db


def start_session(project: str = "lolagame", db_path: Path = DATABASE) -> str:
    sid = f"flow_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with closing(_connect(db_path)) as db, db:
        db.execute("INSERT INTO flow_sessions (session_id, project_name) VALUES (?, ?)", (sid, project))
    return sid


def update_session(prompts: int = 0, generated: int = 0, downloaded: int = 0,
                   notes: str = "", db_path: Path = DATABASE) -> dict:
    with closing(_connect(db_path)) as db, db:
        row = db.execute(
            "SELECT session_id FROM flow_sessions ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        sid = row[0] if row else f"flow_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if not row:
            db.execute("INSERT INTO flow_sessions (session_id) VALUES (?)", (sid,))
        db.execute("""
            UPDATE flow_sessions
            SET prompts_sent = prompts_sent + ?,
                images_generated = images_generated + ?,
                images_downloaded = images_downloaded + ?,
                notes = CASE WHEN ? != '' THEN ? ELSE notes END
            WHERE session_id = ?
        """, (prompts, generated, downloaded, notes, notes, sid))
        cur = db.execute(
            "SELECT session_id, prompts_sent, images_generated, images_downloaded, notes "
            "FROM flow_sessions WHERE session_id = ?", (sid,)
        ).fetchone()
    return {"session_id": cur[0], "prompts_sent": cur[1],
            "images_generated": cur[2], "images_downloaded": cur[3], "notes": cur[4]}


def session_summary(db_path: Path = DATABASE) -> dict:
    with closing(_connect(db_path)) as db:
        totals = db.execute(
            "SELECT COUNT(*), COALESCE(SUM(prompts_sent), 0), "
            "COALESCE(SUM(images_generated), 0), COALESCE(SUM(images_downloaded), 0) "
            "FROM flow_sessions"
        ).fetchone()
        latest = db.execute(
            "SELECT session_id, prompts_sent, images_generated, images_downloaded "
            "FROM flow_sessions ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
    return {"sessions": totals[0], "total_prompts": totals[1], "total_generated": totals[2],
            "total_downloaded": totals[3], "latest": latest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", action="store_true", help="Start a new Flow session.")
    parser.add_argument("--prompts", type=int, default=0)
    parser.add_argument("--generated", type=int, default=0)
    parser.add_argument("--downloaded", type=int, default=0)
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    if args.start:
        print("Started session:", start_session())
    if args.prompts or args.generated or args.downloaded or args.notes:
        print("Updated:", update_session(args.prompts, args.generated, args.downloaded, args.notes))
    print("Summary:", session_summary())


if __name__ == "__main__":
    main()
