# LOLA - Chapter 4, Day 5: Assignment Deadline.

label day_05_home:
    $ travel_to("home")
    $ go_to_time_slot("morning")
    scene bg_home at bg_slow_zoom_in
    with dissolve

    "Day 5 - Friday Morning. Three minutes to deadline, ink still warm on the cover sheet."
    $ travel_to("college")
    scene cg_girl_arriving_at_campus_001950e9 at cg_breathe
    with dissolve
    $ attend_class()

    elena "Tell me you didn't write the conclusion on the bus again."
    maya "Hey, pressure makes diamonds—or at least decent footnotes. Watch this."

    menu:
        "Lead with sharp research & hard city numbers":
            $ change_stat("intelligence", 4)
            $ add_education_progress(6)
        "Sell the room with eye contact, wit & effortless poise":
            $ change_stat("appeal", 3)
            $ change_stat("communication", 3)
            $ reputation += 4

    if education_progress >= 30 or intelligence >= 18:
        $ complete_assignment("Week 1 Reflection Paper")
        $ reputation += 10
        $ change_stat("confidence", 8)
        $ set_emotional_state("proud")
        elena "Whoa—even prof nodded twice. You totally pulled that off!"
    else:
        $ complete_assignment("Week 1 Reflection Paper")
        $ change_stat("stress", 6)
        $ change_stat("work_skill", 1)
        $ set_emotional_state("tired")
        maya "{cps=24}Whew... barely made the bell. Brain's totally fried, m'kay.{/cps}"

    $ go_to_time_slot("afternoon")
    jump day_hub
