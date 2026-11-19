"""
High-Performance SQLite-Backed Story Narrative Engine Database.
Provides ultra-fast indexing, querying, CRUD, and logical alignment verification.
"""
import sqlite3
import json
import os

class StoryDatabase:
    def __init__(self, db_path="data/story_engine/story_arcs.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS story_beats (
                    beat_id TEXT PRIMARY KEY,
                    act TEXT NOT NULL,
                    chapter TEXT NOT NULL,
                    tension_level INTEGER NOT NULL,
                    scene_type TEXT NOT NULL,
                    hook_description TEXT NOT NULL,
                    stakes_description TEXT NOT NULL,
                    associated_music TEXT,
                    is_active INTEGER DEFAULT 1
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS character_alignments (
                    char_id TEXT PRIMARY KEY,
                    public_facade TEXT NOT NULL,
                    secret_agenda TEXT NOT NULL,
                    vulnerability TEXT NOT NULL,
                    leverage_item TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS narrative_rules (
                    rule_id TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    rule_text TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """)
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_beat_chapter ON story_beats(chapter)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_beat_tension ON story_beats(tension_level)")

    def upsert_beat(self, beat_id, act, chapter, tension, scene_type, hook, stakes, music=""):
        with self.conn:
            self.conn.execute("""
                INSERT INTO story_beats (beat_id, act, chapter, tension_level, scene_type, hook_description, stakes_description, associated_music, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                ON CONFLICT(beat_id) DO UPDATE SET
                    act=excluded.act, chapter=excluded.chapter, tension_level=excluded.tension_level,
                    scene_type=excluded.scene_type, hook_description=excluded.hook_description,
                    stakes_description=excluded.stakes_description, associated_music=excluded.associated_music, is_active=1
            """, (beat_id, act, chapter, tension, scene_type, hook, stakes, music))

    def get_beat(self, beat_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM story_beats WHERE beat_id = ?", (beat_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def list_chapter_beats(self, chapter):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM story_beats WHERE chapter = ? AND is_active = 1 ORDER BY tension_level ASC", (chapter,))
        return [dict(r) for r in cur.fetchall()]

    def delete_beat(self, beat_id):
        with self.conn:
            self.conn.execute("DELETE FROM story_beats WHERE beat_id = ?", (beat_id,))

    def close(self):
        self.conn.close()
