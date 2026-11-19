"""Harmonic + BPM DJ transition planner reading game/audio/music_database.json."""

import argparse
import json
from pathlib import Path

from .camelot import camelot_compatibility, to_camelot

ROOT = Path(__file__).resolve().parents[2]
MUSIC_DB = ROOT / "game" / "audio" / "music_database.json"
MIX_PLAN = ROOT / "game" / "audio" / "dj_mix_plan.json"


def score_transition(track_a: dict, track_b: dict) -> float:
    """Score a DJ transition from track_a to track_b (higher = smoother mix)."""
    harmonic = camelot_compatibility(track_a.get("key", ""), track_b.get("key", ""))
    bpm_diff = abs(float(track_a.get("bpm", 80)) - float(track_b.get("bpm", 80)))
    bpm_score = max(0.0, 1.0 - (bpm_diff / 14.0))
    energy_diff = abs(float(track_a.get("energy", 0.5)) - float(track_b.get("energy", 0.5)))
    energy_score = max(0.0, 1.0 - energy_diff)
    return round(0.50 * harmonic + 0.35 * bpm_score + 0.15 * energy_score, 3)


def build_mix_plan(db_path: Path = MUSIC_DB, top_k: int = 4) -> dict:
    """Build ranked compatible next-track recommendations for every track in the DB."""
    tracks = json.loads(db_path.read_text(encoding="utf-8-sig"))
    plan = {}
    for src in tracks:
        candidates = []
        for dst in tracks:
            if dst["id"] == src["id"]:
                continue
            cues = dst.get("cue_points", {})
            entry_sec = float(cues.get("beat_drop", cues.get("intro", 0.0)))
            candidates.append({
                "id": dst["id"],
                "title": dst["title"],
                "audio_file": dst["audio_file"].replace("game/", "", 1),
                "bpm": dst["bpm"],
                "camelot": to_camelot(dst.get("key", "")),
                "entry_sec": entry_sec,
                "bridge_sec": float(cues.get("bridge", entry_sec)),
                "score": score_transition(src, dst),
            })
        candidates.sort(key=lambda item: -item["score"])
        plan[src["id"]] = {
            "title": src["title"],
            "bpm": src["bpm"],
            "camelot": to_camelot(src.get("key", "")),
            "next_tracks": candidates[:top_k],
        }
    return {"schema_version": 1, "tracks": plan}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=MUSIC_DB)
    parser.add_argument("--out", type=Path, default=MIX_PLAN)
    args = parser.parse_args()
    plan = build_mix_plan(args.db)
    args.out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {args.out} for {len(plan['tracks'])} tracks.")


if __name__ == "__main__":
    main()
