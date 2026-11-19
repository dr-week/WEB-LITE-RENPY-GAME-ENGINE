# LOLA - Relationship queries and character summaries.

init python:
    def get_strongest_relationship(character_id):
        char = get_character_by_id(character_id)
        if not char:
            return None
        levels = {kind: char.get(kind, 0)
                  for kind in ("friendship", "romance", "hostility")}
        strongest = max(levels, key=levels.get)
        return strongest if levels[strongest] >= 5 else None

    def can_characters_interact(character_id1, character_id2):
        return bool(get_character_by_id(character_id1) and
                    get_character_by_id(character_id2))

    def get_relationship_summary_for_character(character_id):
        char = get_character_by_id(character_id)
        if not char:
            return "Character not found"
        lines = ["{} ({})".format(char.get("display_name", "Unknown"),
                                  char.get("role", "unknown"))]
        for kind in ("friendship", "romance", "hostility"):
            lines.append("  {}: {}/100".format(
                kind.capitalize(), char.get(kind, 0)))
        return "\n".join(lines)

    def is_relationship_meaningful(character_id):
        char = get_character_by_id(character_id)
        return bool(char and any(char.get(kind, 0) > 10
                                 for kind in ("friendship", "romance", "hostility")))
