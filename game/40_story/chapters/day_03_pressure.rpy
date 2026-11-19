# LOLA - Chapter 2, Day 3: Midweek Financial Pressure.

label day_03_home:
    $ travel_to("home")
    $ go_to_time_slot("morning")
    scene bg_home at bg_slow_zoom_in
    with dissolve

    "Day 3 - Morning. The fridge hummed like an empty tin can."
    maya "{cps=26}Ugh... $[money] left till Friday. C'mon, Maya, figure it out...{/cps}"

    menu:
        "Grab a $6 bag of groceries & pack lunch" if can_afford(6):
            $ spend_money(6, "Groceries")
            $ change_stat("energy", 12)
            $ change_stat("financial_literacy", 3)
            $ change_stat("intelligence", 1)
            maya "Two days of real food for six bucks. Boring? Yeah. Smart? Definitely."
        "Pocket the cash & bluff through on tap water ($0)":
            $ change_stat("energy", -4)
            $ change_stat("financial_literacy", 2)
            $ change_stat("confidence", 2)
            maya "Zero dollars spent. Stomach's complainin', wallet's smilin'."

    scene cg_girl_sipping_espresso_at_cafe_36dbe4bd at cg_breathe
    with dissolve
    $ introduce_character("marcus")
    if is_employed():
        marcus "Yo, Maya—you look half-asleep already. Lemme pull a double shot before your shift, yeah?"
    else:
        marcus "Hey—don't tell the boss I said this, but we're short two hands. Need quick cash?"

    $ go_to_time_slot("afternoon")
    jump day_hub
