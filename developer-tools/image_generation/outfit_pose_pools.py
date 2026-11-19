"""PG-13 bold/cheeky outfit-change pose prompts across random city spots with meme easter eggs."""

import hashlib

MAYA_FACE_STYLE = (
    "East Asian young woman Maya with soft round-oval face, gentle rounded cheeks, "
    "expressive almond eyes, and blonde-dipped dark hair. "
    "2D anime-influenced cell-shaded character composited over photorealistic environment, "
    "matched lighting, solid ground contact and accurate anatomy, no text or watermarks"
)

OUTFIT_POSE_BEATS = (
    ("social_events", "outfit_rooftop_cocktail_slip",
     "Maya in a sleek dark-emerald satin cocktail mini-dress and heeled sandals, leaning boldly against a glowing rooftop glass railing while tossing her hair back with a triumphant, shameless smirk",
     "photorealistic glittering city rooftop lounge at night with warm amber bar lights",
     "subtle 'Leonardo DiCaprio Raising Glass' patron raising a drink in admiration behind her, no text"),
    ("hobbies_outdoors", "outfit_tennis_court_sporty",
     "Maya in a crisp navy pleated tennis skirt, fitted white cropped tank, and sneakers, perched shamelessly on the umpire's high chair on a sunlit park court twirling a racket with a playful wink",
     "photorealistic sunlit urban park tennis court surrounded by green trees and golden-hour glow",
     "subtle 'Doge' fluffy Shiba Inu chasing a stray tennis ball near the baseline, no text"),
    ("shops_markets", "outfit_night_market_offshoulder",
     "Maya in an off-shoulder burgundy knit top, high-waisted denim mini-skirt, and ankle boots, striking a confident model-like hip-pop pose between glowing night-market lanterns",
     "photorealistic bustling outdoor night market alley with warm paper lanterns and food stalls",
     "subtle 'Distracted Boyfriend' shopper turning his head in surprise in the blurred crowd, no text"),
    ("public_places", "outfit_gallery_oversized_blazer",
     "Maya in an oversized charcoal tailored blazer worn over a sleek black bralette-style crop top and mini-shorts with loafers, leaning back against a white gallery pedestal with a sly, unapologetic grin",
     "photorealistic modern downtown loft art gallery with warm track spotlights and concrete floors",
     "subtle 'Stonks' minimalist upward green zigzag arrow canvas hanging on the far wall, no text"),
    ("home_lodging", "outfit_balcony_silk_lounge",
     "Maya in a breezy lavender silk cami-and-shorts lounge set with messy morning hair, stretching her arms overhead on a sunlit apartment balcony while peeking cheekily down at the street below",
     "photorealistic sunlit city apartment balcony overlooking morning rooftops and coffee shops",
     "subtle 'Kermit Sipping Tea' small green frog figurine sitting beside a coffee mug on the balcony table, no text"),
)


def build_outfit_pose_prompts(limit: int = 5) -> list[dict]:
    """Return bold outfit-change pose prompts with environmental meme easter eggs."""
    items = []
    for category, slug, action, env, egg in OUTFIT_POSE_BEATS[:limit]:
        pid = "outf_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: flattering cinematic medium-wide shot] "
            f"[OUTFIT_AND_STYLE: {MAYA_FACE_STYLE}] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "outfit-poses", "category": category, "target": slug, "prompt": prompt})
    return items


NAVY_MOD_BEATS = (
    ("social_events", "navy_mod_mesh_shoulder_slit",
     "Maya in her signature dark navy-blue t-shirt dress customized with sheer black mesh shoulder-and-sleeve panels and a bold high side-slit hem, leaning back against a glowing rooftop bar rail pulling the collar playfully off one shoulder with a shameless smirk",
     "photorealistic glittering city rooftop lounge at night with warm amber bar lights",
     "subtle 'Leonardo DiCaprio Raising Glass' patron raising a drink in the background, no text"),
    ("public_places", "navy_mod_knotted_hem_cutout",
     "Maya in her signature dark navy-blue t-shirt dress modified with a knotted side-hem gather and geometric shoulder cutouts, perched boldly on a plaza fountain ledge pulling lightly at the hem with a teasing wink",
     "photorealistic sunlit downtown stone plaza with fountain spray and golden-hour glow",
     "subtle 'Doge' fluffy Shiba Inu splashing a paw at the fountain edge behind her, no text"),
    ("shops_markets", "navy_mod_ladder_sleeve_distressed",
     "Maya in her signature dark navy-blue t-shirt dress altered with edgy ladder-cutout sleeves, distressed raw hem, and one-shoulder drape, striking a bold hip-pop pose between glowing night-market stalls",
     "photorealistic bustling outdoor night market alley with warm paper lanterns and food stalls",
     "subtle 'Distracted Boyfriend' shopper turning his head in surprise in the blurred crowd, no text"),
    ("transport", "navy_mod_back_strap_mesh_waist",
     "Maya in her signature dark navy-blue t-shirt dress restyled with sheer mesh side-waist panels and an open crisscross strap back, glancing back over her shoulder at a subway platform pillar with an unapologetic grin",
     "photorealistic tiled underground metro station platform under cool neon and fluorescent strips",
     "subtle 'Stonks' tiny green zigzag arrow sticker on a metro map behind her, no text"),
    ("hobbies_outdoors", "navy_mod_asymmetric_laceup_side",
     "Maya in her signature dark navy-blue t-shirt dress customized with an asymmetric off-shoulder cut and lace-up eyelet side openings over dark shorts, lounging boldly across a neon arcade bench while tugging the sleeve",
     "photorealistic vibrant retro-neon downtown arcade aisle with glowing cabinet reflections",
     "subtle 'This Is Fine' tiny orange plush dog sitting on a nearby arcade stool, no text"),
)


def build_navy_mod_prompts(limit: int = 5) -> list[dict]:
    """Return bold streetwear-modified dark navy-blue t-shirt dress prompts with meme easter eggs."""
    items = []
    for category, slug, action, env, egg in NAVY_MOD_BEATS[:limit]:
        pid = "nmod_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: flattering cinematic medium-wide shot] "
            f"[OUTFIT_AND_STYLE: {MAYA_FACE_STYLE}, wearing her modified dark navy-blue t-shirt short dress and dark slide sandals] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "navy-mods", "category": category, "target": slug, "prompt": prompt})
    return items
