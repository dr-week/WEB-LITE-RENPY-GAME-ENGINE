# LOLA - New-game state reset and canonical cast registration.

init python:
    def init_new_game_state():
        global current_day, time_slot, game_state, episode, current_location
        global traveled_to, reputation, relationship_count, energy, stress
        global confidence, health, learning, communication, work_skill
        global financial_literacy, intelligence, appeal, emotional_state, education_progress
        global has_college_id, college_course, assignments_due, classes_attended
        global employment_state, current_job, shift_today, work_experience
        global shifts_worked, workplace_hours, library_visits, money
        global wallet_ledger, bitcoin_units, bitcoin_cost_basis
        global bitcoin_realized_gain, essential_costs, recent_events
        global day_summary, story_flags, recurring_characters
        global generated_characters, used_names, image_story_seen
        global image_story_seen_categories, active_classmate_id
        global active_coworker_id, active_study_partner_id, week_01_outcome, active_prologue_id

        current_day, time_slot, game_state, episode = 1, "morning", "playing", 1
        current_location = "home"
        traveled_to = {"home": True}
        reputation, relationship_count = 0, 0
        energy, stress, confidence, health = 70, 30, 30, 100
        learning, communication, work_skill, financial_literacy = 0, 0, 0, 0
        intelligence, appeal = 10, 10
        emotional_state = "hopeful"
        education_progress, has_college_id = 0, False
        college_course, assignments_due, classes_attended = "General Studies", [], 0
        employment_state, current_job, shift_today = "unemployed", None, False
        work_experience, shifts_worked, workplace_hours, library_visits = 0, 0, 0, 0
        money, wallet_ledger = protagonist_starting_money, []
        bitcoin_units, bitcoin_cost_basis, bitcoin_realized_gain = 0.0, 0.0, 0.0
        essential_costs = {"rent": 0, "food": 0, "transport": 0}
        recent_events, day_summary = [], {}
        image_story_seen, image_story_seen_categories = [], []
        active_classmate_id, active_coworker_id = "elena", "marcus"
        active_study_partner_id, week_01_outcome, active_prologue_id = "priya", "", ""
        story_flags = {
            "has_seen_home": True, "has_seen_bus_stop": False,
            "has_reached_college": False, "has_met_first_classmate": False,
            "has_met_coworker": False, "has_searched_for_work": False,
            "has_first_job_interview": False, "has_first_shift": False,
            "has_met_library_staff": False, "has_visited_park": False,
        }
        recurring_characters, generated_characters = {}, {}
        used_names = {"Maya", "Elena", "Marcus", "Priya"}
        _register_initial_cast()

    def _register_initial_cast():
        cast = [
            ("elena", "Elena", "classmate", 19),
            ("marcus", "Marcus", "coworker", 21),
            ("priya", "Priya", "study_partner", 20),
        ]
        for cid, name, role, age in cast:
            register_recurring_character(cid, {
                "character_id": cid, "display_name": name, "role": role,
                "recurring": True, "is_recurring": True,
                "friendship": 0, "romance": 0, "hostility": 0,
                "gender": "male" if cid == "marcus" else "female",
                "age": age, "is_adult": True, "introduced": False,
            })
