# Dialogue history screen.

screen history():
    tag menu
    predict False

    use game_menu(_("History"), scroll="vpgrid", yinitial=1.0, spacing=14):
        style_prefix "history"

        for h in _history_list:
            window:
                has fixed:
                    yfit True

                if h.who:
                    label h.who:
                        style "history_name"
                        substitute False
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")


style history_window:
    xfill True
    ysize gui.history_height
    background Solid("#222638")
    padding (20, 14)


style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width


style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign
    color gui.accent_color


style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")
    color gui.text_color
