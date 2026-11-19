"""Unit tests for lightweight visual quality inspection."""

import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

from image_quality import inspect_image


class ImageQualityTests(unittest.TestCase):
    def test_valid_hd_scene_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scene.jpg"
            img = Image.new("RGB", (1376, 768), (110, 125, 145))
            draw = ImageDraw.Draw(img)
            for x in range(0, 1376, 40):
                draw.line([(x, 0), (x, 768)], fill=(220, 200, 180), width=4)
            img.save(path)
            result = inspect_image(path)
            self.assertTrue(result["ok"])
            self.assertEqual(result["status"], "pass")
            self.assertEqual((result["width"], result["height"]), (1376, 768))

    def test_blank_dark_image_warns_and_scores_low(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dark.png"
            Image.new("RGB", (1280, 720), (3, 3, 3)).save(path)
            result = inspect_image(path)
            self.assertTrue(result["ok"])
            self.assertEqual(result["status"], "warn")
            self.assertIn("too_dark", result["flags"])
            self.assertLess(result["quality_score"], 75)

    def test_corrupt_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.jpg"
            path.write_bytes(b"not-a-valid-image")
            result = inspect_image(path)
            self.assertFalse(result["ok"])
            self.assertEqual(result["status"], "fail")


if __name__ == "__main__":
    unittest.main()
