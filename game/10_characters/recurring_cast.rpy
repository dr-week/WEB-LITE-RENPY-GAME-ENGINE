# LOLA - Recurring Cast Definitions
# Authored characters that persist throughout the game
# Ren'Py 8.6.0

define elena = Character("Elena", color="#9ee7ff")
define marcus = Character("Marcus", color="#ffd08a")
define priya = Character("Priya", color="#b8f2b8")

init python:
    # ============================================================================
    # CHARACTER HELPER FUNCTIONS
    # ============================================================================

    def is_character_introduced(character_id):
        """Check if a recurring character has been introduced."""
        char = get_character_by_id(character_id)
        if not char:
            return False
        return char.get("introduced", False)

    def introduce_character(character_id):
        """Mark a recurring character as introduced."""
        char = get_character_by_id(character_id)
        if char:
            char["introduced"] = True

    def get_recurring_character_count():
        """Get count of recurring characters."""
        return len(recurring_characters)

    def list_recurring_characters():
        """List all recurring characters."""
        return list(recurring_characters.values())
