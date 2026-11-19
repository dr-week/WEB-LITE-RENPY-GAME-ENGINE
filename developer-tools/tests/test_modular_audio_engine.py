"""
Unit tests for the standalone Modular Audio Engine package.
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from modules.modular_audio_engine import AudioCatalog, MixPlanner, SfxGenerator, RenpyAudioAdapter

class TestModularAudioEngine(unittest.TestCase):
    def setUp(self):
        self.catalog = AudioCatalog("game/audio/music_database.json")
        self.planner = MixPlanner(self.catalog)

    def test_catalog_loaded_all_sixteen_tracks(self):
        self.assertEqual(len(self.catalog.tracks), 16)

    def test_planner_bpm_matches(self):
        matches = self.planner.find_beatmatches("vibin", max_bpm_delta=2)
        matched_ids = [m["track"]["id"] for m in matches]
        self.assertIn("morning_routine", matched_ids)
        self.assertIn("on_my_way", matched_ids)

    def test_mid_beat_offset_calculation(self):
        # 75 BPM track: 1 beat = 0.8s; beat 16 = 12.8s
        sec = self.planner.calculate_beat_offset("vibin", beat_index=16)
        self.assertAlmostEqual(sec, 12.8, delta=0.1)

    def test_cue_offset_retrieval(self):
        drop_sec = self.planner.get_cue_offset("vibin", "beat_drop")
        self.assertEqual(drop_sec, 12.8)

    def test_sfx_generator_buffers(self):
        riser = SfxGenerator.generate_riser(duration=0.5, sr=22050)
        boom = SfxGenerator.generate_boom(duration=0.5, sr=22050)
        scratch = SfxGenerator.generate_scratch(duration=0.2, sr=22050)
        self.assertEqual(len(riser), int(0.5 * 22050))
        self.assertEqual(len(boom), int(0.5 * 22050))
        self.assertEqual(len(scratch), int(0.2 * 22050))

    def test_renpy_adapter_statements(self):
        track = self.catalog.get_track("downtown_glow")
        cmd = RenpyAudioAdapter.play_track(track, fadein=3.0)
        self.assertIn('renpy.music.play("audio/music/lofi/downtown_glow.mp3"', cmd)

if __name__ == "__main__":
    unittest.main()
