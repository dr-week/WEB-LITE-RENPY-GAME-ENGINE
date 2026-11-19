# LOLA - Home Location
# Home scene and interactions
# Ren'Py 8.6.0

label location_home:
    $ travel_to("home")
    scene bg_home
    with dissolve

    "Maya unlocked her apartment door and set her bag down beside the kitchen counter."

    menu:
        "Rest and recharge":
            $ change_stat("energy", 15)
            $ change_stat("stress", -10)
            $ change_stat("appeal", 1)
            "Half an hour with tea and quiet music took the edge off the rush."
            menu:
                "Take an evening breather and keep the day going":
                    jump day_hub_after_activity
                "Call it a night and go to sleep":
                    jump end_day_home
        "Study at her desk (+Intelligence & Education)":
            $ add_education_progress(10)
            $ change_stat("intelligence", 2)
            $ change_stat("energy", -10)
            scene cg_girl_checking_plans_at_home_aaa53bbd
            with dissolve
            "Maya opened her notebook under the desk lamp and worked cleanly through her outline."
            jump day_hub_after_activity
        "Review finances & fictional Bitcoin (+Financial Literacy)":
            call show_money_status
            $ change_stat("financial_literacy", 2)
            jump location_home


label show_money_status:
    scene cg_checking_bank_balance_on_phone_aaf91257
    with dissolve
    $ btc_amount = "{:.4f}".format(bitcoin_units)
    "Maya checked her monthly notebook: $[money] [currency] in cash and [btc_amount] BTC held."

    menu:
        "Buy $20 of fictional Bitcoin" if can_afford(20):
            $ buy_bitcoin(20)
            "The purchase was recorded in Maya's offline wallet."
            jump show_money_status
        "Sell half the Bitcoin held" if bitcoin_units > 0:
            $ sell_bitcoin(bitcoin_units / 2.0)
            "The sale settled cleanly back into her cash balance."
            jump show_money_status
        "Return":
            return
