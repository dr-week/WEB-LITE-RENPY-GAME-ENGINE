# Rolling 2-option planner leads with narrative hooks and stat consequences.

default planner_seen_leads = []

init python:
    import random

    PLANNER_LEADS = [
        {"id": "lead_lab_cram", "label": "Sneak into the quiet upper-floor lab (+Intelligence & +2% Edu)",
         "hook": "Someone left a half-empty cold brew and a study guide on the back desk.",
         "stat": ("intelligence", 3), "extra": "edu", "dest": "location_college"},
        {"id": "lead_cafe_rush", "label": "Cover Marcus's chaotic rush hour at Daily Grind (+Cash & Work Skill)",
         "hook": "Marcus texted: 'espresso machine's hissin' like an angry cat, c'mon rescue me.'",
         "stat": ("work_skill", 2), "extra": None, "dest": "location_work"},
        {"id": "lead_journal_roam", "label": "Chase a wild city story in Maya's Journal (Visual Story Moment)",
         "hook": "A neon flyer blew right across her sandal—some rooftop thing, or maybe a late-night market.",
         "stat": ("appeal", 2), "extra": None, "dest": "image_story_hub"},
        {"id": "lead_park_breeze", "label": "Crash on a shaded park bench & people-watch (-Stress & +Appeal)",
         "hook": "Head's buzzin' from lectures; five minutes under the trees sounds like heaven.",
         "stat": ("appeal", 2), "extra": None, "dest": "location_park"},
        {"id": "lead_street_haggle", "label": "Work the street market stalls for flips (+Financial Literacy)",
         "hook": "Half the vendors mark up prices for tourists—Maya's got an itch to talk 'em down.",
         "stat": ("financial_literacy", 2), "extra": None, "dest": "location_street"},
        {"id": "lead_home_crash", "label": "Head back to the apartment & lock the door (+Energy & Budget)",
         "hook": "Feet are aching, brain's mush—time to kick off the sandals and count every dollar.",
         "stat": ("confidence", 2), "extra": None, "dest": "location_home"},
    ]

    def roll_planner_pair():
        global planner_seen_leads
        unseen = [item for item in PLANNER_LEADS if item["id"] not in planner_seen_leads]
        if len(unseen) < 2:
            planner_seen_leads = []
            unseen = list(PLANNER_LEADS)
        pair = random.sample(unseen, 2)
        planner_seen_leads.extend(item["id"] for item in pair)
        return pair

    def planner_mood_hook():
        if energy <= 30:
            return "Maya's words slurred slightly under her breath—'ugh, need coffee or a nap, stat.'"
        if stress >= 60:
            return "Pulse ticking fast, Maya tapped her thumb on her phone. 'Gotta play this smart.'"
        if time_slot == "evening":
            return "Streetlights flickered on outside. 'Night's still young—where's the real action?'"
        return "Sunlit breeze hit the sidewalk. 'Alright, city—whaddaya got for me next?'"
