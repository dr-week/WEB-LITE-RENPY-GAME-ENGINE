# Audio channels and tracks registry with full sub-folder separation
init -5 python:
    renpy.music.register_channel("sfx_ambient", "sfx", loop=True)
    renpy.music.register_channel("sfx_cinematic", "sfx", loop=False)

    # Music Lo-Fi Tracks
    MUSIC_TRANQUIL_TRANSIT = "audio/music/lofi/tranquil_transit.mp3"
    MUSIC_MORNING_ROUTINE  = "audio/music/lofi/morning_routine.mp3"
    MUSIC_LITTLE_WISHES    = "audio/music/lofi/little_wishes.mp3"
    MUSIC_COLORFUL_FLOWERS = "audio/music/lofi/colorful_flowers.mp3"
    MUSIC_BEDTIME_COFFEE   = "audio/music/lofi/bedtime_after_a_coffee.mp3"
    MUSIC_SUNSET_DRIVE     = "audio/music/lofi/sunset_drive.mp3"
    MUSIC_WHEN_I_WAS_A_BOY = "audio/music/lofi/when_i_was_a_boy.mp3"

    # Curated Aesthetic Transition & Atmosphere Sound Effects
    SFX_SWOOSH_CINEMATIC = "audio/sfx/transitions/dragon-studio-whoosh-cinematic-sound-effect-376889.mp3"
    SFX_WHOOSH_MOTION    = "audio/sfx/transitions/dragon-studio-whoosh-motion-405445.mp3"
    SFX_SWOOSH_SOFT      = "audio/sfx/transitions/universfield-swoosh-010-352856.mp3"
    SFX_EPIC_TRANSITION  = "audio/sfx/transitions/dragon-studio-epic-transition-478367.mp3"
    SFX_SHARP_RISER      = "audio/sfx/transitions/creatorshome-sharp-riser-327342.mp3"
    SFX_SWOOSH           = SFX_SWOOSH_SOFT
    SFX_WOOSH            = SFX_WHOOSH_MOTION

    # UI Interaction Sound Effects
    SFX_UI_CLICK         = "audio/sfx/ui/click_001.wav"
    SFX_UI_SELECT        = "audio/sfx/ui/select_001.wav"
    SFX_UI_SWITCH        = "audio/sfx/ui/switch_001.wav"
    SFX_UI_CONFIRM       = "audio/sfx/ui/confirmation_001.wav"
    SFX_UI_BACK          = "audio/sfx/ui/back_001.wav"
