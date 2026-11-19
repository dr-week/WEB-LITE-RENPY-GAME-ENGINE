# Shared frame and navigation for game-menu screens.

screen game_menu(title=_("Menu"), scroll=None, yinitial=0.0, spacing=0):
    tag menu
    modal True
    style_prefix "game_menu"
    add Solid("#0b1020f2")

    frame:
        style "game_menu_outer_frame"
        hbox:
            spacing 32
            frame:
                style "game_menu_navigation_frame"
                vbox:
                    yfill True
                    vbox:
                        style_prefix "game_menu_navigation"
                        spacing 8
                        textbutton _("Status") action ShowMenu("status")
                        textbutton _("People") action ShowMenu("character_info")
                        if not main_menu:
                            textbutton _("Map") action ShowMenu("world_map")
                        textbutton _("Music & DJ") action ShowMenu("music_jukebox")
                        textbutton _("Save") action ShowMenu("save")
                        textbutton _("Load") action ShowMenu("load")
                        textbutton _("History") action ShowMenu("history")
                        textbutton _("Settings") action ShowMenu("preferences")
                        textbutton _("About") action ShowMenu("about")
                        if not main_menu:
                            textbutton _("Main Menu") action MainMenu()
                        textbutton _("Quit") action Quit(confirm=not main_menu)
                    textbutton _("Return") action Return() style "game_menu_return_button" yalign 1.0
            frame:
                style "game_menu_content_frame"
                if scroll == "viewport":
                    viewport:
                        style "game_menu_viewport"
                        xsize 1272
                        ysize 710
                        viewport_xsize 1244
                        viewport_ysize 710
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        vbox:
                            style_prefix None
                            xsize 1244
                            spacing spacing
                            transclude
                elif scroll == "vpgrid":
                    vpgrid:
                        cols 1
                        style_prefix None
                        xsize 1272
                        ysize 710
                        viewport_xsize 1244
                        viewport_ysize 710
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        spacing spacing
                        transclude
                else:
                    fixed:
                        style_prefix None
                        xsize 1272
                        ysize 710
                        transclude

    label title style "game_menu_label"
    add Solid("#5b3d73", xysize=(1272, 2)) xpos 490 ypos 196
    key "game_menu" action Return()
