"""Unit tests for unified story & image SQLite database and quality replacement."""

from contextlib import closing
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

from image_audit.database import create_database
from replace_low_quality import apply_replacements, find_replacements
from story_db import sync_story_db


class StoryDatabaseTests(unittest.TestCase):
    def test_story_sync_and_low_quality_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            game = root / "game"
            (game / "10_characters").mkdir(parents=True)
            (game / "40_story" / "endings").mkdir(parents=True)
            (game / "data").mkdir(parents=True)
            (game / "images" / "college").mkdir(parents=True)

            bad_img = game / "images" / "college" / "old_dark.jpg"
            good_img = game / "images" / "college" / "new_crisp.jpg"
            Image.new("RGB", (640, 360), (2, 2, 2)).save(bad_img)
            img = Image.new("RGB", (1376, 768), (110, 120, 130))
            ImageDraw.Draw(img).rectangle([100, 100, 900, 600], fill=(220, 200, 170))
            img.save(good_img)

            (game / "10_characters" / "scene_art.rpy").write_text(
                'image bg_college = fit_scene_art("images/college/old_dark.jpg")\n',
                encoding="utf-8",
            )
            (game / "data" / "story_starts.json").write_text(
                json.dumps({"starts": [{"id": "PROL_TEST", "location": "college", "scene": "bg_college"}]}),
                encoding="utf-8",
            )
            (game / "40_story" / "endings" / "ending_routes.rpy").write_text(
                '        return {"id": "END_TEST", "title": "Test Ending"}\n',
                encoding="utf-8",
            )

            db_path = root / "test.sqlite"
            assets = [
                ("images/college/old_dark.jpg", bad_img.stat().st_size),
                ("images/college/new_crisp.jpg", good_img.stat().st_size),
            ]
            create_database(assets, [], {}, [], db_path=db_path, game_root=game)
            stats = sync_story_db(game, db_path)
            self.assertEqual(stats["endings"], 1)

            plans = find_replacements(game, db_path, min_score=85)
            self.assertEqual(len(plans), 1)
            self.assertEqual(plans[0]["new"], "images/college/new_crisp.jpg")
            apply_replacements(plans, db_path)
            self.assertIn("new_crisp.jpg", (game / "10_characters" / "scene_art.rpy").read_text(encoding="utf-8"))

            with closing(sqlite3.connect(db_path)) as db:
                status = db.execute("SELECT status FROM image_assets WHERE path='images/college/old_dark.jpg'").fetchone()[0]
                self.assertEqual(status, "replaced")


if __name__ == "__main__":
    unittest.main()
