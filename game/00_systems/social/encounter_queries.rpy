# LOLA - Generated character recurrence and event queries.

init python:
    def can_character_recur(character_id):
        char = get_character_by_id(character_id)
        return bool(char and char.get("recurring") and len(char.get("seen_events", [])) >= 2)

    def record_character_event(character_id, event_type):
        char = get_character_by_id(character_id)
        if char and event_type not in char["seen_events"]:
            char["seen_events"].append(event_type)

    def get_character_summary(character_id):
        char = get_character_by_id(character_id)
        if not char:
            return "Unknown character"
        parts = []
        for kind, label in (("friendship", "friendship"), ("romance", "romance"),
                            ("hostility", "tension")):
            value = char.get(kind, 0)
            if value > 0:
                parts.append("{}: {}".format(label, get_relationship_level(value)))
        status = ", ".join(parts) if parts else "no relationship yet"
        return "{} ({}) - {}".format(char["display_name"], char["role"], status)
