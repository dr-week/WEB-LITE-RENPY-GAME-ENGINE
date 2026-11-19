# Status dashboard styles.

style status_summary_card:
    xsize 396
    background gui.glass_card
    padding (22, 16)

style status_column_card:
    xsize 600
    background gui.glass_card
    padding (24, 20)

style status_card_title:
    font gui.interface_text_font
    size 18
    bold True
    color "#d8b4f8"
    xalign 0.0

style status_label:
    font gui.interface_text_font
    size 19
    color "#e8eaf6"
    xalign 0.0

style status_stat_num:
    font gui.interface_text_font
    size 18
    color "#b8bed9"
    xalign 1.0

style status_value:
    font gui.interface_text_font
    size 24
    bold True
    color "#ffffff"
    xalign 0.0

style status_value_small:
    font gui.interface_text_font
    size 18
    color "#c9cfe3"
    xalign 0.0

style status_bar:
    xsize 550
    ysize 12
    left_bar Solid("#9b59b6")
    right_bar Solid("#2b3048")
    thumb None
