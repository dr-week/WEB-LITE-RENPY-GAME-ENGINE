# Styling for the music jukebox and track explorer screen.
# Ren'Py 8.6.0

style music_section_label:
    font gui.interface_text_font
    size 18
    color "#e8d5f5"
    bold True

style music_deck_button:
    background Solid("#633e82")
    hover_background Solid("#8554af")
    padding (16, 10)

style music_deck_button_text:
    font gui.interface_text_font
    size 16
    bold True
    color "#ffffff"
    hover_color "#ffe8a3"

style music_deck_button_secondary:
    background Solid("#222842")
    hover_background Solid("#38426c")
    padding (14, 10)

style music_deck_button_secondary_text:
    font gui.interface_text_font
    size 15
    color "#d8d3e8"

style music_track_btn:
    background Solid("#2b223c")
    hover_background Solid("#5a3c7c")
    padding (12, 6)

style music_track_btn_text:
    font gui.interface_text_font
    size 13
    bold True
    color "#ffffff"
    hover_color "#ffe8a3"

style music_track_btn_active:
    background Solid("#ffe8a3")
    padding (12, 6)

style music_track_btn_active_text:
    font gui.interface_text_font
    size 13
    bold True
    color "#191128"
