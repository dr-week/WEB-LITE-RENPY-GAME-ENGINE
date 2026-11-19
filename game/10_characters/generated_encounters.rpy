# LOLA - Encounter categories and generated-character creation.

init python:
    encounter_types = {
        "classmate": {
            "description": "A fellow student",
            "gender_options": ["male", "female"],
            "recurring_possible": True,
            "promotion_channels": ["study_group", "project_partner"],
        },
        "stranger": {
            "description": "Someone you just met",
            "gender_options": ["male", "female"],
            "recurring_possible": False,
            "promotion_channels": [],
        },
        "coworker": {
            "description": "A fellow employee",
            "gender_options": ["male", "female", "nonbinary"],
            "recurring_possible": True,
            "promotion_channels": ["work_shift", "break_room"],
        },
        "customer": {
            "description": "A customer at your workplace",
            "gender_options": ["male", "female"],
            "recurring_possible": False,
            "promotion_channels": [],
        },
        "neighbor": {
            "description": "A neighbor in your building",
            "gender_options": ["male", "female"],
            "recurring_possible": True,
            "promotion_channels": ["building_hallway", "mailbox"],
        },
        "party_guest": {
            "description": "Someone at a social event",
            "gender_options": ["male", "female"],
            "recurring_possible": True,
            "promotion_channels": ["party", "after_party"],
        },
    }

    def create_encounter(encounter_type, venue=None):
        info = encounter_types.get(encounter_type, {})
        gender = renpy.random.choice(info.get("gender_options", ["male", "female"]))
        character_id = "gen_{}".format(renpy.random.randint(10000, 99999))
        character = {
            "character_id": character_id,
            "display_name": generate_name(gender),
            "role": encounter_type,
            "first_encounter": encounter_type,
            "personality": renpy.random.choice(
                ["friendly", "reserved", "talkative", "quiet", "curious"]),
            "friendship": 0,
            "romance": 0,
            "hostility": 0,
            "recurring": info.get("recurring_possible", False),
            "introduced": True,
            "visual_asset_id": None,
        }
        generated_characters[character_id] = character
        return character
