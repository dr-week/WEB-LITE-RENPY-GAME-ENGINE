# Dynamic Story & Music Director System
# Bridges story mood, locations, and narrative tension to musical cues
# Ren'Py 8.6.0

init -4 python:
    class StoryMusicDirector:
        """Dynamically selects, mixes, and crossfades music based on story conditions."""
        
        SITUATION_MAP = {
            "morning_wake": ("audio/music/lofi/morning_routine.mp3", 75, "audio/sfx/transitions/dragon-studio-whoosh-motion-405445.mp3"),
            "daily_commute": ("audio/music/lofi/morning_station.mp3", 78, "audio/sfx/transitions/dragon-studio-swoosh-1-376872.mp3"),
            "college_social": ("audio/music/lofi/little_wishes.mp3", 76, None),
            "study_focus": ("audio/music/lofi/midnight_stroll.mp3", 76, None),
            "cafe_chill": ("audio/music/lofi/vibin.mp3", 75, None),
            "spring_walk": ("audio/music/lofi/memories_of_spring.mp3", 78, "audio/sfx/transitions/universfield-swoosh-010-352856.mp3"),
            "evening_walk": ("audio/music/lofi/way_home.mp3", 80, None),
            "night_streets": ("audio/music/lofi/downtown_glow.mp3", 85, "audio/sfx/transitions/emircanalp-zoom-sound-effect-125029.mp3"),
            "con_tension": ("audio/music/lofi/sunset_drive.mp3", 82, "audio/sfx/transitions/creatorshome-sharp-riser-327342.mp3"),
            "crisis_debt": ("audio/music/lofi/and_so_it_begins.mp3", 70, "audio/sfx/transitions/dragon-studio-epic-transition-478367.mp3"),
            "bedroom_late": ("audio/music/lofi/bedtime_after_a_coffee.mp3", 72, None),
            "home_chill": ("audio/music/lofi/morning_routine.mp3", 75, None),
            "city_hustle": ("audio/music/lofi/downtown_glow.mp3", 85, "audio/sfx/transitions/dragon-studio-whoosh-motion-405445.mp3"),
            "cafe_work": ("audio/music/lofi/vibin.mp3", 75, None),
            "park_breeze": ("audio/music/lofi/memories_of_spring.mp3", 78, "audio/sfx/transitions/universfield-swoosh-010-352856.mp3"),
            "harbor_twilight": ("audio/music/lofi/way_home.mp3", 80, None),
            "library_mystery": ("audio/music/lofi/midnight_stroll.mp3", 76, None),
        }

        @classmethod
        def set_situation(cls, situation, fadein=2.0, beat_drop=False):
            if situation not in cls.SITUATION_MAP:
                return
            track, bpm, sfx = cls.SITUATION_MAP[situation]
            if sfx:
                renpy.sound.play(sfx, relative_volume=0.35)
            if beat_drop:
                # Jump straight into the 16th beat drop (where drums kick in)
                start_sec = round((16 * 60.0) / bpm, 2)
                renpy.music.play(f"<from {start_sec}>{track}", channel="music", fadeout=fadein, fadein=fadein, loop=True)
            else:
                renpy.music.play(track, channel="music", fadeout=fadein, fadein=fadein, loop=True)

    def set_story_music(situation, fadein=2.0, beat_drop=False):
        StoryMusicDirector.set_situation(situation, fadein=fadein, beat_drop=beat_drop)
