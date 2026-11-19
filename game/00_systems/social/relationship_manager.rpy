# LOLA - Relationship updates and display descriptions.

init python:
    def update_relationship(character_id, relationship_type, amount, bounded=True):
        char = get_character_by_id(character_id)
        if not char:
            return False
        value = char.get(relationship_type, 0) + amount
        char[relationship_type] = max(0, min(100, value)) if bounded else value
        return True

    def get_relationship_level(value):
        if value < 10:
            return "strangers"
        elif value < 25:
            return "acquaintances"
        elif value < 50:
            return "friendly"
        elif value < 75:
            return "close"
        return "intimate"

    def get_relationship_description(character_id):
        char = get_character_by_id(character_id)
        if not char:
            return "Unknown"
        name = char.get("display_name", "Someone")
        parts = []
        for kind, label in (("friendship", "friendly"), ("romance", "romantic interest"),
                            ("hostility", "tension")):
            value = char.get(kind, 0)
            if value > 0:
                parts.append("{} ({})".format(label, get_relationship_level(value)))
        return "{}: {}".format(name, ", ".join(parts) if parts else "just met")
