"""Unit tests for batch lofi music importer, dedup, mix plan rebuild, and credits."""

import json
import os
import tempfile
import time
import unittest
from pathlib import Path

from audio_toolkit.import_music import import_music_folder, merge_colab_analysis
from checks.audio_health import check_audio_health


class ImportMusicTests(unittest.TestCase):
    def test_import_dedups_sanitizes_and_writes_credits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "downloads"
            lofi = root / "game" / "audio" / "music" / "lofi"
            db = root / "game" / "audio" / "music_database.json"
            plan = root / "game" / "audio" / "dj_mix_plan.json"
            credits_out = root / "game" / "audio" / "CREDITS_MUSIC.txt"
            src.mkdir(parents=True)
            lofi.mkdir(parents=True)
            db.write_text("[]", encoding="utf-8")

            (src / "Rainy Night (Lofi).mp3").write_bytes(b"track-one-bytes")
            (src / "zzz_Duplicate Track.mp3").write_bytes(b"track-one-bytes")
            (src / "Sunny Walk.ogg").write_bytes(b"track-two-bytes")

            res = import_music_folder(src, lofi, db, plan, credits_out, apply=True)
            self.assertEqual(res["imported"], 2)
            self.assertEqual(res["skipped"], 1)
            self.assertTrue((lofi / "rainy_night_lofi.mp3").is_file())
            self.assertTrue((lofi / "sunny_walk.ogg").is_file())
            self.assertEqual(len(json.loads(db.read_text(encoding="utf-8"))), 2)
            self.assertIn("Rainy Night Lofi", credits_out.read_text(encoding="utf-8"))

            analysis = root / "music_analysis.json"
            analysis.write_text(json.dumps([{"id": "sunny_walk", "bpm": 82.0, "key": "G Minor",
                                             "beat_drop": 15.5, "bridge": 48.0}]), encoding="utf-8")
            self.assertEqual(merge_colab_analysis(analysis, db, plan), 1)
            updated = next(t for t in json.loads(db.read_text(encoding="utf-8")) if t["id"] == "sunny_walk")
            self.assertEqual(updated["bpm"], 82.0)

    def test_recent_minutes_filter_and_audio_budget_guardrail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "downloads"
            lofi = root / "game" / "audio" / "music" / "lofi"
            db = root / "game" / "audio" / "music_database.json"
            plan = root / "game" / "audio" / "dj_mix_plan.json"
            credits_out = root / "game" / "audio" / "CREDITS_MUSIC.txt"
            src.mkdir(parents=True)
            lofi.mkdir(parents=True)
            db.write_text("[]", encoding="utf-8")

            old_file = src / "Old Track.mp3"
            new_file = src / "Fresh Lofi.mp3"
            old_file.write_bytes(b"old-bytes")
            new_file.write_bytes(b"x" * 20_000)
            old_ts = time.time() - 3600
            os.utime(old_file, (old_ts, old_ts))

            res = import_music_folder(src, lofi, db, plan, credits_out, apply=True, recent_minutes=30)
            self.assertEqual(res["imported"], 1)
            self.assertEqual(res["files"], ["fresh_lofi.mp3"])

            health = check_audio_health(root / "game", budget_mb=0.0)
            self.assertTrue(health["ok"])
            self.assertGreaterEqual(health["audio_mb"], 0.0)
            self.assertTrue(health["over_budget"])


if __name__ == "__main__":
    unittest.main()
