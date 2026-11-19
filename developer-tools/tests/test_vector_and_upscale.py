"""
Unit test for Vector Icon conversion and Lanczos Background Upscaling.
"""
import unittest
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from image_audit.vector_and_upscale import convert_icons_to_svg, upscale_background_lanczos

class TestVectorAndUpscale(unittest.TestCase):
    def test_svg_conversion_output(self):
        svg_folder = "game/images/ui/svg_icons"
        self.assertTrue(os.path.exists(svg_folder))
        svg_files = [f for f in os.listdir(svg_folder) if f.endswith(".svg")]
        self.assertGreaterEqual(len(svg_files), 35)

    def test_upscale_lanczos(self):
        test_img_path = "game/images/ui/test_temp_upscale.png"
        img = Image.new("RGB", (100, 100), color=(120, 50, 200))
        img.save(test_img_path)
        try:
            res = upscale_background_lanczos(test_img_path, target_width=200, target_height=200)
            self.assertTrue(res)
            with Image.open(test_img_path) as up:
                self.assertEqual(up.size, (200, 200))
        finally:
            if os.path.exists(test_img_path):
                os.remove(test_img_path)

if __name__ == "__main__":
    unittest.main()
