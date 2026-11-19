# LOLA - Work Location
# Workplace scenes and interactions
# Ren'Py 8.6.0

label location_work:
    scene bg_cafe
    with dissolve
    $ travel_to("cafe")
    "Steam and roasted beans filled The Daily Grind Cafe as customers queued along the counter."
    if not is_employed():
        menu:
            "Ask about job openings":
                $ set_flag("has_first_job_interview", True)
                jump cafe_job_interview_location
            "Order coffee and unwind ($5)" if can_afford(5):
                $ spend_money(5, "Coffee")
                $ change_stat("energy", 6)
                $ change_stat("appeal", 2)
                jump day_hub_after_activity
            "Study cafe menu pricing ($0)":
                $ change_stat("financial_literacy", 2)
                jump day_hub_after_activity
    else:
        menu:
            "Start her shift (+Money & Work Skill)":
                $ set_flag("has_first_shift", True)
                $ record_event("first_shift")
                jump cafe_shift_scene
            "Take a break with Marcus (+Appeal)":
                call coworker_break
                jump day_hub_after_activity
            "Review shift tips and rest (+Energy)":
                $ change_stat("energy", 5)
                $ change_stat("work_skill", 1)
                jump day_hub_after_activity

label cafe_job_interview_location:
    scene cg_job_interview_at_cafe_counter_6cbfb206
    with dissolve
    "Maya stepped up to the counter, where the manager checked schedules while Marcus wiped the espresso bar."
    $ introduce_character(active_coworker_id)
    $ set_flag("has_met_coworker", True)
    menu:
        '"I\'m looking for part-time hours. Are you still hiring?"':
            $ start_job(starter_job)
            $ change_stat("confidence", 3)
            jump cafe_shift_scene
        '"Could I leave my resume for the weekend roster?"':
            $ reputation += 5
            $ change_stat("intelligence", 2)
            jump day_hub_after_activity
        "Ask Marcus what the barista shifts are like":
            $ update_relationship(active_coworker_id, "friendship", 4)
            $ change_stat("appeal", 2)
            jump day_hub_after_activity

label cafe_shift_scene:
    scene cg_girl_earning_money_at_cafe_089dec34
    with dissolve
    "Maya tied her apron on and stepped behind the counter beside Marcus."
    $ introduce_character(active_coworker_id)
    menu:
        "Work fast and keep orders moving cleanly":
            $ change_stat("work_skill", 2)
            $ change_stat("intelligence", 1)
            $ work_shift()
            $ update_relationship(active_coworker_id, "friendship", 10)
        "Keep a steady pace at the register":
            $ work_shift()
            $ change_stat("financial_literacy", 2)
        "Greet regulars warmly and boost tips":
            $ reputation += 10
            $ change_stat("appeal", 3)
            $ change_stat("communication", 2)
            $ update_relationship(active_coworker_id, "friendship", 5)
            $ work_shift()
    "By the end of the shift, Maya's feet ached, but her wallet felt noticeably heavier."
    jump day_hub_after_activity

label coworker_break:
    scene cg_girl_sipping_espresso_at_cafe_36dbe4bd
    with dissolve
    $ introduce_character(active_coworker_id)
    "Maya grabbed two mugs and slid into the corner booth with Marcus for ten quiet minutes."
    $ update_relationship(active_coworker_id, "friendship", 5)
    menu:
        "Swap tips on handling rush-hour orders":
            $ update_relationship(active_coworker_id, "friendship", 5)
            $ change_stat("work_skill", 1)
        "Trade stories about settling into the city":
            $ update_relationship(active_coworker_id, "friendship", 8)
            $ change_stat("appeal", 2)
            $ change_stat("confidence", 4)
        "Enjoy a quiet espresso and catch her breath":
            $ change_stat("energy", 6)
            $ change_stat("stress", -5)
    return
