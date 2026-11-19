"""
CLI Tool for fast story queries, additions, updates, and integrity checks.
"""
import sys
import json
from .narrative_db import StoryDatabase

def populate_default_story():
    db = StoryDatabase()
    beats = [
        ("BEAT_01_PROL_MIRROR", "Prologue", "Day_01", 3, "Crisis/Hook",
         "Eviction notice pinned behind cracked mirror; $120 left in city",
         "If Maya cannot secure a financial foothold in 7 days, she is on the streets",
         "morning_wake"),
        ("BEAT_02_BUS_COMMUTE", "Prologue", "Day_01", 4, "Observation/Con",
         "Commuter drop-wallet bluff test at crowded express line",
         "Testing social leverage without blowing innocent student cover",
         "daily_commute"),
        ("BEAT_03_CAMPUS_GATES", "Prologue", "Day_01", 5, "Social Infiltration",
         "Infiltrating elite university circle under false pretense of scholarship kid",
         "Discovery risks immediate expulsion and criminal trespass",
         "college_social"),
        ("BEAT_04_ELENA_PACT", "Prologue", "Day_01", 6, "Alliance/Vulnerability",
         "Elena notices Maya's altered transcript slip; offers alliance instead of reporting",
         "Elena holds Maya's secret; Maya must discover Elena's leverage",
         "study_focus"),
        ("BEAT_05_MARCUS_LEVERAGE", "Prologue", "Day_01", 7, "Underground Economics",
         "Cafe shift doubles as laundering hub for downtown nightlife debts",
         "Marcus offers quick illegal cash vs steady clean wages",
         "con_tension"),
    ]
    for b in beats:
        db.upsert_beat(*b)
    print(f"Populated {len(beats)} foundational high-stakes narrative beats into SQLite.")

if __name__ == "__main__":
    populate_default_story()
