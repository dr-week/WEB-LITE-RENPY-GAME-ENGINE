# LOLA - Chapter 3, Day 4: Building Connections.

label day_04_home:
    $ travel_to("home")
    $ go_to_time_slot("morning")
    scene bg_home at bg_slow_zoom_in
    with dissolve

    "Day 4 - Morning. Maya's phone buzzed before she even laced her sandals: two unread texts from campus."
    $ unlock_location("library")
    $ unlock_location("park")
    $ travel_to("library")
    scene cg_girl_reading_textbook_in_library_d2c016ba at cg_breathe
    with dissolve

    $ introduce_character("elena")
    $ introduce_character("priya")
    priya "You're six minutes late, which means you owe us coffee—or at least the good highlighter."
    elena "Shh, librarian's watchin'. C'mere, sit—we're drowning in source notes."

    menu:
        "Team up with Elena & Priya and split the reading list":
            $ update_relationship("elena", "friendship", 10)
            $ update_relationship("priya", "friendship", 10)
            $ add_education_progress(10)
            $ change_stat("communication", 2)
            $ change_stat("appeal", 2)
            priya "Okay, not bad. Keep that pace and we might actually survive Friday."
        "Bail out to City Park for ten minutes of fresh air & quiet focus":
            $ add_education_progress(12)
            $ change_stat("intelligence", 4)
            $ change_stat("stress", -10)
            $ change_stat("energy", 8)
            maya "{cps=30}S'fine, lemme clear my head outside—I'll send my half in twenty.{/cps}"

    $ go_to_time_slot("afternoon")
    jump day_hub
