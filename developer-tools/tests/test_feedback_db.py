"""Unit tests for persistent SQLite audit DB and feedback regeneration loop."""

import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

from image_audit.database import create_database
from image_audit.feedback_sync import get_flagged_assets, sync_feedback_file
from image_generation.feedback_prompts import build_regen_prompt


class FeedbackDatabaseTests(unittest.TestCase):
    def test_feedback_sync_flags_asset_and_builds_regen_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            game = root / "game"
            img_path = game / "images" / "college" / "Maya_lecture_test.jpg"
            img_path.parent.mkdir(parents=True)
            img = Image.new("RGB", (1280, 720), (100, 110, 120))
            ImageDraw.Draw(img).rectangle([100, 100, 600, 500], fill=(220, 180, 140))
            img.save(img_path)

            db_path = root / "test_audit.sqlite"
            create_database([("images/college/Maya_lecture_test.jpg", img_path.stat().st_size)],
                            [], {}, [], db_path=db_path, game_root=game)

            fb_path = game / "data" / "image_feedback.json"
            fb_path.parent.mkdir(parents=True)
            fb_path.write_text(json.dumps({
                "schema_version": 1,
                "ratings": [{
                    "asset_path": "images/college/Maya_lecture_test.jpg",
                    "rating": "down",
                    "reason": "Wrong character / outfit",
                    "scene_label": "day_01_college",
                    "created_at": "2026-11-16T11:20:00",
                }],
            }), encoding="utf-8")

            stats = sync_feedback_file(fb_path, db_path)
            self.assertEqual(stats["imported"], 1)
            self.assertEqual(stats["flagged"], 1)

            flagged = get_flagged_assets(db_path)
            self.assertEqual(len(flagged), 1)
            self.assertEqual(flagged[0]["status"], "needs_regen")
            prompt = build_regen_prompt(flagged[0])
            self.assertIn("dark slate-blue T-shirt dress", prompt)
            self.assertIn("day_01_college", prompt)


if __name__ == "__main__":
    unittest.main()
