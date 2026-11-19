"""
Mix Planner: Computes BPM beatmatching, harmonic key compatibility,
scene energy curves, and mid-track beat jump calculations.
"""
from ..catalog.audio_catalog import AudioCatalog

class MixPlanner:
    def __init__(self, catalog=None):
        self.catalog = catalog or AudioCatalog()

    def find_beatmatches(self, track_id, max_bpm_delta=4):
        """Find tracks with compatible BPM for smooth tempo transitions."""
        target = self.catalog.get_track(track_id)
        if not target:
            return []
        matches = []
        for t in self.catalog.tracks:
            if t["id"] != track_id:
                delta = abs(t["bpm"] - target["bpm"])
                if delta <= max_bpm_delta:
                    matches.append({
                        "track": t,
                        "bpm_delta": delta,
                        "transition_recommended": "crossfade_4s" if delta <= 2 else "beat_sync_riser"
                    })
        matches.sort(key=lambda x: x["bpm_delta"])
        return matches

    def calculate_beat_offset(self, track_id, beat_index=16):
        """Calculate start time in seconds for jumping into any specific beat."""
        track = self.catalog.get_track(track_id)
        if not track:
            return 0.0
        bpm = track.get("bpm", 75)
        sec_per_beat = 60.0 / bpm
        return round(beat_index * sec_per_beat, 2)

    def get_cue_offset(self, track_id, cue_name="beat_drop"):
        """Get exact second offset for named cue (intro, beat_drop, bridge, outro)."""
        track = self.catalog.get_track(track_id)
        if not track or "cue_points" not in track:
            return 0.0
        return track["cue_points"].get(cue_name, 0.0)

    def build_scene_mix_set(self, vibe="cozy", length=3):
        """Creates a continuous mix playlist that fits a specific mood/vibe."""
        candidates = [t for t in self.catalog.tracks if any(vibe.lower() in tag for tag in t.get("tags", []))]
        if not candidates:
            candidates = self.catalog.tracks
        candidates.sort(key=lambda x: x["bpm"])
        return candidates[:length]
