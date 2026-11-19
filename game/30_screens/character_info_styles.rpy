# Character information panel styles.

style char_info_empty:
    font gui.interface_text_font
    size 20
    color gui.text_muted
    xalign 0.0

style char_info_name:
    font gui.interface_text_font
    size 24
    color "#ffffff"
    bold True
    xalign 0.0
    yalign 0.5

style char_info_role:
    font gui.interface_text_font
    size 18
    color "#d8b4f8"
    xalign 0.0
    yalign 0.5

style char_info_stat:
    font gui.interface_text_font
    size 18
    color "#c9cfe3"
    xalign 0.0
    yalign 0.5

style char_rel_bar:
    xsize 260
    ysize 12
    yalign 0.5
    left_bar Solid("#9b59b6")
    right_bar Solid("#2b3048")
    thumb None

style char_info_recurring:
    font gui.interface_text_font
    size 16
    bold True
    color "#ffe8a3"
    xalign 0.5
