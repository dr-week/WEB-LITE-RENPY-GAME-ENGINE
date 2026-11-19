"""
Randomized Audio Transition Engine.
Selects, pairs, and generates dynamic transition recipes.
"""
import random

class TransitionEngine:
    TRANSITION_PRESETS = [
        {"name": "DJ_SCRATCH_DROP", "sfx_lead": "dj_scratch", "sfx_tail": "sub_drop", "fade_time": 1.5, "overlap_delay": 0.4},
        {"name": "SPINBACK_WOOSH", "sfx_lead": "dj_spinback", "sfx_tail": "woosh", "fade_time": 1.2, "overlap_delay": 0.5},
        {"name": "CINEMATIC_IMPACT", "sfx_lead": "noise_riser", "sfx_tail": "boom", "fade_time": 2.2, "overlap_delay": 1.8},
        {"name": "TAPE_STOP_REVERSE", "sfx_lead": "dj_tape_stop", "sfx_tail": "reverse_cymbal", "fade_time": 1.6, "overlap_delay": 0.6},
        {"name": "AIRHORN_DROP", "sfx_lead": "dj_airhorn", "sfx_tail": "cinematic_hit", "fade_time": 1.4, "overlap_delay": 0.8},
        {"name": "SMOOTH_SWEEP", "sfx_lead": "swoosh", "sfx_tail": "woosh", "fade_time": 2.0, "overlap_delay": 0.3},
    ]

    @classmethod
    def get_random_transition(cls):
        return random.choice(cls.TRANSITION_PRESETS)
