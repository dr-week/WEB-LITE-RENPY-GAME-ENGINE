# LOLA - Day 10 (Library Mystery)

# Generated modular 2-option story beat (home / morning / cozy).

label day_10_morning_home:
    $ travel_to("home")
    $ go_to_time_slot("morning")
    $ set_story_music("home_chill", fadein=1.5)
    scene bg_home at bg_slow_zoom_in
    with dissolve
    "Morning light hit Maya's desk. New day, clean slate."
    priya "Saved you the corner seat. Breathe for a sec."
    maya "Ooh, big chill."
    $ set_emotional_state("tired")
    maya_thought "Breathe out."
    menu:
        "Take the bold social angle":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("appeal", 3)
            $ update_relationship("priya", "friendship", 4)
            $ set_flag("day_10_morning_home_bold", True)
            priya "Bold call. Let's go."
        "Protect your cash and play it smart":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("financial_literacy", 3)
            $ set_flag("day_10_morning_home_solo", True)
            maya "Nice. warm vibe."
    jump day_10_afternoon_library

# Generated modular 2-option story beat (library / afternoon / tense).

label day_10_afternoon_library:
    $ travel_to("library")
    $ go_to_time_slot("afternoon")
    $ set_story_music("study_focus", fadein=1.5)
    scene bg_library at bg_slow_zoom_in
    with dissolve
    "Rain tapped the glass rotunda over quiet oak tables."
    elena "Heads up—act natural and don't look back."
    maya "Hold up. eyes up."
    $ set_emotional_state("worried")
    maya_thought "Quiet steps."
    menu:
        "Take the bold social angle":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("appeal", 3)
            $ update_relationship("elena", "friendship", 4)
            $ set_flag("day_10_afternoon_library_bold", True)
            elena "Bold call. Let's go."
        "Protect your cash and play it smart":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("financial_literacy", 3)
            $ set_flag("day_10_afternoon_library_solo", True)
            maya "Wait. no panic."
    jump day_10_evening_viewpoint

# Generated modular 2-option story beat (viewpoint / evening / hustle).

label day_10_evening_viewpoint:
    $ travel_to("viewpoint")
    $ go_to_time_slot("evening")
    $ set_story_music("park_breeze", fadein=1.5)
    scene bg_park at bg_slow_zoom_in
    with dissolve
    "All of Solis Bay sparkled below Pinecrest Ridge."
    maya "Okay, two plays here. No overthinking."
    maya "Bet. lock in."
    $ set_emotional_state("proud")
    maya_thought "Clean play."
    menu:
        "Step up and own the spotlight":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("confidence", 4)
            $ set_flag("day_10_evening_viewpoint_bold", True)
            maya "Bold call. Let's go."
        "Hang back and pocket the edge":
            play sound SFX_SWOOSH_SOFT
            $ change_stat("learning", 3)
            $ set_flag("day_10_evening_viewpoint_solo", True)
            maya "Clock in. stack cash."
    jump end_day_home
