# Shared frame and navigation styles for game-menu screens.

style game_menu_outer_frame:
    xalign 0.5
    yalign 0.5
    xsize 1740
    ysize 910
    background gui.glass_elevated
    padding (40, 40)

style game_menu_navigation_frame:
    xsize 300
    yfill True
    background gui.glass_panel
    padding (22, 24)

style game_menu_navigation_button:
    xfill True
    background gui.glass_btn_idle
    hover_background gui.glass_btn_hover
    padding (18, 12)

style game_menu_navigation_button_text:
    size 22
    color "#f4eff8"
    hover_color "#ffe8a3"

style game_menu_return_button:
    xfill True
    background gui.glass_pill
    hover_background gui.glass_btn_hover
    padding (18, 12)

style game_menu_return_button_text:
    size 22
    bold True
    color "#ffffff"
    xalign 0.5

style game_menu_content_frame:
    xsize 1336
    yfill True
    background gui.glass_card
    padding (34, 92, 34, 28)

style game_menu_viewport:
    xsize 1244

style game_menu_label:
    xpos 490
    ypos 142
    ysize 44
    xalign 0.0

style game_menu_label_text:
    size 38
    bold True
    color "#e8d5f5"
