# Reusable UI/UX hover, entrance, float, and pulse ATL transforms (custom warpers).

transform ui_hover_pop:
    subpixel True
    on hover:
        ease 0.16 zoom 1.04 yoffset -2
    on idle:
        ease 0.18 zoom 1.0 yoffset 0

transform ui_icon_nudge:
    subpixel True
    on hover:
        ease 0.16 zoom 1.12
    on idle:
        ease 0.18 zoom 1.0

transform ui_card_enter:
    subpixel True
    alpha 0.0 yoffset 18
    ease 0.32 alpha 1.0 yoffset 0

transform ui_modal_pop:
    subpixel True
    alpha 0.0 zoom 0.95
    ease 0.24 alpha 1.0 zoom 1.0

transform ui_float_gentle:
    subpixel True
    ease 2.2 yoffset -5
    ease 2.2 yoffset 5
    repeat

transform ui_pulse_soft:
    subpixel True
    ease 1.4 alpha 1.0
    ease 1.4 alpha 0.72
    repeat
