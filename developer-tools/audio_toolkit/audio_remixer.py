"""
Lightweight Audio Remixer, Crossfader & DJ Stems Toolkit.
Designed for Lola / Ren'Py audio pipelines.
"""
import os
import json
import wave
import struct
import math
import random

class AudioRemixer:
    def __init__(self, db_path="game/audio/music_database.json"):
        self.db_path = db_path
        self.tracks = self._load_db()

    def _load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_track(self, track_id):
        for t in self.tracks:
            if t["id"] == track_id:
                return t
        return None

    def find_compatible_mixes(self, track_id, max_bpm_diff=6):
        """Find tracks with matching/close BPM for clean DJ beatmatching."""
        base = self.get_track(track_id)
        if not base:
            return []
        matches = []
        for t in self.tracks:
            if t["id"] != track_id:
                diff = abs(t["bpm"] - base["bpm"])
                if diff <= max_bpm_diff:
                    matches.append({
                        "track": t,
                        "bpm_diff": diff,
                        "ratio": round(base["bpm"] / t["bpm"], 3)
                    })
        matches.sort(key=lambda x: x["bpm_diff"])
        return matches
