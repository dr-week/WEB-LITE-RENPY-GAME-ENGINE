# LOLA - Main Entry Point
# Minimal script that routes to story and systems
# Ren'Py 8.6.0

define config.name = "LOLA"
define config.version = "0.1.0 vertical slice"

define config.rollback_enabled = True
define config.skip_sounds = False

define config.has_music = True
define config.has_sound = True
define config.has_voice = True

label start:
    jump game_start


label game_start:
    $ init_new_game_state()
    jump prologue_random_start


label game_continue:
    jump day_router


label start_game:
    jump game_start
