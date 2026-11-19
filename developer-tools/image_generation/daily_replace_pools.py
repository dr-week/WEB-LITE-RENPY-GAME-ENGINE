"""Daily chapter (Days 2-6) replacement prompts with environmental meme easter eggs."""

import hashlib
from .desperate_story_pools import MAYA_CONTINUITY

DAILY_REPLACE_BEATS = (
    ("college", "day02_class_notes_egg",
     "Maya and her classmate Elena sitting side-by-side in a tiered university lecture hall, laughing quietly as they trade shorthand notebook pages across the wooden desk",
     "photorealistic sunlit university lecture hall with warm overhead lights and students",
     "subtle 'Distracted Boyfriend' student turning to glance back in the blurred upper row, no text"),
    ("food_drink", "day03_cafe_marcus_egg",
     "Maya pausing outside The Daily Grind Cafe window with a thoughtful smirk while Marcus stacks espresso cups behind the glass counter and waves her in for a part-time shift",
     "photorealistic warm-lit corner coffee shop storefront and espresso bar at midweek morning",
     "subtle 'This Is Fine' tiny orange plush dog sitting beside a steaming mug on the counter, no text"),
    ("college", "day04_library_priya_egg",
     "Maya and her study partner Priya leaning over open textbooks and laptops at an oak university library table, sharing a focused yet sly grin over their research notes",
     "photorealistic quiet university library study room with warm brass desk lamps and bookshelves",
     "subtle 'Woman Yelling at a Cat' framed art postcard taped inside a book cover nearby, no text"),
    ("college", "day05_campus_deadline_egg",
     "Maya walking briskly through the stone campus archway on Friday morning clutching her finished reflection paper folder with a triumphant, relieved smile",
     "photorealistic crisp Friday morning college campus entrance with brick paths and autumn trees",
     "subtle 'Success Kid' toddler-pose bronze garden gnome statue tucked beside the campus hedge, no text"),
    ("hobbies_outdoors", "day06_weekend_park_egg",
     "Maya and Elena relaxing on a sunny weekend park bench with iced coffees, laughing together after surviving their first week in the city",
     "photorealistic golden Saturday morning city park path with trees, benches, and warm sunlight",
     "subtle 'Doge' fluffy Shiba Inu sitting upright on the grass nearby with an approving side-eye, no text"),
)


def build_daily_replace_prompts(limit: int = 5) -> list[dict]:
    """Return structured Days 2-6 replacement prompts with meme easter eggs."""
    items = []
    for category, slug, action, env, egg in DAILY_REPLACE_BEATS[:limit]:
        pid = "day_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: clear cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "daily-replace", "category": category, "target": slug, "prompt": prompt})
    return items


START_REPLACE_BEATS = (
    ("home_lodging", "start_alarm_overslept_egg",
     "Maya blinking awake on the edge of her messy studio bed at 7:45 AM, glaring sideways at a silent phone alarm on the nightstand with ruffled hair",
     "photorealistic sunlit small apartment bedroom at early morning with warm window blinds",
     "subtle 'Awkward Look Monkey Puppet' plushie sitting on the nightstand beside the silent phone, no text"),
    ("home_lodging", "start_bank_balance_egg",
     "Maya leaning against her tiny kitchen counter holding a mug of coffee and squinting at her phone banking screen with a wry, calculating half-smile",
     "photorealistic lived-in apartment kitchen at morning with cracked mirror and city window",
     "subtle 'Stonks' tiny green zigzag arrow fridge magnet on the refrigerator behind her, no text"),
    ("college", "start_classroom_entry_egg",
     "Maya stepping smoothly through a wooden university lecture hall doorway just before class starts, scanning the room for the best seat with an innocent angel-face",
     "photorealistic sunlit college lecture hall entrance with tiered desks and students",
     "subtle 'Side-Eyeing' student glancing over a laptop lid near the front row, no text"),
    ("college", "start_elena_wave_egg",
     "Maya's friendly classmate Elena waving warmly from a middle-row lecture desk with a spare seat saved beside her while Maya walks up the aisle",
     "photorealistic warm-lit university lecture hall middle row with wooden desks and notebooks",
     "subtle 'Leonardo DiCaprio Raising Cup' student raising a travel coffee mug in the background row, no text"),
    ("home_lodging", "start_menu_hero_egg",
     "Maya standing confidently by her apartment window overlooking the glittering city skyline at golden hour, glancing back over her shoulder with a charming, mischievous smirk",
     "photorealistic warm-lit high-rise studio apartment window overlooking downtown city skyline at sunset",
     "subtle 'Kermit Sipping Tea' small green frog figurine sitting on the windowsill beside a teacup, no text"),
)


def build_start_replace_prompts(limit: int = 5) -> list[dict]:
    """Return replacement prompts for older start-of-story and menu hero images."""
    items = []
    for category, slug, action, env, egg in START_REPLACE_BEATS[:limit]:
        pid = "start_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: clear cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "start-flagged", "category": category, "target": slug, "prompt": prompt})
    return items
