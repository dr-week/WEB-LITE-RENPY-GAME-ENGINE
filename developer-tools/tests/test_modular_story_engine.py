import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.modular_story_engine.checks.menu_remixer import remix_story_menus
from modules.modular_story_engine.checks.two_option_validator import count_menu_options, validate_two_option_rule
from modules.modular_story_engine.core.micro_dialogue import make_maya_line
from modules.modular_story_engine.generator.beat_generator import build_beat_spec, render_rpy_beat
from modules.modular_story_engine.generator.day_builder import build_day_arc


class ModularStoryEngineTests(unittest.TestCase):
    def test_micro_dialogue_is_ultra_short(self):
        for tone in ("hustle", "cozy", "tense", "playful"):
            line = make_maya_line(tone, seed=3)
            self.assertLessEqual(len(line.split()), 5)
            self.assertLessEqual(len(make_maya_line(tone, seed=3, thought=True).split()), 3)

    def test_generated_beat_has_two_options_tone_district_and_flags(self):
        rpy = render_rpy_beat(build_beat_spec("day_08_pier_beat", location="harbor_pier", tone="tense", seed=12))
        self.assertIn("label day_08_pier_beat:", rpy)
        self.assertIn("play sound SFX_SWOOSH_SOFT", rpy)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "beat.rpy"
            p.write_text(rpy, encoding="utf-8")
            menus = count_menu_options(p)
            self.assertEqual(len(menus), 1)
            self.assertEqual(menus[0]["options"], 2)

    def test_create_day_chains_three_slots_and_updates_sqlite(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_file = Path(tmp) / "arcs.db"
            res = build_day_arc(8, theme="harbor_twilight", seed=5, sync_db=True, db_path=str(db_file))
            self.assertEqual(len(res["beats"]), 3)
            self.assertIn("maya_thought", res["rpy"])
            self.assertIn("jump end_day_home", res["rpy"])
            conn = sqlite3.connect(db_file)
            rows = conn.execute("SELECT beat_id FROM story_beats").fetchall()
            conn.close()
            self.assertEqual(len(rows), 3)

    def test_validator_and_remixer_on_three_option_menu(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.rpy"
            p.write_text(
                'label x:\n    menu:\n'
                '        "Option A":\n            $ change_stat("appeal", 2)\n'
                '        "Option B":\n            $ change_stat("intelligence", 3)\n'
                '        "Option C":\n            $ change_stat("energy", 5)\n',
                encoding="utf-8",
            )
            self.assertFalse(validate_two_option_rule(Path(tmp))["ok"])
            rep = remix_story_menus(Path(tmp), apply=True)
            self.assertEqual(rep["remixed_count"], 1)
            self.assertEqual(rep["menus"][0]["discarded"], ["Option B"])
            self.assertTrue(validate_two_option_rule(Path(tmp))["ok"])
            self.assertIn('change_stat("intelligence", 3)', p.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
