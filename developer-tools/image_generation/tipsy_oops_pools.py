"""PG-13 tipsy 'oops!' clumsy-catch group-hangout prompts with meme easter eggs."""

import hashlib
from .desperate_story_pools import MAYA_CONTINUITY

TIPSY_OOPS_BEATS = (
    ("social_events", "tipsy_oops_dance_stumble",
     "Maya with rosy flushed cheeks mid-stumble on a glowing club dance floor during a spin, laughing helplessly as two guys catch her by both arms and waist before she falls, drink glass tilted harmlessly",
     "photorealistic neon-lit rooftop lounge dance floor with warm string lights and bokeh",
     "subtle 'This Is Fine' tiny orange plush dog sitting on a DJ booth speaker, no text"),
    ("social_events", "tipsy_oops_barstool_tilt",
     "Maya tilting sideways off a tall velvet barstool with wide startled-laughing eyes and rosy cheeks, one guy catching her shoulders while another grabs her hand to steady her",
     "photorealistic cozy upscale cocktail bar with warm amber shelves and brass footrail",
     "subtle 'Surprised Pikachu' wide-eyed shock expression on a bartender in the background, no text"),
    ("home_lodging", "tipsy_oops_sofa_tumble",
     "Maya tipping backward onto a plush loft sofa mid-laugh with one sandal dangling off, two friends catching her ankles and hands in a playful tumble while she grins sheepishly",
     "photorealistic warm-lit modern loft apartment living room with fairy lights and cushions",
     "subtle 'Awkward Look Monkey Puppet' plushie peeking from behind a sofa cushion, no text"),
    ("food_drink", "tipsy_oops_karaoke_trip",
     "Maya tripping slightly over a karaoke microphone cord in a neon booth with flushed cheeks and a giggling 'oops!' expression, leaning into a guy's chest as another steadies her elbow",
     "photorealistic vibrant neon-lit private karaoke lounge booth with glowing screen glow",
     "subtle 'Leonardo DiCaprio Laughing' friend laughing with a drink in the booth corner, no text"),
    ("public_places", "tipsy_oops_alley_spin",
     "Maya stepping off a wet curb outside a late-night bistro with rosy cheeks and a dizzy giggle, one guy catching her waist from behind while another holds both her hands to keep her upright",
     "photorealistic rain-slicked downtown bistro sidewalk glowing with warm neon signs",
     "subtle 'Distracted Boyfriend' passerby turning his head in surprise down the sidewalk, no text"),
)


def build_tipsy_oops_prompts(limit: int = 5) -> list[dict]:
    """Return PG-13 tipsy clumsy-catch group prompts with environmental meme easter eggs."""
    items = []
    for category, slug, action, env, egg in TIPSY_OOPS_BEATS[:limit]:
        pid = "oops_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: dynamic cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "tipsy-oops", "category": category, "target": slug, "prompt": prompt})
    return items


SHAMELESS_POSE_BEATS = (
    ("transport", "shameless_subway_seat_spread",
     "Maya lounging unapologetically across an empty late-night subway bench with legs stretched out and one arm draped over the seatback, giving an unbothered shameless smirk while tossing her hair",
     "photorealistic tiled underground subway car under warm fluorescent lights at night",
     "subtle 'This Is Fine' tiny orange plush dog sitting on the seat beside her backpack, no text"),
    ("shops_markets", "shameless_supermarket_cart",
     "Maya perched casually on the front rim of a shiny grocery cart in a midnight supermarket aisle, holding a pint of ice cream and flashing a shameless, carefree grin toward the off-frame clerk",
     "photorealistic brightly lit 24-hour grocery store snack aisle at midnight",
     "subtle 'Stonks' tiny green zigzag arrow price-tag sticker on the shelf behind her, no text"),
    ("public_places", "shameless_fountain_ledge_pose",
     "Maya sitting boldly on the stone rim of a downtown plaza fountain with ankles crossed and chin tilted up, basking in golden-hour sunlight with an unapologetic, confident smirk",
     "photorealistic bustling city stone plaza with fountain spray and warm sunset light",
     "subtle 'Doge' Shiba Inu dog splashing a paw at the edge of the fountain behind her, no text"),
    ("college", "shameless_lectern_desk_perch",
     "Maya sitting perched right on the edge of a professor's empty lecture-hall desk after hours, swinging one sandal lazily and peeking over her sunglasses with a bold, shameless grin",
     "photorealistic empty tiered university lecture hall with warm afternoon window beams",
     "subtle 'Roll Safe' chalk doodle silhouette on the corner of the blackboard behind her, no text"),
    ("food_drink", "shameless_bakery_sample_steal",
     "Maya leaning shamelessly across a bakery display counter to snag a second free sample pastry while giving the stunned baker off-frame a sweet, unapologetic wink",
     "photorealistic cozy sunlit artisan bakery with glass pastry cases and warm wooden shelves",
     "subtle 'Surprised Pikachu' wide-eyed shocked cat figurine sitting beside the cash register, no text"),
)


def build_shameless_pose_prompts(limit: int = 5) -> list[dict]:
    """Return bold, unapologetic 'shameless' cheeky-pose prompts across random city spots."""
    items = []
    for category, slug, action, env, egg in SHAMELESS_POSE_BEATS[:limit]:
        pid = "sham_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: dynamic cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "shameless-poses", "category": category, "target": slug, "prompt": prompt})
    return items
