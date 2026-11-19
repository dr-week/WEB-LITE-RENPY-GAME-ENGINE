# LOLA - Authored and generated character registry.

init python:
    def register_recurring_character(character_id, data):
        recurring_characters[character_id] = data
        if data.get("name"):
            used_names.add(data["name"])

    def get_character_by_id(character_id):
        if character_id in recurring_characters:
            return recurring_characters[character_id]
        return generated_characters.get(character_id)

    def get_all_characters():
        all_chars = dict(recurring_characters)
        all_chars.update(generated_characters)
        return all_chars

    def get_character_count():
        return len(recurring_characters) + len(generated_characters)

    def remove_generated_character(character_id):
        if character_id not in generated_characters:
            return
        char = generated_characters[character_id]
        name = char.get("display_name")
        if name and name in used_names:
            uses = sum(1 for item in get_all_characters().values()
                       if item.get("display_name") == name)
            if uses <= 1:
                used_names.discard(name)
        del generated_characters[character_id]

    def list_characters_by_role(role):
        return [char for char in get_all_characters().values()
                if char.get("role") == role]
