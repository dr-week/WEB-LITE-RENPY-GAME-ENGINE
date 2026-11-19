# LOLA - Event Manager
# Handles story events and tracking
# Ren'Py 8.6.0

init python:
    # ============================================================================
    # EVENT SYSTEM
    # ============================================================================
    
    # Events are tracked per character and globally
    
    def record_event(event_type, character_id=None, details=None):
        """Record a story event."""
        global recent_events, story_flags
        
        event = {
            "type": event_type,
            "character_id": character_id,
            "details": details or {},
            "day": current_day,
            "time_slot": time_slot,
        }
        
        recent_events.insert(0, event)
        
        # Keep only last 20 events
        if len(recent_events) > 20:
            recent_events = recent_events[-20:]
        
        # Set flag if applicable
        if event_type == "first_classmate_meeting":
            story_flags["has_met_first_classmate"] = True
        elif event_type == "first_coworker_meeting":
            story_flags["has_met_coworker"] = True
        elif event_type == "first_shift":
            story_flags["has_first_shift"] = True
        elif event_type == "reached_college":
            story_flags["has_reached_college"] = True
    
    def get_recent_events(limit=5):
        """Get recent events."""
        return recent_events[:limit]
    
    def has_event_type(event_type):
        """Check if an event type has occurred."""
        for event in recent_events:
            if event["type"] == event_type:
                return True
        return False
    
    def get_events_for_character(character_id):
        """Get all events involving a character."""
        events = []
        for event in recent_events:
            if event["character_id"] == character_id:
                events.append(event)
        return events
    
    def record_day_summary(summary_dict):
        """Record a summary of the day."""
        day_summary[current_day] = summary_dict
    
    def get_day_summary(day=None):
        """Get summary for a day."""
        if day is None:
            day = current_day
        return day_summary.get(day, {})
    
    def clear_recent_events():
        """Clear recent events (for testing or major transitions)."""
        global recent_events
        recent_events = []
