# LOLA - Options Configuration
# Ren'Py 8.6.0

define config.developer = True
define config.default_fullscreen = False
define config.main_menu_music = "audio/music/lofi/downtown_glow.mp3"

default quick_menu = True
default _game_menu_screen = "save"
default _history_screen = "history"
default _preferences_screen = "preferences"

init python:
    if "situational_fx_overlay" not in config.overlay_screens:
        config.overlay_screens.append("situational_fx_overlay")
    if "hud_bar" not in config.overlay_screens:
        config.overlay_screens.append("hud_bar")
    if "cd_music_widget" not in config.overlay_screens:
        config.overlay_screens.append("cd_music_widget")
    if "quick_menu" not in config.overlay_screens:
        config.overlay_screens.append("quick_menu")
    if "image_feedback_overlay" not in config.overlay_screens:
        config.overlay_screens.append("image_feedback_overlay")
