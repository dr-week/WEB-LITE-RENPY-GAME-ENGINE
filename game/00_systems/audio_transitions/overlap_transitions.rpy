# Smooth dual-deck DJ crossfade & subtle short-duration transition SFX engine.

init -4 python:
    import json
    import random

    renpy.music.register_channel("sfx_transition_a", "sfx", loop=False)

    def _load_short_sfx():
        try:
            with renpy.open_file("audio/sfx_transitions.json", encoding="utf-8") as handle:
                return [item["file"] for item in json.load(handle).get("sfx", [])]
        except Exception:
            return []

    CURATED_TRANSITION_SFX = _load_short_sfx()

    def play_random_overlap_transition(next_music_track=None, start_sec=0.0, fade_sec=1.6):
        """Play one subtle short-duration swoosh/riser, duck music briefly, and crossfade across dual decks."""
        if CURATED_TRANSITION_SFX:
            duck_music(0.72, 0.2)
            sfx_path = random.choice(CURATED_TRANSITION_SFX)
            renpy.sound.play(sfx_path, channel="sfx_transition_a", relative_volume=0.35)
        if next_music_track:
            crossfade_decks(next_music_track, start_sec=start_sec, fade_sec=fade_sec)
            renpy.restart_interaction()
        elif CURATED_TRANSITION_SFX:
            restore_music(1.1)
