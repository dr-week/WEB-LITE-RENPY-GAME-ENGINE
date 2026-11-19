# LOLA - Promotion and lookup helpers for generated encounters.

init python:
    def promote_encounter_to_recurring(character_id, new_role=None):
        char = get_character_by_id(character_id)
        if not char:
            return False
        info = encounter_types.get(char.get("role"), {})
        if not info.get("recurring_possible", False):
            return False
        if new_role:
            char["role"] = new_role
        char["recurring"] = True
        return True

    def is_recurring(character_id):
        char = get_character_by_id(character_id)
        return bool(char and char.get("recurring", False))

    def get_encounter_by_type(encounter_type):
        return [char for char in generated_characters.values()
                if char.get("role") == encounter_type]
