# Modular random-start prologue loader backed by data/story_starts.json.

default active_prologue_id = ""

init python:
    import json

    def load_story_starts():
        try:
            with renpy.open_file("data/story_starts.json", encoding="utf-8") as handle:
                return json.load(handle).get("starts", [])
        except Exception:
            return []

    def select_random_prologue_start():
        starts = load_story_starts()
        chosen = pick_unseen_entry(starts, persistent.seen_prologue_starts, key="id")
        return chosen or {
            "id": "PROL_KITCHEN_OVERSLEPT", "location": "home", "scene": "scene_day1_home",
            "mood": "hopeful", "money": 120, "energy": 70, "next_label": "day_01_opening_choice",
            "beats": ["Maya woke up ready to test her luck in the city."],
        }

label prologue_random_start:
    $ go_to_time_slot("morning")
    $ _start_cfg = select_random_prologue_start()
    $ active_prologue_id = _start_cfg["id"]
    $ set_emotional_state(_start_cfg["mood"])
    $ travel_to(_start_cfg["location"])
    $ money = _start_cfg["money"]
    $ energy = _start_cfg["energy"]
    $ confidence, intelligence, appeal = 30, 10, 10
    $ employment_state, education_progress = "unemployed", 0
    $ mark_story_image_seen(_start_cfg["scene"])
    $ set_story_music("morning_wake", fadein=2.0)
    $ renpy.scene()
    $ renpy.show(_start_cfg["scene"], at_list=[bg_slow_zoom_in])
    with dissolve
    $ precache_images(["bg_college_entrance", "bg_bus_stop"])

    "Day 1 - Morning"

    $ _beats = _start_cfg["beats"]
    "[_beats[0]]"
    if len(_beats) > 1:
        "[_beats[1]]"
    $ _next_target = _start_cfg.get("next_label", "day_01_opening_choice")
    $ renpy.jump(_next_target)
