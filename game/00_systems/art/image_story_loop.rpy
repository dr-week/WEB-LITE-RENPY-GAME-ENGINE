# Image-led story routes. Refresh the catalog after organizing new artwork.

default image_story_seen = []
default image_story_seen_categories = []

init python:
    import json

    try:
        IMAGE_STORY_EVENTS = json.loads(renpy.file("data/image_story_catalog.json").read())
    except Exception:
        IMAGE_STORY_EVENTS = {"events": []}

    IMAGE_STORY_ROUTE_LABELS = {
        "college": "Explore Campus & Study Lounges (+Intelligence)",
        "food_drink": "Visit Local Cafes & Bakeries (+Energy & Appeal)",
        "hobbies_outdoors": "Unwind Outdoors & Try a Hobby (-Stress, +Appeal)",
        "home_lodging": "Quiet Time at the Apartment (+Energy & Calm)",
        "public_places": "Explore City Landmarks & Plazas (+Confidence)",
        "relationships": "Share a Moment with Someone Close (+Friendship & Appeal)",
        "shops_markets": "Browse Neighborhood Shops & Markets (+Financial Literacy)",
        "social_events": "Attend a City Gathering (+Appeal & Communication)",
        "transport": "Take a Scenic City Transit Route (+Learning)",
        "general_scenes": "Wander the City Streets (+Confidence)",
    }

    def image_story_categories():
        return sorted({event["category"] for event in IMAGE_STORY_EVENTS["events"]
                       if any(path not in image_story_seen for path in event["images"])})

    def image_story_category_name(category):
        return IMAGE_STORY_ROUTE_LABELS.get(category, category.replace("_", " ").title())

    def image_story_personalize(text):
        name = protagonist.get("name", "Maya") if isinstance(protagonist, dict) else "Maya"
        return text.replace("Maya", name)

    def next_image_story_event(category):
        event = next((item for item in IMAGE_STORY_EVENTS["events"] if item["category"] == category
                      and any(path not in image_story_seen for path in item["images"])), None)
        if not event:
            return None
        selected = dict(event)
        selected["images"] = [path for path in event["images"] if path not in image_story_seen]
        image_story_seen.extend(selected["images"])
        return selected
