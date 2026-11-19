"""Tests for stable, image-driven looping story assets."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from image_story_loop.catalog import build_catalog
from image_story_loop.narrative import event_key, story_event


class ImageStoryLoopTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.game = Path(self.temporary.name) / "game"
        self.images = self.game / "images"
        self.images.mkdir(parents=True)

    def tearDown(self):
        self.temporary.cleanup()

    def test_variants_share_a_story_moment_and_reference_art_is_excluded(self):
        folder = self.images / "transport"
        folder.mkdir()
        first = folder / "Girl_waiting_for_bus_12345678.jpg"
        second = folder / "Girl_waiting_for_bus_abcdef12.jpg"
        first.write_bytes(b"first image")
        second.write_bytes(b"second image")
        reference = self.images / "character_reference"
        reference.mkdir()
        (reference / "Girl_turnaround_87654321.jpg").write_bytes(b"reference")

        catalog = build_catalog(self.game)
        self.assertEqual(len(catalog["events"]), 1)
        event = catalog["events"][0]
        self.assertEqual(event_key(first), "girl waiting for bus")
        self.assertEqual(event["title"], "Girl Waiting For Bus")
        self.assertEqual(len(event["images"]), 2)
        self.assertIn("waited for a bus at the bus stop", event["narration"])

    def test_generated_art_excluded_and_location_prefixes_parsed(self):
        gen = self.images / "generated_art"
        gen.mkdir()
        (gen / "grok-image-12345678.jpg").write_bytes(b"gen1")
        food = self.images / "food_drink"
        food.mkdir()
        (food / "grok-image-abcdef12.jpg").write_bytes(b"gen2")
        loc = food / "__LOCATION____[(Sunny_vineyard_+_tasting_bc5747bc.jpg"
        loc.write_bytes(b"vineyard")
        catalog = build_catalog(self.game)
        self.assertEqual(len(catalog["events"]), 1)
        ev = catalog["events"][0]
        self.assertEqual(ev["category"], "food_drink")
        self.assertFalse(ev["title"].startswith(("Irl ", "Aya ", "Oman ")))
        self.assertNotIn("uncaptioned moment", ev["narration"])

    def test_exact_copy_is_skipped_without_skipping_distinct_moments(self):
        folder = self.images / "shops_markets"
        folder.mkdir()
        first = folder / "Girl_buying_flowers_at_market_12345678.jpg"
        copy = folder / "Girl_buying_flowers_at_market_12345678 (1).jpg"
        other = folder / "Girl_browsing_records_at_fair_abcdefgh.jpg"
        first.write_bytes(b"same image")
        copy.write_bytes(b"same image")
        other.write_bytes(b"different image")

        catalog = build_catalog(self.game)
        self.assertEqual(len(catalog["events"]), 2)
        self.assertEqual(len(catalog["exact_duplicates_skipped"]), 1)

    def test_current_story_art_is_not_added_twice(self):
        folder = self.images / "college"
        folder.mkdir()
        image = folder / "Girl_entering_classroom_12345678.jpg"
        image.write_bytes(b"class image")
        definitions = self.game / "10_characters"
        story = self.game / "40_story"
        definitions.mkdir()
        story.mkdir()
        (definitions / "art.rpy").write_text(
            'image cg_class = fit_scene_art("images/college/Girl_entering_classroom_12345678.jpg")\n',
            encoding="utf-8")
        (story / "day.rpy").write_text("label day:\n    scene cg_class\n", encoding="utf-8")

        self.assertEqual(build_catalog(self.game)["events"], [])


if __name__ == "__main__":
    unittest.main()
