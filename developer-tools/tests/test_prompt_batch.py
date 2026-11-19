"""Unit tests for batch-of-5 structured prompt orchestration."""

import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image

from image_audit.database import create_database
from prompt_batch import build_prompt_batch, mark_dispatched


class PromptBatchTests(unittest.TestCase):
    def test_batch_caps_at_five_and_advances_after_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            game = root / "game"
            (game / "images" / "college").mkdir(parents=True)
            img = game / "images" / "college" / "low.jpg"
            Image.new("RGB", (640, 360), (2, 2, 2)).save(img)

            db_path = root / "batch.sqlite"
            create_database([("images/college/low.jpg", img.stat().st_size)],
                            [], {}, [], db_path=db_path, game_root=game)

            reqs_path = root / "requests.json"
            reqs_path.write_text(json.dumps({
                "requests": [
                    {"storyKey": f"story_{i}", "category": "college",
                     "storyFile": "40_story/day.rpy", "status": "needs_generation",
                     "prompt": f"Prompt {i}"}
                    for i in range(7)
                ]
            }), encoding="utf-8")

            first = build_prompt_batch(limit=10, kind="all", db_path=db_path, requests_path=reqs_path)
            self.assertEqual(len(first), 5)
            self.assertEqual(first[0]["kind"], "regen")
            mark_dispatched(first, db_path=db_path)

            second = build_prompt_batch(limit=5, kind="story", db_path=db_path, requests_path=reqs_path)
            self.assertEqual(len(second), 3)
            self.assertFalse({p["id"] for p in first} & {p["id"] for p in second})


if __name__ == "__main__":
    unittest.main()
