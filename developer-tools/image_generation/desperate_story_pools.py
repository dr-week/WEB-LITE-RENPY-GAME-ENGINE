"""Grounded 'desperate sides' story prompt pool for Maya with strict character continuity."""

import hashlib

MAYA_CONTINUITY = (
    "East Asian young woman Maya with soft round-oval face, blonde-dipped dark hair, "
    "wearing her exact oversized dark navy-blue t-shirt short dress and dark slide sandals. "
    "2D anime-influenced cell-shaded character composited over photorealistic environment, "
    "matched lighting, solid ground contact and accurate anatomy, no text or watermarks"
)

DESPERATE_BEATS = (
    ("home_lodging", "rent_notice_kitchen",
     "standing barefoot-in-sandals in her dim apartment kitchen at night, holding a crumpled rent envelope with tense shoulders and worried eyes, biting her lip, gaze off-camera",
     "photorealistic cramped apartment kitchen with dim refrigerator light and shadows"),
    ("shops_markets", "counting_last_coins",
     "hunched slightly at a late-night corner mart counter, emptying loose coins from her small wallet onto the counter with an anxious, pleading half-smile toward the off-frame clerk",
     "photorealistic fluorescent-lit convenience store counter at midnight"),
    ("transport", "rain_soaked_dead_phone",
     "sitting slumped on a cold metal bus shelter bench in heavy pouring rain, hugging her knees while staring down at a dark dead phone screen, hair damp, exhausted expression",
     "photorealistic rain-lashed city bus stop reflecting blurred neon taillights"),
    ("food_drink", "begging_extra_shift",
     "leaning across the Daily Grind Cafe back counter with clasped hands and desperate, hopeful eyes, pleading with the off-frame manager for an extra closing shift",
     "photorealistic empty closing-time cafe counter with stacked chairs and warm overhead bulbs"),
    ("college", "cramming_3am_library",
     "slumped forward over an oak library table at 3 AM surrounded by open textbooks, rubbing her eyes with one hand while clutching a cold coffee cup, exhausted and stressed",
     "photorealistic quiet university library desk lit by a single warm brass lamp"),
    ("home_lodging", "empty_fridge_dusk",
     "crouching slightly before an almost-empty open refrigerator in her dim studio apartment, bathed in cool fridge light with a hollow, stressed expression",
     "photorealistic small studio apartment kitchen at dusk with cool fridge glow"),
    ("shops_markets", "thrift_counter_trade",
     "standing nervously at a vintage pawn/thrift shop glass counter, sliding her watch across the counter with conflicted, desperate eyes while negotiating cash, gaze off-camera",
     "photorealistic cluttered vintage thrift shop counter with warm hanging bulbs"),
    ("college", "overdue_tuition_stairwell",
     "sitting on the cold concrete steps of a quiet college stairwell, head tilted back against the wall with one hand over her forehead after reading a harsh alert on her phone",
     "photorealistic empty university concrete stairwell with harsh afternoon window light"),
    ("transport", "missed_last_train",
     "sitting alone on a tiled subway platform bench late at night, elbows on knees and chin in hands, staring down the empty tracks with quiet desperation",
     "photorealistic empty underground metro station platform under cool fluorescent strips"),
    ("public_places", "alley_exhaustion_rain",
     "leaning her back heavily against a damp brick alley wall under a flickering streetlamp, catching her breath with shadowed, vulnerable eyes looking down the wet street",
     "photorealistic rain-slicked downtown side alley at night with warm streetlamp reflections"),
)


def build_desperate_prompts(limit: int = 10) -> list[dict]:
    """Return structured desperate-tone story prompts with deterministic IDs."""
    items = []
    for category, slug, action, env in DESPERATE_BEATS[:limit]:
        pid = "desp_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [FRAME: intimate cinematic medium shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: extra limbs, distorted hands, floating feet, text, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "desperate", "category": category, "target": slug, "prompt": prompt})
    return items
