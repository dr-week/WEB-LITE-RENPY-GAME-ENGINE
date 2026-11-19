# LOLA - Day 9 (Campus Hustle)

# Generated modular 2-option story beat (home / morning / cozy).

label day_09_morning_home:
    $ travel_to("home")
    $ go_to_time_slot("morning")
    $ set_story_music("home_chill", fadein=1.5)
    scene bg_home at bg_slow_zoom_in
    with dissolve
    "Morning light hit Maya's desk. New day, clean slate."
    priya "Saved you the corner seat. Breathe for a sec."
    maya "Ooh, needed this."
    $ set_emotional_state("hopeful")
    maya_thought "Warm tea."
    menu:
        "Take the bold social angle":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("appeal", 3)
            $ update_relationship("priya", "friendship", 4)
            $ set_flag("day_09_morning_home_bold", True)
            priya "Bold call. Let's go."
        "Protect your cash and play it smart":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("financial_literacy", 3)
            $ set_flag("day_09_morning_home_solo", True)
            maya "Mmm, warm vibe."
    jump day_09_afternoon_college

# Generated modular 2-option story beat (college / afternoon / playful).

label day_09_afternoon_college:
    $ travel_to("college")
    $ go_to_time_slot("afternoon")
    $ set_story_music("college_social", fadein=1.5)
    scene bg_college_entrance at bg_slow_zoom_in
    with dissolve
    "Students spilled across the campus quad between bells."
    priya "Bet you five bucks you can't pull this off."
    maya "Oops— got 'em."
    $ set_emotional_state("teasing")
    maya_thought "Too smooth."
    menu:
        "Take the bold social angle":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("appeal", 3)
            $ update_relationship("priya", "friendship", 4)
            $ set_flag("day_09_afternoon_college_bold", True)
            priya "Bold call. Let's go."
        "Protect your cash and play it smart":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("financial_literacy", 3)
            $ set_flag("day_09_afternoon_college_solo", True)
            maya "Haha, my bad."
    jump day_09_evening_cafe

# Generated modular 2-option story beat (cafe / evening / hustle).

label day_09_evening_cafe:
    $ travel_to("cafe")
    $ go_to_time_slot("evening")
    $ set_story_music("cafe_work", fadein=1.5)
    scene bg_cafe at bg_slow_zoom_in
    with dissolve
    "Espresso steam curled through The Daily Grind's low lo-fi."
    maya "Okay, two plays here. No overthinking."
    maya "Say less. move fast."
    $ set_emotional_state("tired")
    maya_thought "Clean play."
    menu:
        "Take the bold social angle":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("appeal", 3)
            $ set_flag("day_09_evening_cafe_bold", True)
            maya "Bold call. Let's go."
        "Protect your cash and play it smart":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("financial_literacy", 3)
            $ set_flag("day_09_evening_cafe_solo", True)
            maya "Clock in. stack cash."
    jump end_day_home
