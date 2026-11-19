import json
import tempfile
import unittest
from pathlib import Path
from click.testing import CliRunner

import cli_anything_lola_flow as cli_mod
from ingest_flow_download import ingest_file


class CliAnythingFlowTests(unittest.TestCase):
    def test_prompt_menu_json_and_session_update(self):
        runner = CliRunner()
        res = runner.invoke(cli_mod.cli, ["--json", "prompt", "menu", "--count", "2", "--seed", "7"])
        self.assertEqual(res.exit_code, 0, res.output)
        data = json.loads(res.output)
        self.assertTrue(data["ok"])
        self.assertEqual(data["count"], 2)
        sess = json.loads(runner.invoke(cli_mod.cli, ["--json", "session"]).output)
        self.assertEqual(sess["last_count"], 2)
        self.assertEqual(len(sess["last_asset_ids"]), 2)

    def test_prompt_story_json_output(self):
        runner = CliRunner()
        res = runner.invoke(cli_mod.cli, ["--json", "prompt", "story"])
        self.assertEqual(res.exit_code, 0, res.output)
        data = json.loads(res.output)
        self.assertTrue(data["ok"])
        self.assertIn("open_count", data)

    def test_ingest_file_writes_sidecar_and_moves_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps([{"asset_id": "menu_test_01", "category": "menu_assets", "title": "Test"}]), encoding="utf-8")
            src = root / "raw_download.png"
            src.write_bytes(b"fake-png-bytes")
            dest = ingest_file(src, "menu_test_01", manifest_path=manifest, images_dir=root / "images")
            self.assertTrue(dest.is_file())
            self.assertFalse(src.exists())
            meta = json.loads(dest.with_suffix(".json").read_text(encoding="utf-8"))
            self.assertEqual(meta["asset_id"], "menu_test_01")
            self.assertIn("sha256", meta)


if __name__ == "__main__":
    unittest.main()
