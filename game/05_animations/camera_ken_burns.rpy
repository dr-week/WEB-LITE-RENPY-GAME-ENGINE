# Reusable subpixel Ken Burns, slideshow crossfade, and camera-shake transforms.

transform slide_fade_in:
    subpixel True
    alpha 0.0
    ease 1.4 alpha 1.0

transform menu_kb_zoom_in:
    subpixel True
    xalign 0.5 yalign 0.5 zoom 1.0
    ease 6.2 zoom 1.07

transform menu_kb_zoom_out:
    subpixel True
    xalign 0.5 yalign 0.5 zoom 1.07
    ease 6.2 zoom 1.0

transform menu_kb_zoom_in_left:
    subpixel True
    xalign 0.55 yalign 0.5 zoom 1.02
    ease 6.2 zoom 1.08 xalign 0.42

transform menu_kb_zoom_out_right:
    subpixel True
    xalign 0.42 yalign 0.5 zoom 1.08
    ease 6.2 zoom 1.02 xalign 0.55

transform menu_kb_pan_up_zoom:
    subpixel True
    xalign 0.5 yalign 0.58 zoom 1.02
    ease 6.2 zoom 1.07 yalign 0.42

transform menu_kb_pan_down_zoom:
    subpixel True
    xalign 0.5 yalign 0.42 zoom 1.07
    ease 6.2 zoom 1.02 yalign 0.58

transform bg_slow_zoom_in(duration=14.0):
    subpixel True
    xalign 0.5 yalign 0.5 zoom 1.0
    ease duration zoom 1.08

transform bg_slow_zoom_out(duration=14.0):
    subpixel True
    xalign 0.5 yalign 0.5 zoom 1.08
    ease duration zoom 1.0

transform bg_pan_left(duration=12.0):
    subpixel True
    xalign 0.60 yalign 0.5 zoom 1.06
    ease duration xalign 0.40

transform bg_pan_right(duration=12.0):
    subpixel True
    xalign 0.40 yalign 0.5 zoom 1.06
    ease duration xalign 0.60

transform cg_breathe:
    subpixel True
    xalign 0.5 yalign 0.5 zoom 1.0
    ease 3.2 zoom 1.02
    ease 3.2 zoom 1.0
    repeat

transform camera_shake:
    subpixel True
    ease 0.05 xoffset -10 yoffset 6
    ease 0.05 xoffset 10 yoffset -6
    ease 0.05 xoffset -6 yoffset -4
    ease 0.05 xoffset 6 yoffset 4
    ease 0.08 xoffset 0 yoffset 0
