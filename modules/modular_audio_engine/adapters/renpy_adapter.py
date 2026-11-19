"""
Modular Audio Engine Adapter for Ren'Py games.
Provides standard Ren'Py script statement helpers and transitions.
"""

class RenpyAudioAdapter:
    @staticmethod
    def play_track(track_dict, fadein=2.0, loop=True):
        """Returns renpy python code string or runs renpy.music.play."""
        path = track_dict.get("audio_file", "")
        # Adjust for renpy game/ root
        if path.startswith("game/"):
            path = path[len("game/"):]
        return f'renpy.music.play("{path}", channel="music", fadein={fadein}, loop={loop})'

    @staticmethod
    def dj_transition_cue(sfx_name="sfx_scratch", next_track_path="", fadein=1.5):
        """Generates cue instructions for crossfading with a DJ FX."""
        return [
            f'renpy.sound.play("{sfx_name}", channel="sound")',
            f'renpy.music.play("{next_track_path}", channel="music", fadein={fadein}, loop=True)'
        ]
