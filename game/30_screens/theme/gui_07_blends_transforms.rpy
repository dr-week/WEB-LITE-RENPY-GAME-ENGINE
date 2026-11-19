# Modular opacity, blur, shadow, blending-mode, and UI motion transforms.

init offset = -2

transform ui_glass_opacity(opacity=0.94):
    alpha opacity

transform ui_glass_blur(blur_px=6.0, opacity=0.88):
    blur blur_px
    alpha opacity

transform ui_blend_add_sheen(opacity=0.22):
    blend "add"
    alpha opacity

transform ui_blend_multiply_shadow(opacity=0.55):
    blend "multiply"
    alpha opacity

transform ui_vignette_overlay(opacity=0.58):
    xysize (1920, 1080)
    blend "multiply"
    alpha opacity

transform ui_panel_entrance(delay_s=0.0):
    alpha 0.0
    yoffset 10
    pause delay_s
    easein 0.22 alpha 1.0 yoffset 0

transform ui_modal_pop:
    alpha 0.0
    zoom 0.96
    easein 0.18 alpha 1.0 zoom 1.0

transform ui_button_hover_pop:
    on idle:
        ease 0.12 zoom 1.0
    on hover:
        ease 0.12 zoom 1.02

transform ui_ambient_pulse(low_a=0.18, high_a=0.34):
    blend "add"
    alpha low_a
    block:
        easein 2.4 alpha high_a
        easeout 2.4 alpha low_a
        repeat
