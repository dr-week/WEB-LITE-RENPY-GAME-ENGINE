# LOLA - Rolling 2-option-at-a-time afternoon & evening planner.

label day_hub:
    if time_slot == "night" or energy <= 10:
        if energy <= 10:
            "Maya's eyelids drooped—'m'kay... zero battery left, gotta crash.'"
        jump end_day_home

    $ slot_label = time_slot.capitalize()
    $ sync_mood_from_wellbeing()
    $ _hook = planner_mood_hook()
    $ _pair = roll_planner_pair()
    "Day [current_day] ([slot_label]) • $[money] • [energy]/100 Energy — [_hook]"

label day_hub_roll:
    $ _opt_a, _opt_b = _pair[0], _pair[1]
    menu:
        "[_opt_a['hook']]\n→ [_opt_a['label']]":
            $ change_stat(_opt_a["stat"][0], _opt_a["stat"][1])
            if _opt_a["extra"] == "edu":
                $ add_education_progress(2)
            $ renpy.jump(_opt_a["dest"])
        "[_opt_b['hook']]\n→ [_opt_b['label']]":
            $ change_stat(_opt_b["stat"][0], _opt_b["stat"][1])
            if _opt_b["extra"] == "edu":
                $ add_education_progress(2)
            $ renpy.jump(_opt_b["dest"])
        "Roll two other leads...":
            $ _pair = roll_planner_pair()
            jump day_hub_roll

label day_hub_lifestyle:
    jump day_hub

label day_hub_after_activity:
    $ advance_time_slot()
    if time_slot == "night" or time_slot == "morning":
        jump end_day_home
    jump day_hub
