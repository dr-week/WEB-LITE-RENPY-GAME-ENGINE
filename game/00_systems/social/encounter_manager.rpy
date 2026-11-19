# LOLA - Generated character creation and promotion.

init python:
    def generate_encounter_character(scene_type, venue=None, gender_preference=None):
        global generated_characters
        gender = gender_preference or renpy.random.choice(["male", "female"])
        character_id = "gen_{}".format(renpy.random.randint(10000, 99999))
        personalities = {
            "classmate": ["friendly", "reserved", "ambitious", "quirky", "helpful"],
            "stranger": ["mysterious", "friendly", "distant", "curious", "nervous"],
            "coworker": ["supportive", "quiet", "talkative", "efficient", "witty"],
            "customer": ["polite", "demanding", "friendly", "rushed", "curious"],
            "neighbor": ["friendly", "reserved", "nosy", "helpful", "quiet"],
            "party_guest": ["outgoing", "shy", "friendly", "mysterious", "energetic"],
        }
        character = {
            "character_id": character_id,
            "display_name": generate_name(gender),
            "role": scene_type,
            "first_encounter": scene_type,
            "personality_tags": [renpy.random.choice(personalities.get(scene_type, ["neutral"]))],
            "recurring": False,
            "introduced": True,
            "friendship": 0,
            "romance": 0,
            "hostility": 0,
            "seen_events": [scene_type],
            "visual_asset_id": None,
            "gender": gender,
            "age": renpy.random.randint(18, 25),
            "is_adult": True,
            "venue_context": venue,
        }
        generated_characters[character_id] = character
        return character

    def promote_to_recurring(character_id, recurring_role, recurring_name=None):
        if character_id not in generated_characters:
            return False
        char = generated_characters[character_id]
        char["recurring"] = True
        char["role"] = recurring_role
        if recurring_name and recurring_name not in used_names:
            used_names.add(recurring_name)
            char["display_name"] = recurring_name
        return True
