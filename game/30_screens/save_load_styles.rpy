# Styling for save/load pages and slots.

style page_label:
    xpadding 35
    ypadding 4
    xalign 0.5


style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color


style page_button:
    properties gui.button_properties("page_button")
    background gui.glass_btn_idle
    hover_background gui.glass_btn_hover
    padding (14, 10)


style page_button_text:
    properties gui.text_properties("page_button")
    size 20


style slot_button:
    properties gui.button_properties("slot_button")
    background gui.glass_card
    hover_background gui.glass_btn_hover
    padding (16, 14)


style slot_button_text:
    properties gui.text_properties("slot_button")
    color gui.text_color


style slot_time_text:
    size 16
    color gui.text_secondary
    xalign 0.5


style slot_name_text:
    size 19
    color gui.text_color
    xalign 0.5
