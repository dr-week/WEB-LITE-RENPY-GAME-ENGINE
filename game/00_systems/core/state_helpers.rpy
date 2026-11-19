# LOLA - Protagonist configuration and playthrough-state helpers.

init python:
    protagonist = {
        "name": "Maya",
        "age": 19,
        "is_adult": True,
        "pronouns": "she/her",
        "starting_money": protagonist_starting_money,
    }

    def get_status_summary():
        return "Day {} - {} | Location: {} | Money: {} {} | Energy: {}/100".format(
            current_day, time_slot.capitalize(), current_location, money,
            currency, energy
        )

    def set_flag(flag_name, value=True):
        story_flags[flag_name] = value

    def get_flag(flag_name, default=False):
        return story_flags.get(flag_name, default)

    def has_flag(flag_name):
        return story_flags.get(flag_name, False)

    def add_recent_event(event_description):
        recent_events.insert(0, {
            "description": event_description,
            "day": current_day,
            "time": time_slot,
        })
        del recent_events[10:]

    def is_protagonist_adult():
        return protagonist.get("is_adult", False) and protagonist.get("age", 0) >= 18
