# Modular multi-ending evaluator with stable END_* identifiers.

init python:
    def evaluate_week_01_ending():
        if education_progress >= 45 and intelligence >= 20 and (money >= 120 or appeal >= 18) and stress <= 50:
            return {
                "id": "END_THRIVING",
                "mood": "proud",
                "title": "Thriving in the City",
                "summary": "Maya balanced sharp focus, genuine charm, work hours, and friendships without burning out.",
            }
        if appeal >= 22 or relationship_count >= 3:
            return {
                "id": "END_CONNECTOR",
                "mood": "hopeful",
                "title": "City Connector",
                "summary": "Maya turned every hallway, cafe, and plaza encounter into a real alliance across town.",
            }
        if len(image_story_seen) >= 4:
            return {
                "id": "END_WANDERER",
                "mood": "calm",
                "title": "City Chronicler",
                "summary": "From rooftops to late-night markets, Maya collected stories the rest of the campus never noticed.",
            }
        if education_progress >= 45 or intelligence >= 24:
            return {
                "id": "END_ACADEMIC",
                "mood": "hopeful",
                "title": "Dean's List Bound",
                "summary": "Her classes and library hours gave her real intellectual momentum.",
            }
        if shifts_worked >= 2 or money >= 140:
            return {
                "id": "END_INDEPENDENT",
                "mood": "proud",
                "title": "Hardworking Independent",
                "summary": "Maya proved she could stand on her own two feet financially.",
            }
        return {
            "id": "END_STEADY",
            "mood": "calm",
            "title": "Finding Her Footing",
            "summary": "The first week had bumps, yet the city finally felt navigable.",
        }
