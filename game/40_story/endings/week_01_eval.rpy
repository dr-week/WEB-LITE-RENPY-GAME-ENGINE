# LOLA - End of Week 1 Milestone Evaluation.

label week_01_evaluation:
    $ travel_to("home")
    $ go_to_time_slot("morning")
    scene bg_home at bg_slow_zoom_in
    with dissolve

    "Day 7 - Week One Review"
    "One full week in the city. Maya opened her notebook and took stock of where things stood."

    $ portfolio = bitcoin_summary()
    $ btc_val = "{:.2f}".format(portfolio["value"])
    "Origin: [active_prologue_id or 'PROL_APT_MORNING'] | Journal Moments: [len(image_story_seen)]"
    "Education: [education_progress]/100 | Cash: [money] [currency] | BTC Value: [btc_val] | Shifts: [shifts_worked]"
    "Intelligence: [intelligence]/100 | Appeal: [appeal]/100 | Confidence: [confidence]/100 | Stress: [stress]/100"

    $ _ending = evaluate_week_01_ending()
    $ week_01_outcome = _ending["id"]
    $ set_emotional_state(_ending["mood"])
    "[_ending['title']] ([week_01_outcome]): [_ending['summary']]"

    menu:
        "Continue into Week 2 (Open City Life)":
            $ go_to_time_slot("afternoon")
            jump day_hub
        "Return to Main Menu":
            return
