# Ren'Py settings, graphics card renderer, and online community links.
screen preferences():
    tag menu
    use game_menu(_("Settings & Links"), scroll="viewport"):
        vbox:
            spacing 28
            # External Links Section
            frame:
                background Solid("#151d3bee")
                padding (24, 18)
                xfill True
                vbox:
                    spacing 10
                    label _("Official Links & Audio Credits") style "pref_label"
                    hbox:
                        spacing 20
                        textbutton _("Music Artist Credits") action OpenURL("https://freemusicarchive.org/music/pumpupthemind/single/tranquil-transit/") style "main_menu_button"
                        textbutton _("Chosic Free Lofi Library") action OpenURL("https://www.chosic.com/free-music/lofi/") style "main_menu_button"
            hbox:
                spacing 50
                vbox:
                    style_prefix "radio"
                    label _("Display & Graphics")
                    textbutton _("Windowed") action Preference("display", "window")
                    textbutton _("Fullscreen") action Preference("display", "fullscreen")
                    textbutton _("Hardware Acceleration (GL2)") action Preference("gl powersave", "disable")
                vbox:
                    style_prefix "check"
                    label _("Skip & Transitions")
                    textbutton _("Unseen text") action Preference("skip", "toggle")
                    textbutton _("After choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))
            hbox:
                spacing 50
                style_prefix "slider"
                vbox:
                    label _("Text speed")
                    bar value Preference("text speed")
                    label _("Auto-forward time")
                    bar value Preference("auto-forward time")
                vbox:
                    if config.has_music:
                        label _("Music volume")
                        bar value Preference("music volume")
                    if config.has_sound:
                        label _("Sound volume")
                        bar value Preference("sound volume")
                    textbutton _("Mute all") action Preference("all mute", "toggle")
