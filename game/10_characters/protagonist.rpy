# LOLA - Protagonist Definition
# Ren'Py 8.6.0

# ============================================================================
# PROTAGONIST CONFIGURATION (PROVISIONAL)
# ============================================================================
# These values are provisional until user confirmation.
# See: LOLA_Modular_Architecture_and_Safe_Migration_Plan_v0.5.md §2

# Note: protagonist_starting_money is defined in state.rpy

define maya = MayaCharacter("Maya", color="#f2d8ff", callback=maya_voice_callback)
define maya_thought = MayaCharacter(None, what_italic=True, what_color="#d8c8f2", callback=maya_voice_callback)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

init python:
    def get_protagonist_expression():
        """Get current protagonist expression based on state."""
        if stress > 70:
            return "worried"
        elif confidence < 20:
            return "neutral"
        elif energy < 20:
            return "tired"
        return "neutral"
