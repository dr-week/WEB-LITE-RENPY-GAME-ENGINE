# LOLA - Chapter 1, Day 2: Morning Class & First Assignment.

label day_02_class_beat:
    $ travel_to("college")
    $ go_to_time_slot("morning")
    scene bg_classroom at bg_slow_zoom_in
    with dissolve

    $ introduce_character("elena")
    "The heavy oak door clicked shut half a second behind Maya's heel."
    elena "{cps=40}Psst—over here! Saved you the middle seat before prof started his whole dramatic glare thing.{/cps}"
    scene cg_girl_passing_note_in_classroom_0058f8dc at cg_breathe
    with dissolve
    maya "You're a lifesaver. Seriously, slept right through two alarms—brain's still mush."
    "Elena slid a folded doodle across the desk right as the professor tapped the board: Week 1 Reflection Paper, due Friday."
    elena "Y'know... we split the reading, or we both suffer till midnight. Whaddaya say?"

    $ attend_class()
    $ add_assignment("Week 1 Reflection Paper", due_day=5)

    menu:
        "Trade shorthand pages & banter with Elena after the bell":
            $ update_relationship("elena", "friendship", 8)
            $ change_stat("appeal", 2)
            $ change_stat("communication", 2)
            $ confidence = min(100, confidence + 4)
            elena "Deal. You charm the TA if we're late, I'll handle the citations—m'kay?"
        "Wave her off for five minutes & outline the paper solo":
            $ add_education_progress(6)
            $ change_stat("intelligence", 3)
            $ change_stat("learning", 2)
            maya "Rain check—lemme lock these three thesis hooks down before they evaporate."

    $ go_to_time_slot("afternoon")
    jump day_hub
