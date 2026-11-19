# LOLA - Persistent playthrough defaults.

define protagonist_starting_money = 120

default current_day = 1
default time_slot = "morning"
default game_state = "playing"
default episode = 1
default current_location = "home"
default traveled_to = {"home": True}
default available_locations = ["home", "bus_stop", "college", "cafe"]

default reputation = 0
default relationship_count = 0
default energy = 70
default stress = 30
default confidence = 30
default health = 100
default learning = 0
default communication = 0
default work_skill = 0
default financial_literacy = 0
default intelligence = 10
default appeal = 10
default emotional_state = "hopeful"

default education_progress = 0
default has_college_id = False
default college_course = "General Studies"
default assignments_due = []
default classes_attended = 0

default employment_state = "unemployed"
default current_job = None
default shift_today = False
default work_experience = 0
default shifts_worked = 0
default workplace_hours = 0
default library_visits = 0

default recurring_characters = {}
default generated_characters = {}
default used_names = set()
default active_classmate_id = "elena"
default active_coworker_id = "marcus"
default active_study_partner_id = "priya"
default week_01_outcome = ""
default money = protagonist_starting_money
default currency = "dollars"
default wallet_ledger = []
default bitcoin_units = 0.0
default bitcoin_cost_basis = 0.0
default bitcoin_realized_gain = 0.0

default essential_costs = {"rent": 0, "food": 0, "transport": 0}
default recent_events = []
default day_summary = {}
default story_flags = {
    "has_seen_home": True,
    "has_seen_bus_stop": False,
    "has_reached_college": False,
    "has_met_first_classmate": False,
    "has_met_coworker": False,
    "has_searched_for_work": False,
    "has_first_job_interview": False,
    "has_first_shift": False,
    "has_met_library_staff": False,
    "has_visited_park": False,
}
