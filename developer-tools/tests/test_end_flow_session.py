"""Unit tests for end-of-session Flow collection ZIP extraction and catalog/DB sync."""

import tempfile
import unittest
from pathlib import Path
import zipfile
from PIL import Image

from end_flow_session import finalize_session, find_collection_zip
from image_audit.database import create_database


class EndFlowSessionTests(unittest.TestCase):
    def test_finalize_session_extracts_categorizes_and_catalogs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            downloads = root / "downloads"
            downloads.mkdir()
            game = root / "game"
            (game / "images").mkdir(parents=True)
            (game / "data").mkdir(parents=True)

            sample = root / "campus_cafeteria_test.jpg"
            Image.new("RGB", (1376, 768), (100, 120, 140)).save(sample)
            zip_path = downloads / "story collection 02.zip"
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.write(sample, arcname="campus_cafeteria_test.jpg")

            found = find_collection_zip(downloads, "story collection 02")
            self.assertEqual(found, zip_path)

            db_path = root / "test.sqlite"
            create_database([], [], {}, [], db_path=db_path, game_root=game)
            res = finalize_session(zip_path, game_root=game, db_path=db_path, collection="story collection 02")
            self.assertEqual(res["imported"], 1)
            self.assertTrue((game / "images" / "college" / "campus_cafeteria_test.jpg").is_file())
            self.assertTrue((game / "data" / "image_story_catalog.json").is_file())


if __name__ == "__main__":
    unittest.main()
