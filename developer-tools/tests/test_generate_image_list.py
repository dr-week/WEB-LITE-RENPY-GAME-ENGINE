import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import generate_image_list as generator
from image_generation.prompts import starter_egg
from image_generation.targets import story_targets


class GenerationListFlowTests(unittest.TestCase):
    def test_story_target_catalog_only_offers_unique_unillustrated_lines(self):
        rows = [
            ("arrival", "bg_campus", "bg_campus", 10, "Maya paused at the crowded campus entrance.", "40_story/day.rpy"),
            ("arrival", "cg_arrival", "bg_campus", 12, "Maya smiled at her new classmate.", "40_story/day.rpy"),
            ("arrival", "bg_campus", "bg_campus", 14, "Maya paused at the crowded campus entrance.", "40_story/day.rpy"),
        ]
        self.assertEqual(story_targets(rows), [])
        unique = story_targets(rows[:2])
        self.assertEqual(len(unique), 1)
        self.assertEqual(unique[0]["storyLabel"], "arrival")
        self.assertEqual(unique[0]["line"], 10)

    def test_story_dialogue_creates_one_tagged_request_then_stops_repeating(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            game = root / "game"
            (game / "images/home_lodging").mkdir(parents=True)
            (game / "images/character_reference").mkdir(parents=True)
            (game / "10_characters").mkdir()
            (game / "40_story/prologue").mkdir(parents=True)
            (game / "images/home_lodging/home.jpg").write_bytes(b"ref")
            (game / "images/character_reference/hero_posing_in_blue_outfit.jpg").write_bytes(b"ref")
            (game / "10_characters/scene.rpy").write_text(
                'image bg_home = fit_scene_art("images/home_lodging/home.jpg")\n', encoding="utf-8")
            story = game / "40_story/prologue/day.rpy"
            story.write_text(
                'label day_03_home:\n'
                '    scene bg_home\n'
                '    "Maya felt tired and unsure in the unfamiliar city."\n'
                '    "Maya checked a folded day planner before leaving."\n', encoding="utf-8")

            original_game = generator.GAME
            try:
                generator.GAME = game
                definitions, events, lines = generator.scan()
                first, existing = generator.fresh_story_beats(definitions, events, lines)
                self.assertEqual(len(first), 1)
                self.assertFalse(existing)
                request = first[0]
                self.assertIn("checked a folded day planner", request["dialogue"])
                self.assertIn("images/character_reference/hero_posing_in_blue_outfit.jpg",
                              request["references"])
                self.assertEqual(request["metadata"]["story_key"], request["key"])
                self.assertEqual(request["starter_egg"], starter_egg(request["key"]))
                self.assertIn("[STARTER_EGG:", request["prompt"])
                _, catalog = generator.build_outputs()
                catalog_item = next(item for item in catalog["requests"] if item["storyKey"] == request["key"])
                self.assertEqual(catalog_item["storyFile"], request["source"])
                self.assertEqual(catalog_item["dialogueContains"], request["dialogue"])

                generated = game / "images/home_lodging" / f"{request['key']}.jpg"
                generated.write_bytes(b"generated")
                generated.with_suffix(".json").write_text(
                    json.dumps(request["metadata"]), encoding="utf-8")
                first, existing = generator.fresh_story_beats(definitions, events, lines)
                self.assertFalse(first)
                self.assertEqual(existing[0][0], request["key"])

                generated.with_suffix(".json").unlink()
                first, existing = generator.fresh_story_beats(definitions, events, lines)
                self.assertFalse(first)
                self.assertEqual(existing[0][0], request["key"])

                with (game / "10_characters/scene.rpy").open("a", encoding="utf-8") as output:
                    output.write(f'image cg_{request["key"]} = fit_scene_art("images/home_lodging/{generated.name}")\n')
                story.write_text(
                    'label day_03_home:\n'
                    '    scene bg_home\n'
                    f'    scene cg_{request["key"]}\n'
                    '    with dissolve\n'
                    '    "Maya checked a folded day planner before leaving."\n', encoding="utf-8")
                definitions, events, lines = generator.scan()
                first, existing = generator.fresh_story_beats(definitions, events, lines)
                self.assertFalse(first)
                self.assertFalse(existing)
            finally:
                generator.GAME = original_game


if __name__ == "__main__":
    unittest.main()
