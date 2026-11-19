"""Unit tests for CLI-Anything LOLA Music & Colab harness."""

import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from click.testing import CliRunner

from audio_toolkit import music_cli


class MusicCliTests(unittest.TestCase):
    def test_status_json_and_colab_pack_unpack(self):
        runner = CliRunner()
        res = runner.invoke(music_cli.cli, ["--json", "status"])
        self.assertEqual(res.exit_code, 0)
        data = json.loads(res.output)
        self.assertIn("audio_mb", data)
        self.assertIn("mp3_tracks", data)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lofi = root / "lofi"
            stems = root / "stems"
            lofi.mkdir()
            (lofi / "demo.mp3").write_bytes(b"mp3-data")
            orig_lofi, orig_stems = music_cli.LOFI_DIR, music_cli.STEMS_DIR
            try:
                music_cli.LOFI_DIR = lofi
                music_cli.STEMS_DIR = stems
                pack_zip = root / "pack.zip"
                pack_res = runner.invoke(music_cli.cli, ["--json", "colab", "pack", "--out", str(pack_zip)])
                self.assertEqual(pack_res.exit_code, 0)
                self.assertTrue(pack_zip.is_file())
                with zipfile.ZipFile(pack_zip) as zf:
                    self.assertIn("demo.mp3", zf.namelist())

                # Verify unpack extracts ogg + stems and reports cleanly
                export_zip = root / "export.zip"
                with zipfile.ZipFile(export_zip, "w") as zf:
                    zf.writestr("ogg/demo.ogg", b"ogg-bytes")
                    zf.writestr("stems/demo/layer_base.ogg", b"base-bytes")
                unpack_res = runner.invoke(music_cli.cli, ["--json", "colab", "unpack", str(export_zip), "--no-replace-mp3"]
                                           if "--no-replace-mp3" in music_cli.colab_unpack.params else ["--json", "colab", "unpack", str(export_zip)])
                self.assertEqual(unpack_res.exit_code, 0)
                self.assertTrue((lofi / "demo.ogg").is_file())
                self.assertTrue((stems / "demo" / "layer_base.ogg").is_file())
            finally:
                music_cli.LOFI_DIR, music_cli.STEMS_DIR = orig_lofi, orig_stems


if __name__ == "__main__":
    unittest.main()
