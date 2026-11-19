# LOLA - College Location
# College scenes and interactions
# Ren'Py 8.6.0

label location_college:
    scene bg_classroom
    with dissolve

    $ travel_to("college")

    "Maya stepped onto campus as students hurried between the lecture halls and quad."

    menu:
        "Attend class (+Education & Intelligence)":
            $ attend_class()
            $ change_stat("intelligence", 2)
            scene cg_professor_teaching_college_lecture_957ef9f4
            with dissolve
            "Maya followed the lecture closely and added sharp notes to her folder."
            jump day_hub_after_activity
        "Study at the library (+Learning)":
            $ unlock_location("library")
            jump location_library
        "Meet with study group (+Appeal & Friendship)":
            call class_meeting
            jump day_hub_after_activity


label class_meeting:
    scene cg_classmate_waving_at_desk_587e2d36
    with dissolve
    "Maya met her classmates in the lounge to trade outlines before the next deadline."

    $ introduce_character(active_classmate_id)
    $ update_relationship(active_classmate_id, "friendship", 5)
    $ change_stat("appeal", 2)
    $ change_stat("communication", 2)

    "Trading perspectives turned an intimidating syllabus into a clear plan."
    return


label location_library:
    $ unlock_location("library")
    $ travel_to("library")

    scene cg_girl_reading_textbook_in_library_d2c016ba
    with dissolve

    "Sunlight filtered across the quiet reading tables on the library's second floor."

    menu:
        "Focus on coursework (+Intelligence)":
            $ study_at_library(2)
            $ change_stat("intelligence", 2)
            "Two uninterrupted chapters left her ahead of schedule."
            jump day_hub_after_activity
        "Study alongside Priya (+Appeal & Friendship)":
            $ introduce_character(active_study_partner_id)
            $ update_relationship(active_study_partner_id, "friendship", 10)
            $ change_stat("appeal", 2)
            $ study_at_library(1)
            "Priya marked tricky sections in two colors, making the review easy to follow."
            jump day_hub_after_activity
        "Read city and campus journals (+Learning)":
            $ study_at_library(1)
            $ change_stat("learning", 2)
            "Local student essays gave Maya fresh ideas for her reflection paper."
            jump day_hub_after_activity
