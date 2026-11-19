# LOLA - Prologue: end-of-day transition.

label end_day_home:
    $ travel_to("home")
    $ go_to_time_slot("night")
    scene bg_home
    with dissolve
    "Home again."
    "Day [current_day] complete."
    menu:
        "Go to sleep":
            jump end_day


label end_day:
    $ daily_expenses()
    $ record_day_summary({"money": money, "energy": energy, "stress": stress})
    $ start_new_day()
    "The sun set. A new day would come."
    menu:
        "Continue to Day 2" if current_day == 2:
            jump day_router
        "Continue to Day [current_day]" if current_day != 2:
            jump day_router
