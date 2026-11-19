# LOLA - Prologue: Day 1 - Work Search
# Cafe job interview and first shift
# Ren'Py 8.6.0

label travel_to_cafe:
    $ go_to_time_slot("evening")
    $ travel_to("cafe")
    scene bg_cafe
    with dissolve

    "The cafe was busy. The smell of coffee filled the air."

    menu:
        "Ask about job openings":
            $ set_flag("has_first_job_interview", True)
            $ record_event("job_interview")
            jump cafe_job_interview
        "Save cash ($0) and watch how orders move":
            $ change_stat("financial_literacy", 2)
            $ change_stat("appeal", 1)
            jump cafe_look_around

label cafe_job_interview:
    "She approached the counter."
    scene cg_job_interview_at_cafe_counter_6cbfb206
    with dissolve
    "The manager looked up."
    if not get_flag("has_met_coworker"):
        $ active_coworker_id = "marcus"
        $ introduce_character("marcus")
        $ coworker = get_character_by_id("marcus")
        $ set_flag("has_met_coworker", True)
        $ record_event("first_coworker_meeting", "marcus")
    else:
        $ coworker = get_character_by_id(active_coworker_id)
    "[coworker['display_name']] - the cafe worker - caught her eye."
    menu:
        "Ask directly: 'I'm looking for work. Do you hire?'":
            $ set_flag("has_first_shift", True)
            $ record_event("first_shift")
            $ start_job(starter_job)
            jump first_work_shift
        "Ask Marcus what shifts are like and leave your resume":
            $ update_relationship(active_coworker_id, "friendship", 5)
            $ change_stat("appeal", 2)
            $ reputation += 5
            jump cafe_look_around

label cafe_look_around:
    scene cg_cafe_spill
    with dissolve
    "As she turns near the counter, a cup lid slips. Maya steadies it in time."
    "The barista grabs a towel with an easy grin. First impressions in this city stick."
    jump end_day_home

label first_work_shift:
    scene cg_girl_earning_money_at_cafe_089dec34
    with dissolve
    "Her first shift at the cafe."
    menu:
        "Work hard, watch the register, and learn fast":
            $ set_emotional_state("proud")
            $ work_shift()
            $ change_stat("work_skill", 2)
            $ change_stat("intelligence", 2)
            $ change_stat("financial_literacy", 2)
            $ update_relationship(active_coworker_id, "friendship", 10)
        "Charm the customers with warm service":
            $ set_emotional_state("hopeful")
            $ reputation += 10
            $ change_stat("appeal", 3)
            $ change_stat("communication", 2)
            $ update_relationship(active_coworker_id, "friendship", 5)
            $ work_shift()
    "Shift over. She had earned some money."
    jump end_day_home
