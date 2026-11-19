# Dual-deck Ren'Py music crossfader, smooth ducking, and 4-stem vertical layering.

init -5 python:
    renpy.music.register_channel("music_deck_b", "music", loop=True)
    STEM_CHANNELS = ("layer_base", "layer_beat", "layer_melody", "layer_ambient")
    for _ch in STEM_CHANNELS:
        renpy.music.register_channel(_ch, "music", loop=True)
    _active_music_deck = "music"

    def crossfade_decks(next_track, start_sec=0.0, fade_sec=1.6):
        """Simultaneously fade out the active deck and fade in the alternate deck."""
        global _active_music_deck
        if not next_track:
            return
        outgoing = _active_music_deck
        incoming = "music_deck_b" if outgoing == "music" else "music"
        target = f"<from {start_sec}>{next_track}" if start_sec > 0 else next_track
        stop_stem_layers(fade_sec=fade_sec)
        renpy.music.stop(channel=outgoing, fadeout=fade_sec)
        renpy.music.play(target, channel=incoming, fadein=fade_sec, loop=True)
        renpy.music.set_volume(1.0, delay=fade_sec, channel=incoming)
        _active_music_deck = incoming

    def duck_music(duck_vol=0.72, fade_sec=0.25):
        """Smoothly lower active deck volume during transition SFX or alerts."""
        renpy.music.set_volume(duck_vol, delay=fade_sec, channel=_active_music_deck)

    def restore_music(fade_sec=0.45):
        """Restore active deck volume back to 1.0 after ducking."""
        renpy.music.set_volume(1.0, delay=fade_sec, channel=_active_music_deck)

    def play_stem_layers(stems, volumes=None, fade_sec=1.0):
        """Start equal-length 44.1 kHz .ogg stems in sample-locked sync via synchro_start."""
        volumes = volumes or {}
        for ch in STEM_CHANNELS:
            path = stems.get(ch)
            if path:
                renpy.music.play(path, channel=ch, synchro_start=True, loop=True)
                renpy.music.set_volume(volumes.get(ch, 1.0), delay=fade_sec, channel=ch)

    def set_stem_layer_volumes(volumes, fade_sec=1.2):
        """Crossfade vertical stem layers dynamically without breaking sync."""
        for ch, vol in volumes.items():
            if ch in STEM_CHANNELS:
                renpy.music.set_volume(vol, delay=fade_sec, channel=ch)

    def stop_stem_layers(fade_sec=1.0):
        """Fade out all 4 vertical stem channels together."""
        for ch in STEM_CHANNELS:
            renpy.music.stop(channel=ch, fadeout=fade_sec)
