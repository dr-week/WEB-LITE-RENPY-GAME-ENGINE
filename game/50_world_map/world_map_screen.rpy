# Interactive pannable Solis Bay world map screen with glassmorphic pins & day/night tinting.

init python:
    def _resolve_map_image():
        path = "images/ui/map/solis_bay_day.png"
        return path if renpy.loadable(path) else Solid("#141c33")

    def _pin_tooltip(loc_id, available):
        loc = get_location(loc_id)
        pin = get_map_pin(loc_id)
        name = loc["name"] if loc else loc_id
        desc = loc["description"] if loc else ""
        terrain = pin["terrain"] if pin else ""
        links = ", ".join(get_location_name(l) for l in get_connected_links(loc_id))
        state_txt = "Click to travel" if available else "Locked (progress story to unlock)"
        return "{} [{}] — {} ({}) | Links: {}".format(name, terrain, desc, state_txt, links or "None")

screen world_map_screen():
    modal True
    zorder 60
    default slot_name = getattr(store, "current_time_slot", "afternoon")
    default map_tint = get_map_lighting_tint(slot_name)

    viewport id "solis_map_vp":
        xysize (1920, 1080)
        draggable True
        mousewheel True
        edgescroll (80, 650)
        fixed:
            xysize MAP_CANVAS_SIZE
            add Transform(_resolve_map_image(), xysize=MAP_CANVAS_SIZE, matrixcolor=TintMatrix(map_tint))
            for loc_id, pin in MAP_PINS.items():
                $ avail = is_location_available(loc_id)
                $ is_here = (getattr(store, "current_location", "") == loc_id)
                $ lbl = get_location_name(loc_id) + (" (Here)" if is_here else ("" if avail else " [Locked]"))
                textbutton lbl:
                    xpos pin["x"]
                    ypos pin["y"]
                    anchor (0.5, 0.5)
                    style ("game_menu_return_button" if is_here else "choice_button")
                    xsize 250
                    sensitive avail
                    tooltip _pin_tooltip(loc_id, avail)
                    action [Hide("world_map_screen"), Function(travel_from_map, loc_id)]

    add "ui_vignette_ambient" at ui_vignette_overlay(0.42)
    frame at ui_panel_entrance(0.02):
        xpos 36 ypos 28 background gui.glass_elevated padding (24, 14)
        hbox:
            spacing 24
            vbox:
                text "[CITY_NAME]" style "status_card_title" size 26
                text "[CITY_TAGLINE] · Drag or scroll to explore" style "status_value_small"
            textbutton "Close Map" style "say_continue_button" action Hide("world_map_screen")

    $ tip = GetTooltip()
    if tip:
        frame:
            xalign 0.5 yalign 0.96 background gui.glass_card padding (24, 14)
            text tip style "status_value_small" color "#ffe8a3"
