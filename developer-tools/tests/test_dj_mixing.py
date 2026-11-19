"""Unit tests for Camelot harmonic mixing, DJ planner, and NumPy mastering."""

import unittest
import numpy as np

from audio_toolkit.camelot import camelot_compatibility, to_camelot
from audio_toolkit.dj_planner import build_mix_plan, score_transition
from audio_toolkit.mastering import equal_power_crossfade, match_rms_loudness


class DjMixingTests(unittest.TestCase):
    def test_camelot_wheel_scores_adjacent_higher_than_clash(self):
        self.assertEqual(to_camelot("C Minor"), "5A")
        self.assertEqual(to_camelot("G Minor"), "6A")
        self.assertGreater(camelot_compatibility("C Minor", "G Minor"),
                           camelot_compatibility("C Minor", "F-Sharp Minor"))

    def test_dj_mix_plan_ranks_compatible_tracks(self):
        plan = build_mix_plan()
        self.assertIn("downtown_glow", plan["tracks"])
        next_list = plan["tracks"]["downtown_glow"]["next_tracks"]
        self.assertTrue(len(next_list) >= 3)
        self.assertGreaterEqual(next_list[0]["score"], next_list[-1]["score"])

    def test_equal_power_crossfade_and_rms_limiter(self):
        sr = 44100
        a = np.ones(sr, dtype=np.float32) * 0.5
        b = np.ones(sr, dtype=np.float32) * 0.5
        blended = equal_power_crossfade(a, b)
        self.assertEqual(len(blended), sr)
        self.assertGreater(float(np.min(blended)), 0.49)
        limited = match_rms_loudness(a * 4.0, target_rms_db=-14.0)
        self.assertLessEqual(float(np.max(np.abs(limited))), 0.90)


if __name__ == "__main__":
    unittest.main()
