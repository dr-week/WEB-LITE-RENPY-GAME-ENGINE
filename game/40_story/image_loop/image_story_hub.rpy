# Maya's expanding city journal: one new art-led moment per visit.

label image_story_hub:
    "Maya opened her journal. The city was bigger than one day, so she chose where to spend the next few hours."
    $ image_story_options = [(image_story_category_name(category), category) for category in image_story_categories()[:2]]
    if not image_story_options:
        "Maya had reached the end of the moments currently in her journal. Tomorrow could bring something new."
        $ image_story_seen = []
        $ image_story_seen_categories = []
        $ image_story_path = ""
        jump day_hub
    $ image_story_options.append(("Back to Afternoon/Evening Planner", "__finish__"))
    $ image_story_category = renpy.display_menu(image_story_options)
    if image_story_category == "__finish__":
        $ image_story_path = ""
        jump day_hub
    jump image_story_play


label image_story_play:
    $ image_story_event = next_image_story_event(image_story_category)
    if image_story_event is None:
        jump image_story_hub
    if image_story_category not in image_story_seen_categories:
        $ image_story_intro = image_story_personalize(image_story_event["intro"])
        "[image_story_intro]"
        $ image_story_seen_categories.append(image_story_category)
    $ image_story_path = image_story_event["images"][0]
    $ image_story_art = fit_scene_art("images/" + image_story_path)
    scene expression image_story_art
    with dissolve
    $ image_story_narration = image_story_personalize(image_story_event["narration"])
    "[image_story_narration]"
    menu:
        "Carry the moment with poise and charm (+Appeal & Confidence)":
            $ change_stat("appeal", 3)
            $ change_stat("confidence", 3)
        "Study the detail and sharpen her mind (+Intelligence & Learning)":
            $ change_stat("intelligence", 3)
            $ change_stat("learning", 2)
        "Turn the observation into a practical side tip (+$5 & Financial Literacy)":
            $ earn_money(5, "City journal tip")
            $ change_stat("financial_literacy", 2)
            $ change_stat("energy", 3)
    $ image_story_path = ""
    jump day_hub_after_activity
