# LOLA - Time Manager
# Handles days, time slots, and time progression
# Ren'Py 8.6.0

init python:
    # ============================================================================
    # TIME SYSTEM
    # ============================================================================
    
    time_slots = ["morning", "afternoon", "evening", "night"]
    
    def get_current_time_slot():
        """Get current time slot."""
        return time_slot
    
    def advance_time_slot():
        """Advance to next time slot."""
        global time_slot
        current_idx = time_slots.index(time_slot) if time_slot in time_slots else 0
        time_slot = time_slots[(current_idx + 1) % len(time_slots)]
    
    def go_to_time_slot(slot):
        """Set a specific time slot."""
        global time_slot
        if slot in time_slots:
            time_slot = slot
            return True
        return False
    
    def is_time_slot(slot):
        """Check if it's a specific time slot."""
        return time_slot == slot
    
    def start_new_day():
        """Start a new day with morning time slot."""
        global current_day, time_slot, energy, stress, shift_today
        current_day += 1
        time_slot = "morning"
        energy = min(100, energy + 20)
        stress = max(0, stress - 5)
        shift_today = False
    
    def get_day_info():
        """Get formatted day info."""
        return f"Day {current_day} - {time_slot.capitalize()}"
    
    def advance_days(n=1):
        """Advance multiple days (skip time)."""
        global current_day
        current_day += n
    
    def is_morning():
        return time_slot == "morning"
    
    def is_afternoon():
        return time_slot == "afternoon"
    
    def is_evening():
        return time_slot == "evening"
    
    def is_night():
        return time_slot == "night"
