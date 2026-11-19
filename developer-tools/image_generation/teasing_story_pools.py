"""Playful, teasing, and slyly charming story beats for Maya with strict continuity."""

import hashlib
from .desperate_story_pools import MAYA_CONTINUITY

TEASING_BEATS = (
    ("food_drink", "teasing_barista_wink",
     "leaning playfully across the espresso bar with chin in one hand, giving the off-frame barista a sly, teasing half-wink and innocent smirk over a free pastry",
     "photorealistic warm-lit cafe counter with morning sunlight and espresso steam"),
    ("social_events", "teasing_vip_bouncer",
     "tilting her head with wide innocent eyes and a mischievous, teasing smile while holding up a borrowed VIP wristband near a velvet-rope doorway, gaze off-camera",
     "photorealistic neon-lit rooftop lounge entrance with velvet ropes and warm sconces"),
    ("college", "teasing_library_note",
     "peeking sideways over an open textbook at a study partner off-frame, biting the end of her pen with a playful, teasing grin while sliding a folded note across the table",
     "photorealistic sunlit university library oak table with stacked books"),
    ("shops_markets", "teasing_street_vendor_bargain",
     "resting one hand on her hip and tilting her sunglasses down slightly with a teasing, persuasive smile while haggling over a vintage jacket at a street stall",
     "photorealistic bustling outdoor weekend market with warm string lights"),
    ("home_lodging", "teasing_balcony_glance",
     "glancing back over her shoulder from a sunlit apartment balcony doorway, tossing her hair with a playful, teasing smirk toward someone off-frame",
     "photorealistic cozy city apartment balcony overlooking golden-hour rooftops"),
)


def build_teasing_prompts(limit: int = 5) -> list[dict]:
    """Return structured teasing-tone story prompts with deterministic IDs."""
    items = []
    for category, slug, action, env in TEASING_BEATS[:limit]:
        pid = "teas_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [FRAME: intimate cinematic medium shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: extra limbs, distorted hands, floating feet, text, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "teasing", "category": category, "target": slug, "prompt": prompt})
    return items


CHEEKY_START_BEATS = (
    ("home_lodging", "cheeky_start_mirror_smirk",
     "Maya standing in front of her apartment bathroom mirror adjusting the hem of her oversized dark navy-blue t-shirt dress with a playful, mischievous wink at her reflection before heading out",
     "photorealistic sunlit studio apartment bathroom and doorway at early morning",
     "subtle 'Roll Safe' tiny framed pose sketch hanging beside the mirror, no text"),
    ("food_drink", "cheeky_start_cafe_freebie",
     "Maya leaning playfully over a corner cafe counter batting her lashes innocently at the off-frame barista while sliding an extra free croissant into her paper bag",
     "photorealistic warm-lit morning coffee shop counter with pastry display and steam",
     "subtle 'This Is Fine' tiny orange plush dog sitting beside the tip jar, no text"),
    ("public_places", "cheeky_start_spare_keycard",
     "Maya slipping a spare VIP lobby keycard into her pocket behind her back while flashing a sweet, innocent 'who, me?' smile toward the off-frame front-desk clerk",
     "photorealistic sunlit modern apartment lobby desk with marble counter and plants",
     "subtle 'Stonks' tiny green zigzag neon arrow sticker on the lobby monitor back, no text"),
    ("college", "cheeky_start_campus_shortcut",
     "Maya hopping lightly past a campus courtyard gate with a borrowed guest lanyard, looking back over her shoulder with a teasing smirk as a security guard checks his clipboard",
     "photorealistic bustling university stone gate and courtyard at morning rush",
     "subtle 'Distracted Boyfriend' student glancing back in surprise on the sidewalk behind her, no text"),
    ("college", "cheeky_start_hallway_tease",
     "Maya leaning casually against a college hallway locker, whispering a playful dare to a blushing classmate while twirling a pen between her fingers",
     "photorealistic sunlit college corridor with metal lockers and bulletin boards",
     "subtle 'Doge' Shiba Inu mascot poster pinned to the hallway bulletin board, no text"),
)


def build_cheeky_start_prompts(limit: int = 5) -> list[dict]:
    """Return mischievous, teasing start-of-story replacement prompts with meme easter eggs."""
    items = []
    for category, slug, action, env, egg in CHEEKY_START_BEATS[:limit]:
        pid = "cheeky_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: clear cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "cheeky-start", "category": category, "target": slug, "prompt": prompt})
    return items
