# LOLA - City Map Navigation Screen

init python:
    MAP_LOCATION_LABELS = {
        "home": "location_home",
        "bus_stop": "location_bus_stop",
        "college": "location_college",
        "cafe": "location_work",
        "street": "location_street",
        "library": "location_library",
        "park": "location_park",
    }
    MAP_LOCATION_ICONS = {
        "home": "home",
        "bus_stop": "time",
        "college": "education",
        "cafe": "shop",
        "street": "map",
        "library": "bag",
        "park": "appeal",
    }

    def travel_from_map(loc_id):
        target = MAP_LOCATION_LABELS.get(loc_id)
        if not target:
            return
        if renpy.context()._menu:
            renpy.jump_out_of_context(target)
        else:
            renpy.hide_screen("world_map")
            renpy.jump(target)

screen world_map():
    tag menu
    use game_menu(_("City Map"), scroll="viewport", spacing=20):
        vbox:
            xfill True
            spacing 20
            hbox:
                spacing 20
                text "Current Location: [get_location_name(current_location)] — [get_location_description(current_location)]" style "map_description" yalign 0.5
                textbutton "Explore Solis Bay Map" style "say_continue_button" action Show("world_map_screen") yalign 0.5

            vpgrid:
                cols 3
                allow_underfull True
                xfill True
                spacing 22

                for loc_id in get_available_locations():
                    $ loc_name = get_location_name(loc_id)
                    $ loc_icon = MAP_LOCATION_ICONS.get(loc_id, "map")
                    if loc_id == current_location:
                        frame:
                            style "map_card_current"
                            hbox:
                                spacing 14
                                add Transform("images/ui/icons/%s.png" % loc_icon, xysize=(42, 42)) yalign 0.5
                                vbox:
                                    spacing 6
                                    text loc_name style "map_button_text"
                                    text "Here Now" style "map_subtext_current"
                    else:
                        button:
                            style "map_card_button"
                            action Function(travel_from_map, loc_id)
                            hbox:
                                spacing 14
                                add Transform("images/ui/icons/%s.png" % loc_icon, xysize=(42, 42)) yalign 0.5
                                vbox:
                                    spacing 6
                                    text loc_name style "map_button_text"
                                    text "Travel Here →" style "map_subtext"
