# Top gameplay HUD and bottom quick-action strip.

screen hud_bar():
    zorder 90
    if not main_menu and not renpy.context()._menu:
        frame:
            xfill True
            ypos 0
            ysize 58
            background Solid("#0d1224f0")
            padding (24, 8)
            hbox:
                xfill True
                yalign 0.5
                frame:
                    background Solid("#2b1e3d")
                    padding (12, 5)
                    yalign 0.5
                    hbox:
                        spacing 8
                        yalign 0.5
                        add Transform("images/ui/icons/calendar.png", xysize=(20, 20)) yalign 0.5
                        text "DAY [current_day] • [time_slot.upper()]  |  [get_location_name(current_location)]" style "hud_badge_text"
                hbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 14
                    for ic, val in [("cash", "$[money]"), ("energy", "[energy]"), ("education", "[education_progress]%"), ("intelligence", "[intelligence]"), ("appeal", "[appeal]"), ("stress", "[stress]")]:
                        hbox:
                            spacing 5
                            yalign 0.5
                            add Transform("images/ui/icons/%s.png" % ic, xysize=(20, 20)) yalign 0.5
                            text val style "hud_stats_text"
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 8
                    textbutton _("Status") action ShowMenu("status") style "hud_nav_button"
                    textbutton _("People") action ShowMenu("character_info") style "hud_nav_button"
                    textbutton _("Map") action ShowMenu("world_map") style "hud_nav_button"
                    textbutton _("Save") action ShowMenu("save") style "hud_nav_button"
                    textbutton _("Settings") action ShowMenu("preferences") style "hud_nav_button"

screen quick_menu():
    zorder 100
    if quick_menu and not main_menu and not renpy.context()._menu:
        hbox:
            style_prefix "quick"
            style "quick_menu"
            textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu("history")
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Save") action ShowMenu("save")
            textbutton _("Load") action ShowMenu("load")
            textbutton _("Status") action ShowMenu("status")
            textbutton _("People") action ShowMenu("character_info")
            textbutton _("Prefs") action ShowMenu("preferences")

style hud_badge_text:
    font gui.interface_text_font
    size 17
    bold True
    color "#f2d8ff"
    yalign 0.5

style hud_stats_text:
    font gui.interface_text_font
    size 18
    color "#eee7f5"
    yalign 0.5

style hud_nav_button:
    background Solid("#322444")
    hover_background Solid("#65457f")
    padding (13, 5)
    yalign 0.5

style hud_nav_button_text:
    font gui.interface_text_font
    size 17
    color "#ffffff"
    hover_color "#ffe8a3"

style quick_menu:
    xalign 0.5
    yalign 0.995
    spacing 6

style quick_button:
    properties gui.button_properties("quick_button")
    background Solid("#101522e8")
    hover_background Solid("#4b3561")
    padding (12, 6)

style quick_button_text:
    properties gui.text_properties("quick_button")
    color gui.quick_button_text_idle_color
    hover_color "#ffffff"
    size 17
