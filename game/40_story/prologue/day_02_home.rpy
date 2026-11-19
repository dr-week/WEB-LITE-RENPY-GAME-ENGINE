# LOLA - Prologue: Day 2 - A New Routine

label day_02_home:
    $ travel_to("home")
    $ go_to_time_slot("morning")
    scene bg_home
    with dissolve

    scene cg_girl_checking_plans_at_home_aaa53bbd
    with dissolve
    "Day [current_day] - Morning"
    "Yesterday left her tired, but the city felt a little less unfamiliar."
    "She checked her plans before stepping into the day."

    menu:
        "Review yesterday's notes before class":
            $ change_stat("intelligence", 3)
            $ change_stat("confidence", 3)
            $ add_education_progress(2)
        "Pull a sharp outfit together & catch your breath":
            $ change_stat("appeal", 3)
            $ change_stat("energy", 8)

    "For the first time, the day ahead felt like something she could shape."
    menu:
        "Head to morning class (+Intelligence)":
            $ change_stat("intelligence", 1)
            jump day_02_class_beat
        "Open Maya's City Journal (+Appeal)":
            $ change_stat("appeal", 1)
            $ go_to_time_slot("afternoon")
            jump image_story_hub
