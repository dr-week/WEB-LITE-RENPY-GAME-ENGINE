"""
Unit tests for the Story Narrative SQLite Database.
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from story_db.narrative_db import StoryDatabase

class NarrativeDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.db_path = "data/story_engine/test_narrative.db"
        self.db = StoryDatabase(self.db_path)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_upsert_and_retrieve_beat(self):
        self.db.upsert_beat(
            beat_id="TEST_BEAT_01",
            act="Act_1",
            chapter="Day_01",
            tension=8,
            scene_type="Climax",
            hook="Stolen phone rings with the mob boss's number",
            stakes="Survival vs Arrest",
            music="crisis_debt"
        )
        beat = self.db.get_beat("TEST_BEAT_01")
        self.assertIsNotNone(beat)
        self.assertEqual(beat["tension_level"], 8)
        self.assertEqual(beat["hook_description"], "Stolen phone rings with the mob boss's number")

    def test_list_and_delete_beat(self):
        self.db.upsert_beat("BEAT_A", "Act_1", "Day_02", 4, "Normal", "Hook A", "Stakes A")
        self.db.upsert_beat("BEAT_B", "Act_1", "Day_02", 7, "High", "Hook B", "Stakes B")
        beats = self.db.list_chapter_beats("Day_02")
        self.assertEqual(len(beats), 2)
        # Verify sorted by tension
        self.assertEqual(beats[0]["beat_id"], "BEAT_A")
        self.assertEqual(beats[1]["beat_id"], "BEAT_B")

        self.db.delete_beat("BEAT_A")
        updated = self.db.list_chapter_beats("Day_02")
        self.assertEqual(len(updated), 1)
        self.assertEqual(updated[0]["beat_id"], "BEAT_B")

if __name__ == "__main__":
    unittest.main()
