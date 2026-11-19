import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from image_generation.identity import story_request_id
from image_reconciliation import apply_reconciliation, plan_reconciliation


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.game = self.root / "game"
        self.images = self.game / "images/college"
        self.story = self.game / "40_story/prologue/chapter.rpy"
        self.images.mkdir(parents=True)
        self.story.parent.mkdir(parents=True)
        self.story.write_text('label arrive_college:\n    scene bg_college\n'
                              '    "Maya arrived at the campus entrance."\n', encoding="utf-8")
        self.image = self.images / "unused_picture.jpg"
        self.image.write_bytes(b"unused-content")

    def tearDown(self):
        self.temporary.cleanup()

    def add_target(self):
        story_file = "40_story/prologue/chapter.rpy"
        dialogue = "Maya arrived at the campus entrance."
        sidecar = {"role": "cg", "category": "college", "story_file": story_file,
                   "story_label": "arrive_college", "dialogue_contains": dialogue,
                   "story_key": story_request_id(story_file, "arrive_college", dialogue)}
        self.image.with_suffix(".json").write_text(json.dumps(sidecar), encoding="utf-8")

    def test_filename_rule_never_selects_dialogue(self):
        proposals, review = plan_reconciliation(self.game)
        self.assertFalse(proposals)
        self.assertIn("No curated filename rule", review[0][2])

    def test_curated_filename_rule_suggests_unique_story_target(self):
        self.story.write_text('label arrive_college:\n'
                              '    scene bg_college\n'
                              '    "The building was huge."\n', encoding="utf-8")
        self.image.unlink()
        self.image = self.images / "Maya_arriving_at_college_entrance.jpg"
        self.image.write_bytes(b"curated-match")
        proposals, review = plan_reconciliation(self.game)
        self.assertEqual(len(proposals), 1)
        self.assertFalse(review)
        self.assertIn("College arrival", proposals[0][2])
        apply_reconciliation(proposals)
        metadata = json.loads(self.image.with_suffix(".json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["story_label"], "arrive_college")
        self.assertTrue(metadata["story_key"].startswith("story_"))

    def test_exact_request_places_and_updates_inventory_sidecar(self):
        self.add_target()
        proposals, review = plan_reconciliation(self.game)
        self.assertEqual(len(proposals), 1)
        self.assertFalse(review)
        apply_reconciliation(proposals)
        self.assertIn(f"scene {proposals[0][0]}", self.story.read_text(encoding="utf-8"))
        metadata = json.loads(self.image.with_suffix(".json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["placement_status"], "placed")
        self.assertTrue(metadata["asset_id"].startswith("asset_"))


if __name__ == "__main__":
    unittest.main()
