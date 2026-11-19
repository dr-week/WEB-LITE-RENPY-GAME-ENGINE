"""Unit tests for the unified check_everything verification modules."""

import json
import tempfile
import unittest
from pathlib import Path

from checks import check_asset_hygiene, check_module_sizes, check_story_integrity


class CheckEverythingTests(unittest.TestCase):
    def test_story_integrity_catches_missing_jump_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            game = Path(tmp) / "game"
            (game / "data").mkdir(parents=True)
            (game / "images").mkdir(parents=True)
            (game / "script.rpy").write_text("label start:\n    jump nowhere\n", encoding="utf-8")
            (game / "data" / "story_starts.json").write_text(json.dumps({"starts": []}), encoding="utf-8")
            res = check_story_integrity(game)
            self.assertFalse(res["ok"])
            self.assertEqual(res["missing_targets"], [("script.rpy", 2, "nowhere")])

    def test_asset_hygiene_and_module_health_pass_on_clean_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            game = root / "game"
            (root / "developer-tools").mkdir()
            (game / "images" / "ui" / "icons").mkdir(parents=True)
            (game / "images" / "ui" / "icons" / "ok.png").write_bytes(b"png")
            (game / "ui.rpy").write_text('screen t():\n    add "ui/icons/ok.png"\n', encoding="utf-8")
            assets = check_asset_hygiene(game)
            modules = check_module_sizes(root)
            self.assertTrue(assets["ok"])
            self.assertEqual(modules["oversized"], [])


if __name__ == "__main__":
    unittest.main()
