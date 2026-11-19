"""
Unit tests for Overlapping Sound Effects, Transition Engine, and Audio Curves.
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from modules.modular_audio_engine.transitions.crossfader.audio_curves import AudioCurves
from modules.modular_audio_engine.transitions.layering.sfx_overlap_mixer import SfxOverlapMixer
from modules.modular_audio_engine.transitions.transition_engine import TransitionEngine

class TestAudioTransitions(unittest.TestCase):
    def test_equal_power_sum_of_squares(self):
        for p in [0.0, 0.25, 0.5, 0.75, 1.0]:
            f_out = AudioCurves.equal_power_fade_out(p)
            f_in = AudioCurves.equal_power_fade_in(p)
            # sin^2 + cos^2 = 1.0
            sum_sq = (f_out ** 2) + (f_in ** 2)
            self.assertAlmostEqual(sum_sq, 1.0, places=4)

    def test_overlap_mixer_length_and_gain(self):
        sfx_a = [0.4] * 1000
        sfx_b = [0.6] * 1000
        mixed = SfxOverlapMixer.mix_two_sfx(sfx_a, sfx_b, delay_sec=0.01, gain_a=1.0, gain_b=1.0, sr=10000)
        # Offset is 100 samples (0.01 * 10000)
        # Total length: max(1000, 100 + 1000) = 1100
        self.assertEqual(len(mixed), 1100)
        # In the overlap zone (at index 200), sample = 0.4 + 0.6 = 1.0
        self.assertAlmostEqual(mixed[200], 1.0)

    def test_random_transition_presets(self):
        preset = TransitionEngine.get_random_transition()
        self.assertIn("sfx_lead", preset)
        self.assertIn("sfx_tail", preset)
        self.assertGreater(preset["fade_time"], 0.5)

if __name__ == "__main__":
    unittest.main()
