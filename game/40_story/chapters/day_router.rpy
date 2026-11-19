# LOLA - Daily story progression router.

label day_router:
    $ go_to_time_slot("morning")

    if current_day == 1:
        jump day_01_home
    elif current_day == 2:
        jump day_02_home
    elif current_day == 3:
        jump day_03_home
    elif current_day == 4:
        jump day_04_home
    elif current_day == 5:
        jump day_05_home
    elif current_day == 6:
        jump day_06_home
    elif current_day == 7:
        jump week_01_evaluation
    elif current_day == 8:
        jump day_08_morning_park
    elif current_day == 9:
        jump day_09_morning_home
    elif current_day == 10:
        jump day_10_morning_home
    else:
        jump day_free_morning
