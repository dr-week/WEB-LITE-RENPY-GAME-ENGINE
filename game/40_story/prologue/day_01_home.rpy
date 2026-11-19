# LOLA - Prologue: Day 1 - Home
# Morning scene with financial pressure and iconic 2-choice decision branching
# Ren'Py 8.6.0

label day_01_home:
    $ set_emotional_state("hopeful")
    $ go_to_time_slot("morning")
    $ travel_to("home")
    $ set_story_music("morning_wake", fadein=2.5)
    $ money = protagonist["starting_money"]
    $ energy = 70
    $ confidence = 30
    $ intelligence = 10
    $ appeal = 10
    $ employment_state = "unemployed"
    $ education_progress = 0

    scene scene_day1_home at bg_slow_zoom_in
    with dissolve
    $ precache_images(["bg_college_entrance", "bg_bus_interior", "char_maya_normal"])

    "The thin mattress creaked under Maya's weight as morning light filtered through dusty blinds."
    "Maya took a slow breath, centering herself."
    "Today was Day 1 in the city. The rent was overdue, and her pockets were nearly hollow."
    "Bank balance: [money] [currency]. Barely enough for transit, coffee, and a bold first impression."
    "Maya smiled innocently at the cracked kitchen mirror. If the city wanted to test her, she'd play along—and win."

label day_01_opening_choice:
    menu:
        "[charm] Dress sharp and project effortless high status":
            play sound SFX_SWOOSH
            $ change_stat("appeal", 3)
            $ change_stat("confidence", 3)
            menu:
                "[charm] Apply luxury perfume and bold lipstick":
                    $ change_stat("appeal", 2)
                    $ change_stat("energy", -5)
                    "Maya checked her reflection. 'First impressions decide who holds the leverage.'"
                    jump travel_bus_stop
                "[stealth] Keep it sleek, understated, and minimalist":
                    $ change_stat("confidence", 2)
                    $ change_stat("intelligence", 1)
                    "Understated, sharp, and confident. Nobody would guess her bank balance."
                    jump travel_bus_stop

        "[logic] Study transit lines and execute a calculated plan":
            play sound SFX_WOOSH
            $ change_stat("intelligence", 3)
            $ change_stat("confidence", 2)
            menu:
                "[cash] Memorize the express bus schedule to save fares":
                    $ change_stat("financial_literacy", 2)
                    $ change_stat("energy", 3)
                    "Efficiency meant saving dollars and avoiding delays."
                    jump travel_bus_stop
                "[target] Scan local notice boards for fast cash opportunities":
                    $ change_stat("intelligence", 2)
                    $ change_stat("confidence", 2)
                    "Maya bookmarked a few notice boards. Information was always currency."
                    jump travel_bus_stop
