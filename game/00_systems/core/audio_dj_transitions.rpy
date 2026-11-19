# Modular Audio Engine - Ren'Py Bindings & Mid-Beat Jump Handlers
init -5 python:
    MUSIC_DOWNTOWN_GLOW    = "audio/music/lofi/downtown_glow.mp3"
    MUSIC_VIBIN            = "audio/music/lofi/vibin.mp3"
    MUSIC_NEW_BEGINNINGS   = "audio/music/lofi/new_beginnings.mp3"
    MUSIC_AND_SO_IT_BEGINS = "audio/music/lofi/and_so_it_begins.mp3"
    MUSIC_ON_MY_WAY        = "audio/music/lofi/on_my_way.mp3"
    MUSIC_MEMORIES_SPRING  = "audio/music/lofi/memories_of_spring.mp3"
    MUSIC_WAY_HOME         = "audio/music/lofi/way_home.mp3"
    MUSIC_MORNING_STATION  = "audio/music/lofi/morning_station.mp3"
    MUSIC_MIDNIGHT_STROLL  = "audio/music/lofi/midnight_stroll.mp3"

    def dj_crossfade_to(next_track, sfx_cue="audio/sfx/transitions/dragon-studio-whoosh-motion-405445.mp3", fadein=2.0):
        """Crossfades into the next track with an optional aesthetic whoosh transition."""
        if sfx_cue:
            renpy.sound.play(sfx_cue, relative_volume=0.4)
        renpy.music.play(next_track, channel="music", fadein=fadein, loop=True)

    def play_music_from(track, start_sec=0.0, fadein=1.0, loop=True):
        """Starts music from any timestamp or middle beat for scene variations."""
        renpy.music.play(f"<from {start_sec}>{track}", channel="music", fadein=fadein, loop=loop)

    def play_music_at_beat(track, bpm=75, beat_num=16, fadein=1.0):
        """Calculates exact beat offset and jumps directly into it."""
        sec = round((beat_num * 60.0) / bpm, 2)
        play_music_from(track, start_sec=sec, fadein=fadein)
