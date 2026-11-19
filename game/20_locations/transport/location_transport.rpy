# LOLA - Transport Location
# Bus and travel scenes
# Ren'Py 8.6.0

label location_bus_stop:
    scene bg_bus_stop
    with dissolve

    $ travel_to("bus_stop")

    "Maya reached the corner bus stop as city traffic hummed past."

    menu:
        "Take the bus to college ($2)" if can_afford(2):
            $ spend_money(2, "Bus fare")
            $ change_stat("energy", 3)
            "The bus arrives right on time."
            jump location_college
        "Walk toward campus (+Health & Save Cash)":
            $ change_stat("energy", -5)
            $ change_stat("health", 2)
            $ change_stat("financial_literacy", 1)
            jump location_college
        "People-watch at the stop (+Appeal & Reputation)":
            $ reputation += 2
            $ change_stat("appeal", 2)
            jump day_hub_after_activity
