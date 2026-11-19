"""Tests for story prompt manifest generation and Flow download ingestion."""

import json
import tempfile
import unittest
from pathlib import Path
from image_generation.menu_prompts import generate_menu_prompts
from ingest_flow_download import ingest_file


class FlowIngestTests(unittest.TestCase):
    def test_story_prompt_has_asset_id_and_ingests_generic_download(self):
        items = generate_menu_prompts(2, seed=42, menu_mode=False)
        self.assertEqual(len(items), 2)
        self.assertTrue(items[0]["asset_id"])
        self.assertIn("[ASSET_ID:", items[0]["prompt"])
        self.assertIn("[PHYSICS:", items[0]["prompt"])
        self.assertIn("extra legs", items[0]["prompt"])
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manifest = tmp_path / "manifest.json"
            manifest.write_text(json.dumps([
                {"asset_id": items[0]["asset_id"], "category": items[0]["category"], "suggested_filename": items[0]["suggested_filename"]},
            ]), encoding="utf-8")
            src = tmp_path / "image (1).png"
            src.write_bytes(b"fake-png-data")
            dest = ingest_file(src, items[0]["asset_id"], manifest_path=manifest, images_dir=tmp_path / "images")
            self.assertTrue(dest.is_file())
            self.assertEqual(dest.name, f"{items[0]['asset_id']}.png")
            self.assertTrue(dest.with_suffix(".json").is_file())


if __name__ == "__main__":
    unittest.main()
