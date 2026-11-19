"""Charismatic, alluring pose & charm story prompts with environmental meme easter eggs."""

import hashlib
from .desperate_story_pools import MAYA_CONTINUITY

ALLURE_POSE_BEATS = (
    ("social_events", "allure_rooftop_lounge_pose",
     "Maya leaning gracefully against a glowing rooftop bar railing in a bold, confident pose, tilting her chin down slightly with a captivating half-smile and tossing her hair back over one shoulder while catching an admirer's eye off-frame",
     "photorealistic glittering city rooftop lounge at twilight with warm amber bar lights",
     "subtle 'Distracted Boyfriend' bystander turning his head in admiration in the blurred background, no text"),
    ("social_events", "allure_jazz_booth_charm",
     "Maya seated at a curved crimson velvet jazz-club booth, leaning forward slightly with elbows resting softly on the table and a playful, magnetic smirk over a sparkling mocktail",
     "photorealistic dimly lit upscale jazz lounge with warm brass lamps and velvet booths",
     "subtle 'Leonardo DiCaprio Raising Glass' patron raising a glass in approval at a distant booth, no text"),
    ("hobbies_outdoors", "allure_art_gallery_glance",
     "Maya standing in a sleek modern loft art gallery in a poised three-quarter stance, glancing back over her shoulder with bright expressive eyes and a teasing, confident smile",
     "photorealistic concrete-walled downtown art gallery with warm spotlights and abstract paintings",
     "subtle 'Stonks' minimalist geometric upward-arrow painting hanging on the far gallery wall, no text"),
    ("food_drink", "allure_cafe_counter_spark",
     "Maya perched lightly on a high cafe barstool with one ankle crossed over the other, resting her cheek in one palm with a warm, alluring gaze toward someone off-frame",
     "photorealistic golden-hour corner bistro window with warm reflections and espresso bar",
     "subtle 'Doge' Shiba Inu dog sitting outside the cafe glass window staring in with wide-eyed approval, no text"),
    ("public_places", "allure_neon_arcade_win",
     "Maya leaning casually against a glowing neon arcade cabinet, winking playfully with one hand on her hip after effortlessly beating a high score while a small crowd watches",
     "photorealistic vibrant retro-neon downtown arcade aisle with glowing cabinet reflections",
     "subtle 'Roll Safe' neon silhouette sticker on the side of the arcade machine, no text"),
)


def build_allure_pose_prompts(limit: int = 5) -> list[dict]:
    """Return structured charismatic-pose prompts with environmental meme easter eggs."""
    items = []
    for category, slug, action, env, egg in ALLURE_POSE_BEATS[:limit]:
        pid = "allure_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: flattering cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "allure-poses", "category": category, "target": slug, "prompt": prompt})
    return items


GROUP_TEASE_BEATS = (
    ("social_events", "group_tease_pool_table",
     "Maya leaning gracefully over a green-felt billiard table lining up a trick shot with a playful smirk while three young men around the table watch in amused disbelief",
     "photorealistic warm-lit downtown lounge billiard room with brass pendant lamps and wooden paneling",
     "subtle 'Leonardo DiCaprio Raising Glass' guy raising a soda glass in the background, no text"),
    ("college", "group_tease_quad_table",
     "Maya perched on the edge of a sunny campus courtyard picnic table tossing her hair with an innocent 'who, me?' wink as a small group of male classmates lean in laughing at her witty remark",
     "photorealistic sunlit brick university courtyard with oak trees and picnic tables",
     "subtle 'Distracted Boyfriend' bystander turning his head in surprise on the path behind them, no text"),
    ("social_events", "group_tease_rooftop_circle",
     "Maya standing at the center of a lively rooftop terrace circle holding a sparkling drink, smiling teasingly over her shoulder as three guys compete to tell the best story",
     "photorealistic twilight city rooftop terrace with warm string lights and skyline view",
     "subtle 'This Is Fine' tiny orange plush dog sitting on a patio side table beside a mug, no text"),
    ("food_drink", "group_tease_diner_booth",
     "Maya sitting in a retro neon diner booth resting her chin in her palm with a sly, teasing smile while a trio of friends across the table try to guess her next move over milkshakes",
     "photorealistic glowing 24-hour retro diner with vinyl booths and warm neon window reflections",
     "subtle 'Spider-Man Pointing' two guys in matching jackets pointing at each other in mock accusation, no text"),
    ("public_places", "group_tease_arcade_crowd",
     "Maya holding a winning arcade prize ticket up with a triumphant, teasing grin while a group of young men behind her look stunned at her high score on the racing cabinet",
     "photorealistic vibrant downtown neon arcade with glowing cabinets and warm reflections",
     "subtle 'Doge' Shiba Inu plushie sitting inside a nearby claw-machine glass case staring out, no text"),
)


def build_group_tease_prompts(limit: int = 5) -> list[dict]:
    """Return PG-13 playful group-charm prompts with environmental meme easter eggs."""
    items = []
    for category, slug, action, env, egg in GROUP_TEASE_BEATS[:limit]:
        pid = "grpt_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: flattering cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "group-tease", "category": category, "target": slug, "prompt": prompt})
    return items
