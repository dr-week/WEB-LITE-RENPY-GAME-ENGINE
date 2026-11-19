"""Interactive story prompts with subtle environmental easter eggs and meme compositions."""

import hashlib
from .desperate_story_pools import MAYA_CONTINUITY

EASTER_EGG_BEATS = (
    ("food_drink", "egg_this_is_fine_cafe",
     "Maya calmly sipping espresso at a cafe booth with an unbothered angel-smile while behind her the espresso machine steams wildly and a tiny orange plush dog sits on a counter stool beside a coffee mug",
     "photorealistic bustling coffee shop interior with warm lighting and steam clouds",
     "subtle 'This Is Fine' calm-in-chaos background gag with a tiny orange plush dog and mug, no text"),
    ("college", "egg_distracted_walk_quad",
     "Maya strolling across the sunny campus quad tossing her hair with a sly smirk while in the blurred background a student walking with his girlfriend turns his head dramatically to stare back",
     "photorealistic sunlit university brick quad with students and autumn trees",
     "subtle background-only 'Distracted Boyfriend' glance composition with original students, no text"),
    ("shops_markets", "egg_stonks_thrift_mirror",
     "Maya grinning mischievously as she holds up a $5 vintage blazer in a thrift store mirror while a mannequin in a crisp suit beside a rising green zigzag arrow neon sign stands in the corner",
     "photorealistic eclectic vintage thrift shop with clothing racks and neon decor",
     "subtle background-only 'Stonks' upward green zigzag neon arrow and suited mannequin, no text"),
    ("hobbies_outdoors", "egg_doge_park_bench",
     "Maya sketching her next city scheme on a park bench with a playful side-eye while a fluffy golden Shiba Inu sitting upright on the grass nearby gives an exaggerated wide-eyed approving stare",
     "photorealistic city park walkway at golden hour with trees and dappled sunlight",
     "subtle 'Doge' Shiba Inu cameo giving an exaggerated approving side-eye on the grass, no text"),
    ("home_lodging", "egg_woman_yelling_cat_kitchen",
     "Maya leaning on her apartment kitchen counter with a dramatic pointing gesture toward a spotless white cat sitting upright on a barstool behind a tiny salad plate",
     "photorealistic cozy apartment kitchen counter with warm pendant lights",
     "subtle 'Woman Yelling at a Cat' visual homage with a white cat at a salad plate, no text"),
)


def build_easter_egg_prompts(limit: int = 5) -> list[dict]:
    """Return structured interactive-story prompts with environmental meme easter eggs."""
    items = []
    for category, slug, action, env, egg in EASTER_EGG_BEATS[:limit]:
        pid = "egg_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: clear cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "easter-eggs", "category": category, "target": slug, "prompt": prompt})
    return items


HAZY_EGG_BEATS = (
    ("social_events", "hazy_egg_rooftop_galaxy",
     "Maya lounging back on a cushioned rooftop sofa under purple string lights, giggling dreamily at a bowl of snacks with relaxed half-lidded eyes while a glowing neon prism projection shimmers on the brick wall behind her",
     "photorealistic hazy twilight city rooftop lounge with warm string lights and neon glow",
     "subtle 'Galaxy Brain' glowing prism light projection on the brick wall behind her, no text"),
    ("home_lodging", "hazy_egg_fire_escape_tea",
     "Maya sitting cross-legged on her apartment fire escape at midnight in a hazy dreamy mood, sipping from a warm mug with a knowing smirk while a small green frog plush sits on the railing beside a teacup",
     "photorealistic neon-lit city fire escape overlooking glowing midnight streets",
     "subtle 'Kermit Sipping Tea' frog plush with teacup on the railing, no text"),
    ("food_drink", "hazy_egg_midnight_diner_spiderman",
     "Maya perched in a retro midnight diner booth grinning lazily at a giant plate of fries while across the diner two identically dressed strangers in matching jackets point at each other in mock shock",
     "photorealistic neon-lit 24-hour retro diner with vinyl booths and glowing jukebox",
     "subtle background-only 'Spider-Man Pointing' twin-jacket strangers gag, no text"),
    ("hobbies_outdoors", "hazy_egg_alley_rollsafe",
     "Maya leaning casually against a neon-lit alley wall in a hazy late-night chill mood, tapping her temple with one finger and a sly knowing smirk while a streetlamp casts dreamy mist around her",
     "photorealistic misty downtown brick alley glowing with magenta and cyan neon signs",
     "subtle 'Roll Safe' temple-tap pose and knowing smirk, no text"),
    ("relationships", "hazy_egg_loft_corkboard",
     "Maya laughing on a cozy loft beanbag chair at 2 AM surrounded by snack bags and vinyl records while behind her a friend points excitedly at a corkboard covered in colorful yarn-connected Polaroids",
     "photorealistic hazy warm-lit loft living room with fairy lights, vinyl records, and corkboard",
     "subtle 'Pepe Silvia' red-yarn Polaroid corkboard gag in the background, no text"),
)


def build_hazy_egg_prompts(limit: int = 5) -> list[dict]:
    """Return structured late-night hazy/chill story prompts with meme easter eggs."""
    items = []
    for category, slug, action, env, egg in HAZY_EGG_BEATS[:limit]:
        pid = "hazy_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: clear cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "hazy-eggs", "category": category, "target": slug, "prompt": prompt})
    return items
