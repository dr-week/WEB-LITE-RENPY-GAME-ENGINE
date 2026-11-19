"""PG-13 warm playful group-hangout prompts (hand-holding, dancing, close banter) with meme easter eggs."""

import hashlib
from .desperate_story_pools import MAYA_CONTINUITY

GROUP_TOUCH_BEATS = (
    ("social_events", "group_touch_dance_floor",
     "Maya smiling warmly on a cozy rooftop lounge dance floor, one hand resting lightly on a guy's shoulder while another friend holds her free hand in a playful spin, glowing with confidence",
     "photorealistic twilight rooftop party under warm string lights and city skyline",
     "subtle 'Leonardo DiCaprio Raising Glass' guest raising a drink in the background, no text"),
    ("relationships", "group_touch_sofa_laugh",
     "Maya curled up playfully in the middle of a plush velvet lounge sofa with her arm linked through one guy's elbow and another guy resting a friendly hand near her shoulder as they all laugh",
     "photorealistic warm-lit modern loft living room with fairy lights and vinyl records",
     "subtle 'Distracted Boyfriend' friend glancing over in mock jealousy from the kitchen counter, no text"),
    ("hobbies_outdoors", "group_touch_bonfire_bench",
     "Maya sitting close between friends on a wooden park bench at dusk, holding hands across a shared warm thermos while leaning her head lightly against a companion's shoulder with a sweet smile",
     "photorealistic golden-hour city park overlook with warm lanterns and autumn trees",
     "subtle 'Doge' Shiba Inu sitting beside the bench looking on approvingly, no text"),
    ("social_events", "group_touch_karaoke_booth",
     "Maya sharing a microphone in a glowing private karaoke booth, one hand playfully tugging a friend's jacket sleeve while another buddy rests an arm along the back of the booth seat behind her",
     "photorealistic neon-lit karaoke lounge booth with warm purple ambient lighting",
     "subtle 'This Is Fine' tiny orange plush dog sitting beside a soda pitcher on the table, no text"),
    ("public_places", "group_touch_ice_rink_edge",
     "Maya laughing as she steadies herself on an outdoor ice-skating rink, gripping one guy's forearm with both hands while another guy skates beside her holding her elbow to keep her balanced",
     "photorealistic festive evening outdoor city ice rink surrounded by warm café lights",
     "subtle 'Awkward Look Monkey Puppet' plushie perched on a spectator's shoulder at the rink barrier, no text"),
)


def build_group_touch_prompts(limit: int = 5) -> list[dict]:
    """Return PG-13 warm playful group-hangout prompts with environmental meme easter eggs."""
    items = []
    for category, slug, action, env, egg in GROUP_TOUCH_BEATS[:limit]:
        pid = "grph_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: flattering cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "group-touch", "category": category, "target": slug, "prompt": prompt})
    return items


GROUP_BOLD_BEATS = (
    ("social_events", "group_bold_dance_dip",
     "Maya caught mid-laugh in a dramatic ballroom-style dance dip, one guy supporting her waist and holding her hand while two other friends cheer and clap beside the glowing dance floor",
     "photorealistic neon-lit rooftop club lounge with warm string lights and city skyline",
     "subtle 'Leonardo DiCaprio Raising Glass' friend raising a soda glass in the background, no text"),
    ("hobbies_outdoors", "group_bold_boardwalk_piggyback",
     "Maya perched high in a playful piggyback hold on a friend's back along a sunset pier, arms looped around his shoulders while another guy walks beside them holding her hand and laughing",
     "photorealistic golden-hour wooden ocean boardwalk with carnival lights and warm reflections",
     "subtle 'Doge' fluffy Shiba Inu sitting on the boardwalk planks staring up in approval, no text"),
    ("social_events", "group_bold_barstool_lean",
     "Maya perched boldly atop a tall velvet barstool leaning back slightly against a companion's arm, one hand resting on another guy's shoulder while tossing her hair with a teasing, triumphant grin",
     "photorealistic upscale downtown cocktail lounge with warm amber backlighting",
     "subtle 'Stonks' tiny green zigzag neon sign glowing behind the bar shelves, no text"),
    ("home_lodging", "group_bold_loft_lounger",
     "Maya lounging stretched diagonally across a cozy loft daybed surrounded by three laughing friends, one holding her fingers in a playful palm-reading pose while another leans over the headboard",
     "photorealistic warm-lit modern loft apartment with fairy lights and floor-to-ceiling windows",
     "subtle 'Woman Yelling at a Cat' white cat sitting upright on the coffee table beside a salad bowl, no text"),
    ("public_places", "group_bold_bowling_celebration",
     "Maya striking a bold victory lean at a retro bowling alley, caught in a joyful group hug with one guy's arm around her waist and another clasping her raised hand after a strike",
     "photorealistic retro-neon bowling alley with glowing lanes and warm overhead lights",
     "subtle 'This Is Fine' tiny orange plush dog sitting on the bowling ball return rack, no text"),
)


def build_group_bold_prompts(limit: int = 5) -> list[dict]:
    """Return PG-13 dynamic bold-pose group-hangout prompts with meme easter eggs."""
    items = []
    for category, slug, action, env, egg in GROUP_BOLD_BEATS[:limit]:
        pid = "grpb_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: dynamic cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "group-bold", "category": category, "target": slug, "prompt": prompt})
    return items
