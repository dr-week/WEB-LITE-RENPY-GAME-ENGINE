# LOLA - Day 8 (Harbor Twilight)

# Generated modular 2-option story beat (park / morning / cozy).

label day_08_morning_park:
    $ travel_to("park")
    $ go_to_time_slot("morning")
    $ set_story_music("park_breeze", fadein=1.5)
    scene bg_park at bg_slow_zoom_in
    with dissolve
    "Bay breeze drifted through the park's winding garden paths."
    priya "Saved you the corner seat. Breathe for a sec."
    maya "Mmm, pure peace."
    $ set_emotional_state("hopeful")
    maya_thought "Love this."
    menu:
        "Take the bold social angle":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("appeal", 3)
            $ update_relationship("priya", "friendship", 4)
            $ set_flag("day_08_morning_park_bold", True)
            priya "Bold call. Let's go."
        "Protect your cash and play it smart":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("financial_literacy", 3)
            $ set_flag("day_08_morning_park_solo", True)
            maya "Mmm, big chill."
    jump day_08_afternoon_tower

# Generated modular 2-option story beat (tower / afternoon / playful).

label day_08_afternoon_tower:
    $ travel_to("tower")
    $ go_to_time_slot("afternoon")
    $ set_story_music("city_hustle", fadein=1.5)
    scene bg_street at bg_slow_zoom_in
    with dissolve
    "The Observation Tower's clock chimed over the plaza."
    priya "Bet you five bucks you can't pull this off."
    maya "Oops— watch this."
    $ set_emotional_state("happy")
    maya_thought "Easy win."
    menu:
        "Take the bold social angle":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("appeal", 3)
            $ update_relationship("priya", "friendship", 4)
            $ set_flag("day_08_afternoon_tower_bold", True)
            priya "Bold call. Let's go."
        "Protect your cash and play it smart":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("financial_literacy", 3)
            $ set_flag("day_08_afternoon_tower_solo", True)
            maya "Heh. my bad."
    jump day_08_evening_harbor_pier

# Generated modular 2-option story beat (harbor_pier / evening / tense).

label day_08_evening_harbor_pier:
    $ travel_to("harbor_pier")
    $ go_to_time_slot("evening")
    $ set_story_music("park_breeze", fadein=1.5)
    scene bg_park at bg_slow_zoom_in
    with dissolve
    "Salt spray and ferry lights drifted across the bay piers."
    elena "Heads up—act natural and don't look back."
    maya "Hold up. play dumb."
    $ set_emotional_state("shy")
    maya_thought "Don't blink."
    menu:
        "Take the bold social angle":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("appeal", 3)
            $ update_relationship("elena", "friendship", 4)
            $ set_flag("day_08_evening_harbor_pier_bold", True)
            elena "Bold call. Let's go."
        "Protect your cash and play it smart":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("financial_literacy", 3)
            $ set_flag("day_08_evening_harbor_pier_solo", True)
            maya "Wait. eyes up."
    jump end_day_home
