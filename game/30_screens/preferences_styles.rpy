# Shared styles for the preferences screen.

style pref_label:
    top_margin 12
    bottom_margin 4


style pref_label_text:
    size 24
    color gui.accent_color


style radio_vbox:
    spacing 8


style check_vbox:
    spacing 8


style radio_button:
    properties gui.button_properties("radio_button")
    background gui.glass_btn_idle
    hover_background gui.glass_btn_hover
    padding (14, 10)


style radio_button_text:
    properties gui.text_properties("radio_button")
    size 21


style check_button:
    properties gui.button_properties("check_button")
    background gui.glass_btn_idle
    hover_background gui.glass_btn_hover
    padding (14, 10)


style check_button_text:
    properties gui.text_properties("check_button")
    size 21


style slider_slider:
    xsize 500


style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 12


style slider_button_text:
    properties gui.text_properties("slider_button")


style slider_vbox:
    xsize 560
