# Player skill and wellbeing rules.
init python:
    def change_stat(name, amount):
        allowed = ("learning", "communication", "work_skill", "financial_literacy",
                   "intelligence", "appeal", "confidence", "energy", "stress", "health")
        if name not in allowed:
            return False
        globals()[name] = max(0, min(100, globals()[name] + amount))
        return True

    def set_emotional_state(state):
        global emotional_state
        allowed = ("calm", "anxious", "hopeful", "embarrassed", "tired", "proud")
        if state in allowed:
            emotional_state = state
            return True
        return False

    def get_player_profile():
        return {"learning": learning, "communication": communication,
                "work_skill": work_skill, "financial_literacy": financial_literacy,
                "intelligence": intelligence, "appeal": appeal,
                "energy": energy, "stress": stress, "health": health,
                "emotional_state": emotional_state}

    def sync_mood_from_wellbeing():
        if stress >= 75 or energy <= 20:
            set_emotional_state("anxious" if stress >= 75 else "tired")
        elif energy >= 60 and stress <= 30:
            set_emotional_state("hopeful")
        return emotional_state

    def daily_goal_hint():
        if stress >= 70:
            return "Maya's stress is high — resting at the park or home will restore her focus."
        if education_progress < 35:
            return "Week 1 Goal: Attend classes or study at the library to build Education."
        if money < 160 and work_experience < 2:
            return "Week 1 Goal: Take a cafe shift to pad Maya's budget for rent."
        return "Maya is on track — explore Maya's City Journal or deepen friendships."
