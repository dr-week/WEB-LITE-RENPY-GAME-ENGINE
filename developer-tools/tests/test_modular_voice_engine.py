import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.modular_voice_engine.core.dialogue_scanner import scan_maya_lines, voice_coverage, write_voice_manifest
from modules.modular_voice_engine.core.emotion_profiles import EMOTION_TTS, line_hash, stylize_genz_mumble


class ModularVoiceEngineTests(unittest.TestCase):
    def test_line_hash_and_genz_stylize(self):
        self.assertEqual(line_hash("Hey there!", "happy"), line_hash("Hey   there!", "happy"))
        self.assertNotEqual(line_hash("Hey there!", "happy"), line_hash("Hey there!", "tired"))
        self.assertIn("happy", EMOTION_TTS)
        self.assertTrue(stylize_genz_mumble("that's wild", "teasing").startswith("wait, seriously?"))

    def test_scan_maya_lines_manifest_and_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            story = root / "story.rpy"
            story.write_text('$ set_emotional_state("teasing")\nmaya "Watch me work."\nmaya_thought "Stay cool."\n', encoding="utf-8")
            items = scan_maya_lines(root)
            self.assertEqual(len(items), 2)
            out = root / "voice_manifest.json"
            res = write_voice_manifest(root, out)
            self.assertEqual(res["count"], 2)
            cov = voice_coverage(root, root / "tts")
            self.assertEqual(cov["total_lines"], 2)
            self.assertEqual(cov["mumble_fallback"], 2)


if __name__ == "__main__":
    unittest.main()
