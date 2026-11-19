import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from image_generation.identity import story_request_id
from image_import.core import plan_imports
from integrate_story_images import apply_import


class ImageRoutingTests(unittest.TestCase):
    def make_project(self, metadata=None, name="college_entrance.jpg"):
        root = Path(self.temporary.name)
        images = root / "game/images"
        story_dir = root / "game/40_story/prologue"
        (root / "game/10_characters").mkdir(parents=True)
        images.mkdir(parents=True)
        story_dir.mkdir(parents=True)
        story = story_dir / "chapter.rpy"
        story.write_text('label arrive_college:\n    scene bg_college\n'
                         '    "Maya arrived at the campus entrance."\n', encoding="utf-8")
        image = images / name
        image.write_bytes(b"unique-image-bytes")
        if metadata is not None:
            image.with_suffix(".json").write_text(json.dumps(metadata), encoding="utf-8")
        return root, story, image

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary.cleanup()

    def test_filename_suggests_category_but_never_places_story(self):
        root, _, _ = self.make_project()
        _, plans = plan_imports(root)
        self.assertEqual(len(plans), 1)
        self.assertIsNone(plans[0].target)
        self.assertIn("No exact sidecar target", plans[0].review)

    def test_request_id_routes_exact_dialogue_and_writes_asset_identity(self):
        story_file = "40_story/prologue/chapter.rpy"
        label, dialogue = "arrive_college", "Maya arrived at the campus entrance."
        metadata = {"category": "college", "role": "cg", "story_file": story_file,
                    "story_label": label, "dialogue_contains": dialogue,
                    "story_key": story_request_id(story_file, label, dialogue)}
        root, story, image = self.make_project(metadata)
        game, plans = plan_imports(root)
        self.assertEqual(plans[0].metadata["story_key"], metadata["story_key"])
        apply_import(game, plans)
        placed = game / "images/college" / image.name
        result = json.loads(placed.with_suffix(".json").read_text(encoding="utf-8"))
        self.assertEqual(result["placement_status"], "placed")
        self.assertTrue(result["asset_id"].startswith("asset_"))
        self.assertIn(f"scene {plans[0].alias}", story.read_text(encoding="utf-8"))

    def test_stale_request_id_is_rejected(self):
        metadata = {"story_file": "40_story/prologue/chapter.rpy",
                    "story_label": "arrive_college", "dialogue_contains": "Maya arrived",
                    "story_key": "story_deadbeef00"}
        root, _, _ = self.make_project(metadata)
        with self.assertRaisesRegex(ValueError, "does not match target request"):
            plan_imports(root)

    def test_reference_role_never_gets_a_scene_alias(self):
        root, _, _ = self.make_project({"role": "reference", "category": "college"}, "maya_reference.png")
        _, plans = plan_imports(root)
        self.assertIsNone(plans[0].alias)
        self.assertEqual(plans[0].destination.parent.name, "character_reference")

    def test_content_already_imported_is_rejected_after_rename(self):
        story_file = "40_story/prologue/chapter.rpy"
        dialogue = "Maya arrived at the campus entrance."
        metadata = {"category": "college", "role": "cg", "story_file": story_file,
                    "story_label": "arrive_college", "dialogue_contains": dialogue,
                    "story_key": story_request_id(story_file, "arrive_college", dialogue)}
        root, _, image = self.make_project(metadata)
        image_bytes = image.read_bytes()
        game, plans = plan_imports(root)
        apply_import(game, plans)
        duplicate = root / "game/images/renamed-copy.jpg"
        duplicate.write_bytes(image_bytes)
        with self.assertRaisesRegex(ValueError, "Duplicate asset content"):
            plan_imports(root)


if __name__ == "__main__":
    unittest.main()
