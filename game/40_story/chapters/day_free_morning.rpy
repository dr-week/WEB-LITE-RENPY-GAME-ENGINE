# LOLA - Open-ended daily routine after Week 1.

label day_free_morning:
    $ travel_to("home")
    $ go_to_time_slot("morning")
    scene bg_home
    with dissolve

    "Day [current_day] - Morning"
    "Another morning in the city. Maya rolled her shoulders and checked what needed attention today."

    menu:
        "Do a quick morning stretch and freshen up":
            $ change_stat("energy", 10)
            $ change_stat("health", 2)
            $ change_stat("appeal", 2)
        "Review class notes over tea & check wallet":
            $ add_education_progress(5)
            $ change_stat("intelligence", 2)
            $ change_stat("financial_literacy", 2)

    $ go_to_time_slot("afternoon")
    jump day_hub
