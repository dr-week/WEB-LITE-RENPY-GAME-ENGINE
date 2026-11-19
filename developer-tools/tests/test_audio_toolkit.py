"""
Tests for AudioRemixer and WavMixer.
"""
import unittest
import os
import json
from audio_toolkit.audio_remixer import AudioRemixer
from audio_toolkit.wav_mixer import WavMixer

class TestAudioToolkit(unittest.TestCase):
    def test_audio_database_loaded(self):
        remixer = AudioRemixer(db_path="game/audio/music_database.json")
        self.assertGreaterEqual(len(remixer.tracks), 7)

    def test_compatible_bpm_matching(self):
        remixer = AudioRemixer(db_path="game/audio/music_database.json")
        # morning_routine is 75 BPM, little_wishes is 76 BPM
        compat = remixer.find_compatible_mixes("morning_routine", max_bpm_diff=3)
        found_ids = [c["track"]["id"] for c in compat]
        self.assertIn("little_wishes", found_ids)

    def test_wav_overlay(self):
        sr = 44100
        music = [0.1] * (sr * 2)
        sfx = [0.5] * sr
        mixed = WavMixer.overlay_sfx(music, sfx, start_sec=0.5, sr=sr, sfx_vol=1.0)
        self.assertEqual(len(mixed), len(music))
        self.assertAlmostEqual(mixed[int(0.6 * sr)], 0.6)

if __name__ == "__main__":
    unittest.main()
