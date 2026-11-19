# LOLA - Prologue: Day 1 - Class and study
# High-stakes lecture and campus infiltration
# Ren'Py 8.6.0

label class_session:
    scene bg_classroom with dissolve
    $ attend_class()
    $ go_to_time_slot("afternoon")
    $ set_story_music("study_focus", fadein=2.0)
    scene cg_professor_teaching_college_lecture_957ef9f4 with dissolve
    "The lecture hall was packed with competitive business majors."
    "The professor scanned the room. Maya kept her chin up, radiating effortless pedigree."
    menu:
        "Dominate the academic discussion":
            play sound SFX_SWOOSH
            $ add_education_progress(10)
            $ change_stat("intelligence", 3)
            menu:
                "Deliver a flawless analysis of market leverage":
                    $ change_stat("intelligence", 2)
                    $ change_stat("confidence", 3)
                    "The professor paused, impressed. Several students turned around to look at her."
                "Politely challenge the professor's textbook theory":
                    $ change_stat("confidence", 5)
                    $ reputation += 5
                    "A calculated gamble that marked Maya as someone who didn't play by ordinary rules."
        "Study the classroom hierarchy for leverage":
            play sound SFX_WOOSH
            $ change_stat("appeal", 2)
            $ change_stat("communication", 2)
            menu:
                "Note who the wealthy trust-fund students flock to":
                    $ change_stat("intelligence", 2)
                    "Maya mapped the room's informal social power structures."
                "Pass a coded note to Elena testing her loyalties":
                    $ update_relationship(active_classmate_id, "friendship", 8)
                    $ change_stat("confidence", 4)
                    "Elena glanced at the folded paper and smirked back knowingly."

    "Class concluded. Maya packed her notebook with purpose."
    menu:
        "Pursue social infiltration":
            play sound SFX_SWOOSH
            menu:
                "Invite Elena for coffee to uncover her background":
                    $ update_relationship(active_classmate_id, "friendship", 10)
                    jump location_library
                "Infiltrate the student business society mixer":
                    $ change_stat("appeal", 3)
                    jump location_library
        "Hunt for immediate cash flow":
            play sound SFX_WOOSH
            $ set_flag("has_searched_for_work", True)
            menu:
                "Scout the campus cafe for counter job openings":
                    $ change_stat("work_skill", 1)
                    jump travel_to_cafe
                "Inspect high-end bulletin boards for lucrative private gigs":
                    $ change_stat("intelligence", 2)
                    jump travel_to_cafe
