# Notification and skip overlays.

screen notify(message):
    zorder 100
    style_prefix "notify"
    frame at notify_appear:
        text "[message!tq]"
    timer 3.25 action Hide("notify")


transform notify_appear:
    on show:
        alpha 0
        linear 0.25 alpha 1.0
    on hide:
        linear 0.5 alpha 0.0


style notify_frame:
    ypos gui.notify_ypos
    xalign 0.5
    background gui.glass_pill
    padding (22, 12)


style notify_text:
    properties gui.text_properties("notify")
    color gui.text_color


screen skip_indicator():
    zorder 100
    style_prefix "skip"
    frame:
        hbox:
            spacing 8
            text _("Skipping")
            text ">" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text ">" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text ">" at delayed_blink(0.4, 1.0) style "skip_triangle"


transform delayed_blink(delay, cycle):
    alpha 0.5
    pause delay
    block:
        linear 0.2 alpha 1.0
        pause 0.2
        linear 0.2 alpha 0.5
        pause (cycle - 0.4)
        repeat


style skip_frame:
    ypos gui.skip_ypos
    background gui.glass_pill
    padding (16, 10)


style skip_text:
    size gui.notify_text_size
    color gui.text_secondary


style skip_triangle:
    color gui.accent_color
