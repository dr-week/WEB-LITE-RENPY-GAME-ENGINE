# LOLA - Character Info Screen

screen character_info():
    tag menu
    $ met_chars = [c for c in get_all_characters().values() if c.get("introduced", False)]

    use game_menu(_("People & Relationships"), scroll="viewport", spacing=16):
        if not met_chars:
            text "Maya hasn't met anyone in the city yet." style "char_info_empty"
        else:
            vbox:
                xfill True
                spacing 16
                for char in met_chars:
                    $ role_label = char["role"].replace("_", " ").title()
                    $ fl_val = char.get("friendship", 0)
                    $ fl = get_relationship_level(fl_val)
                    frame:
                        xfill True
                        background Solid("#202436")
                        padding (24, 18)
                        hbox:
                            xfill True
                            spacing 18
                            vbox:
                                xsize 920
                                spacing 8
                                hbox:
                                    spacing 14
                                    text char["display_name"] style "char_info_name"
                                    text role_label style "char_info_role"
                                hbox:
                                    spacing 16
                                    bar value StaticValue(fl_val, 100) style "char_rel_bar"
                                    text "Friendship: [fl_val]/100 ([fl])" style "char_info_stat"
                                if char.get("romance", 0) > 0:
                                    $ rl_val = char["romance"]
                                    $ rl = get_relationship_level(rl_val)
                                    text "Romance: [rl_val]/100 ([rl])" style "char_info_stat"
                                if char.get("hostility", 0) > 0:
                                    $ hl = get_relationship_level(char["hostility"])
                                    text "Tension: [char['hostility']]/100 ([hl])" style "char_info_stat"
                            if char.get("recurring"):
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background Solid("#3b2852")
                                    padding (14, 6)
                                    text "Recurring" style "char_info_recurring"
