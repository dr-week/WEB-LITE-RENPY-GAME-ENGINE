# LOLA - Public Locations
# Park, streets, and public spaces
# Ren'Py 8.6.0

label location_park:
    scene bg_park
    with dissolve

    $ unlock_location("park")
    $ travel_to("park")

    "A cool breeze moved through the park trees, miles quieter than the downtown avenues."

    menu:
        "Relax and clear her mind (+Appeal & Calm)":
            $ change_stat("energy", 10)
            $ change_stat("stress", -15)
            $ change_stat("appeal", 2)
            "Maya watched the light shift across the pond and felt her shoulders drop."
            jump day_hub_after_activity
        "Go for a brisk walk (+Health & Confidence)":
            $ change_stat("energy", -5)
            $ change_stat("health", 5)
            $ change_stat("confidence", 3)
            "A steady loop along the gravel path cleared the afternoon fog."
            jump day_hub_after_activity
        "Meet someone near the benches (+Communication)":
            call random_encounter
            jump day_hub_after_activity


label random_encounter:
    "Near the fountain benches, someone paused to ask about a campus shortcut."

    $ stranger = generate_encounter_character("stranger")

    menu:
        "Strike up a friendly chat with [stranger['display_name']]":
            $ update_relationship(stranger["character_id"], "friendship", 5)
            $ change_stat("appeal", 2)
            "A few easy jokes left the city feeling smaller and friendlier."
        "Share a warm nod and keep moving":
            $ change_stat("confidence", 2)
        "Observe the crowd and sketch notes from afar":
            $ reputation += 2
            $ change_stat("intelligence", 1)

    return


label location_street:
    $ travel_to("street")
    scene bg_street
    with dissolve

    "Maya wandered down the market block, taking in cafe chalkboards and shopfront windows."

    menu:
        "Window shop and note city style (+Appeal)":
            $ reputation += 3
            $ change_stat("appeal", 2)
            "She spotted two crisp outfits worth saving toward later in the term."
            jump day_hub_after_activity
        "Grab a quick street snack ($4)" if can_afford(4):
            $ spend_money(4, "Street snack")
            $ change_stat("energy", 8)
            "Warm food from a corner cart put fresh bounce back in her step."
            jump day_hub_after_activity
        "Compare student deals on local boards (+Financial Literacy)":
            $ change_stat("financial_literacy", 2)
            $ change_stat("intelligence", 1)
            "Comparing weekly specials showed her where to stretch her budget."
            jump day_hub_after_activity
