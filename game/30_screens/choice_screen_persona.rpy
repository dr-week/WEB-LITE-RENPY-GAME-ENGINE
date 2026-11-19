# Aesthetic Persona / Danganronpa-style Iconic Choice Screen
screen choice(items):
    style_prefix "choice"
    frame:
        at ui_modal_pop
        xalign 0.5
        yalign 0.42
        xsize 960
        ymaximum 560
        background Solid("#0a0e1fee")
        padding (32, 24)
        vbox:
            xfill True
            spacing 14
            text _("TACTICAL DECISION // MAYA'S MOVE") style "choice_hint_text"
            vbox:
                xfill True
                spacing 16
                for item in items:
                    if item.action is None:
                        text item.caption style "choice_hint_text"
                    else:
                        $ icon_info = parse_choice_icon(item.caption)
                        button:
                            at persona_choice_pop
                            action item.action
                            xfill True
                            ysize 62
                            background Solid("#141b38")
                            hover_background Solid("#222d5a")
                            padding (16, 8)
                            hbox:
                                align (0.0, 0.5)
                                spacing 16
                                # Left visual icon badge
                                frame:
                                    xysize (42, 42)
                                    background Solid(icon_info[2])
                                    padding (4, 4)
                                    align (0.5, 0.5)
                                    add icon_info[0] size (34, 34) align (0.5, 0.5)
                                # Primary choice text
                                text icon_info[1]:
                                    substitute False
                                    style "choice_button_text"
                                    yalign 0.5
