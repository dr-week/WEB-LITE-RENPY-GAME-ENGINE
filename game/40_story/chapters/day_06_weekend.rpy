# LOLA - Chapter 5, Day 6: Saturday Balance.

label day_06_home:
    $ travel_to("home")
    $ go_to_time_slot("morning")
    scene bg_home at bg_slow_zoom_in
    with dissolve

    "Day 6 - Saturday. No alarm, no lecture bell—just sunlight and two texts buzzing on the nightstand."

    menu:
        "Meet Elena at City Park (unpack the week & unwind)":
            $ unlock_location("park")
            $ travel_to("park")
            scene bg_park at bg_slow_zoom_in
            with dissolve
            $ introduce_character("elena")
            $ update_relationship("elena", "friendship", 12)
            $ change_stat("appeal", 4)
            $ change_stat("stress", -12)
            $ change_stat("confidence", 5)
            elena "Honestly? On Day 1 I thought this city was gonna eat me alive. Look at us now."
        "Pick up a Saturday rush shift with Marcus at Daily Grind":
            $ travel_to("cafe")
            scene bg_cafe at bg_slow_zoom_in
            with dissolve
            $ introduce_character("marcus")
            if not is_employed():
                $ start_job(starter_job)
            $ work_shift()
            $ change_stat("work_skill", 2)
            $ update_relationship("marcus", "friendship", 10)
            marcus "Hah, you move fast when tips are on the line. Respect, Maya."

    $ go_to_time_slot("afternoon")
    jump day_hub
