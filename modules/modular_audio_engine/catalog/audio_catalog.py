"""
Audio Catalog Manager: Handles song metadata, BPM, Key, and tagging.
Independent of Ren'Py or any GUI framework.
"""
import os
import json

class AudioCatalog:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to bundled catalog
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(os.path.dirname(cur_dir), "..", "..", "game", "audio", "music_database.json")
        self.db_path = os.path.abspath(db_path)
        self.tracks = self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_track(self, track_id):
        for t in self.tracks:
            if t["id"] == track_id:
                return t
        return None

    def filter_by_mood(self, keyword):
        return [t for t in self.tracks if keyword.lower() in t.get("mood", "").lower()]

    def filter_by_bpm_range(self, min_bpm, max_bpm):
        return [t for t in self.tracks if min_bpm <= t.get("bpm", 0) <= max_bpm]
