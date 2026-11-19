# LOLA - Prologue: Day 1 - Transit and campus arrival
# Ren'Py 8.6.0
label travel_bus_stop:
    $ travel_to("bus_stop")
    $ set_story_music("daily_commute", fadein=2.0)
    scene scene_day1_bus_stop at bg_slow_zoom_in with dissolve
    "Maya slipped into the front with an angelic smile."
    menu:
        "Blend in socially":
            play sound SFX_SWOOSH
            $ change_stat("appeal", 2)
            menu:
                "Make warm small talk in line":
                    $ change_stat("communication", 2)
                "Compliment a commuter's coat":
                    $ change_stat("appeal", 3)
        "Focus on strategy":
            play sound SFX_WOOSH
            $ change_stat("intelligence", 2)
            menu:
                "Review class notes on her phone":
                    $ change_stat("intelligence", 2)
                "Compare transit fares to save cash":
                    $ change_stat("financial_literacy", 3)
    $ spend_money(2, "Bus fare") if can_afford(2) else None
    jump arrive_college

label arrive_college:
    $ travel_to("college")
    $ set_story_music("college_social", fadein=2.0)
    scene bg_college_entrance with dissolve
    $ set_flag("has_reached_college", True)
    $ record_event("reached_college")
    "She stepped onto campus with minutes to spare, chin high."
    scene scene_day1_campus_gate at bg_pan_right with dissolve
    menu:
        "Take a social route":
            play sound SFX_SWOOSH
            $ change_stat("communication", 2)
            menu:
                "Ask a friendly student for directions":
                    $ change_stat("confidence", 5)
                    jump find_classroom
                "Check in at the information desk":
                    $ change_stat("appeal", 2)
                    $ reputation += 5
                    jump find_classroom
        "Navigate independently":
            play sound SFX_WOOSH
            $ change_stat("intelligence", 2)
            menu:
                "Study the campus directory carefully":
                    $ change_stat("intelligence", 2)
                    jump find_classroom
                "Follow the flow of business students":
                    $ change_stat("confidence", 3)
                    jump find_classroom

label find_classroom:
    scene scene_day1_classroom_entry at bg_slow_zoom_in with dissolve
    "Maya spotted her room: late enough to turn heads, early enough to charm."
    if not get_flag("has_met_first_classmate"):
        $ active_classmate_id = "elena"
        $ introduce_character("elena")
        $ classmate = get_character_by_id("elena")
        $ record_event("first_classmate_meeting", "elena")
        $ set_flag("has_met_first_classmate", True)
        scene scene_day1_elena_wave at cg_breathe with dissolve
        "A girl in the middle row caught her eye and waved."
        menu:
            "Sit with Elena":
                play sound SFX_SWOOSH
                $ update_relationship("elena", "friendship", 10)
                menu:
                    "Smile and introduce herself warmly":
                        $ update_relationship("elena", "friendship", 5)
                        scene cg_class_notes with dissolve
                        "[classmate['display_name']] slides a note across the desk."
                        jump class_session
                    "Offer to share syllabus details":
                        $ change_stat("intelligence", 2)
                        jump class_session
            "Take an independent desk":
                play sound SFX_WOOSH
                $ change_stat("intelligence", 2)
                menu:
                    "Take a seat near the window":
                        $ change_stat("confidence", 3)
                        jump class_session
                    "Position near the professor's podium":
                        $ change_stat("learning", 3)
                        jump class_session
    else:
        jump class_session
