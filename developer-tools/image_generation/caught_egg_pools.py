"""Dramatic 'getting caught' secret-rendezvous story prompts with meme easter eggs."""

import hashlib
from .desperate_story_pools import MAYA_CONTINUITY

CAUGHT_EGG_BEATS = (
    ("relationships", "caught_egg_cafe_window",
     "Maya freezing mid-sip at a corner cafe table holding hands across the table with a startled date while outside the glass window someone familiar stares in shocked disbelief, a yellow potted shrub beside the window",
     "photorealistic rain-streaked glass-front corner cafe at dusk with warm interior glow",
     "subtle 'Homer Backing Into Bushes' person stepping back into a tall green hedge outside the window, no text"),
    ("home_lodging", "caught_egg_hallway_door",
     "Maya tiptoeing out of an apartment doorway holding her sandals in one hand with wide panicked eyes as a neighbor opens the opposite door in shock, a framed portrait on the wall showing a comical side-eye expression",
     "photorealistic dimly lit apartment corridor with numbered doors and warm sconce light",
     "subtle 'Side-Eyeing' framed portrait expression on the corridor wall, no text"),
    ("social_events", "caught_egg_balcony_curtain",
     "Maya pressing flat against a velvet balcony curtain at a crowded loft party, nervously sweating while glancing around the edge as her two separate dates walk toward each other across the room",
     "photorealistic glamorous evening loft party with warm chandeliers and balcony curtains",
     "subtle 'Sweating Nervous' person dabbing brow with a napkin in the background, no text"),
    ("college", "caught_egg_library_stacks",
     "Maya peeking nervously around a tall library bookshelf while whispering to a handsome stranger, unaware that Elena is standing at the end of the aisle with a tightly clenched fist at her side",
     "photorealistic quiet university library book stacks with warm overhead lights",
     "subtle 'Arthur Clenched Fist' close-up fist-at-side posture on the bystander at the aisle end, no text"),
    ("public_places", "caught_egg_lobby_elevator",
     "Maya stepping out of a boutique hotel lobby elevator arm-in-arm with a charming companion, both stopping dead in their tracks with wide-eyed shock as the lobby receptionist drops a stack of folders",
     "photorealistic upscale modern hotel lobby with marble floors and brass elevator doors",
     "subtle 'Surprised Pikachu' wide-eyed open-mouth shock reaction on a lobby bystander, no text"),
)


def build_caught_egg_prompts(limit: int = 5) -> list[dict]:
    """Return structured getting-caught story prompts with environmental meme easter eggs."""
    items = []
    for category, slug, action, env, egg in CAUGHT_EGG_BEATS[:limit]:
        pid = "caught_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: clear cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "caught-eggs", "category": category, "target": slug, "prompt": prompt})
    return items


HIDDEN_CAUGHT_BEATS = (
    ("college", "hidden_caught_greenhouse_nook",
     "Maya and her partner pulling apart in startled blush behind a tall fern rack in a quiet campus greenhouse as a groundskeeper's flashlight beam sweeps past the glass door, Maya smoothing her hair innocently",
     "photorealistic misty glass campus greenhouse at twilight filled with lush ferns and warm string lights",
     "subtle 'Crying Cat Thumbs Up' framed sticker/badge on a watering can nearby, no text"),
    ("social_events", "hidden_caught_photobooth_curtain",
     "Maya peeking out from behind a striped vintage arcade photo-booth curtain with flushed cheeks and messy hair while pulling her companion back inside as a group of friends walks past laughing",
     "photorealistic neon-lit retro arcade corner with glowing photo booth and velvet curtain",
     "subtle 'Leonardo DiCaprio Laughing' patron raising a soda cup in the background, no text"),
    ("public_places", "hidden_caught_stairwell_landing",
     "Maya pressed close to her companion in a shadowed emergency stairwell alcove, both freezing mid-embrace with wide eyes as heavy footsteps echo and the stairwell door cracks open above",
     "photorealistic quiet concrete stairwell landing lit by warm dusk window light",
     "subtle 'Awkward Look Monkey Puppet' side-glance toy keychain hanging from Maya's tote bag, no text"),
    ("hobbies_outdoors", "hidden_caught_observatory_alcove",
     "Maya and her date ducking behind a brass telescope pedestal on a quiet rooftop observatory deck, Maya biting her lip in a guilty grin as a security guard's silhouette appears at the doorway",
     "photorealistic rooftop planetarium deck at night overlooking city lights and starry sky",
     "subtle 'Shiba Doge' constellation-shaped neon wall lamp glowing softly in the alcove, no text"),
    ("shops_markets", "hidden_caught_bookstore_loft",
     "Maya sitting on a cozy tucked-away mezzanine ladder landing in an indie bookstore, quickly straightening her dress and grabbing a random book upside-down as the shopkeeper calls up the stairs",
     "photorealistic warm wood-paneled indie bookstore mezzanine with fairy lights and tall shelves",
     "subtle 'Conceited Reaction' cat statue glaring disapprovingly from the top bookshelf, no text"),
)


def build_hidden_caught_prompts(limit: int = 5) -> list[dict]:
    """Return PG-13 romantic hidden-place 'getting caught' prompts with meme easter eggs."""
    items = []
    for category, slug, action, env, egg in HIDDEN_CAUGHT_BEATS[:limit]:
        pid = "hid_" + hashlib.sha1(slug.encode("utf-8")).hexdigest()[:10]
        prompt = (
            f"[SCENE: {action}] [ENV: {env}] [EASTER_EGG: {egg}] "
            f"[FRAME: clear cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({"id": pid, "kind": "hidden-caught", "category": category, "target": slug, "prompt": prompt})
    return items
