# LOLA - Dialogue and Choice UI
# Ren'Py 8.6.0

screen say(who, what):
    style_prefix "say"
    window:
        id "window"
        vbox:
            spacing 8
            if who is not None:
                window:
                    id "namebox"
                    style "namebox"
                    text who id "who"
            text what id "what"
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0
