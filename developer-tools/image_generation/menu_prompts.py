"""Combinatorial prompt generator with Flow manifest tracking."""

import hashlib
import json
import random
from pathlib import Path
from .menu_prompt_pools import (
    BACKDROPS, CAMERA_ANGLES, DRESS_VARIATIONS, EGGS, LIGHTING, POSES, RIGHT_BLURS, SETUPS,
)
from .dance_competition_pools import DANCE_COMPETITION_ARC
from .dance_performance_pools import DANCE_PERFORMANCE_ARC
from .editorial_model_pools import EDITORIAL_YOGA_ARC
from .noir_prompt_pools import DIVE_NOIR_ARC
from .romance_prompt_pools import JUNGLE_ROMANCE_ARC
from .yoga_prompt_pools import YOGA_STUDIO_ARC
from .story_prompt_pools import (BODY_CONFIDENCE_ARC, STORY_BEATS, STORY_CAMERAS, STORY_LOCATIONS, TRAPPED_ARC, TRAPPED_NIGHTOUT_ARC)
STORY_THEMES = {
    "body_worry": BODY_CONFIDENCE_ARC, "trapped": TRAPPED_ARC,
    "trapped_nightout": TRAPPED_NIGHTOUT_ARC, "dive_noir": DIVE_NOIR_ARC,
    "jungle_romance": JUNGLE_ROMANCE_ARC, "yoga": YOGA_STUDIO_ARC,
    "editorial_yoga": EDITORIAL_YOGA_ARC, "dance_hustle": DANCE_PERFORMANCE_ARC,
    "dance_competition": DANCE_COMPETITION_ARC
}

HISTORY_FILE = Path(__file__).with_name(".last_menu_prompts.json")
MANIFEST_FILE = Path(__file__).with_name(".prompt_manifest.json")


def _load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _cycled(items: tuple, count: int, rng: random.Random) -> list:
    pool = list(items)
    rng.shuffle(pool)
    while len(pool) < count:
        extra = list(items)
        rng.shuffle(extra)
        pool.extend(extra)
    return pool[:count]


def build_prompt(title: str, place: str, light: str, angle: str, pose: str,
                 dress: str, right_blur: str, egg: str, asset_id: str, menu_mode: bool) -> str:
    mode_tag = "Bold high-concept menu art" if menu_mode else "LOLA story scene"
    frame = (f"[FRAME: {{Sharp focal subject Maya anchored on the LEFT}}; ({right_blur})]"
             if menu_mode else "[FRAME: {Full-bleed cinematic 16:9 story composition with balanced depth}]")
    avoid = ("[AVOID: westernized sharp jawline, angular gaunt face, different face, extra legs, extra arms, extra fingers, distorted hands, floating or levitating subjects, "
             "disconnected shadows, unnatural limb bends, text, logos, watermarks, laptops, holograms, UI buttons, sharp clutter on right]"
             if menu_mode else
             "[AVOID: looking at camera, direct eye contact with viewer, fourth-wall stare, westernized sharp jawline, angular gaunt face, different face, "
             "extra legs, extra arms, extra fingers, distorted hands, floating or levitating subjects, disconnected shadows, unnatural limb bends, text, logos, watermarks, laptops, holograms, UI buttons]")
    return "\n".join([
        f"[ASSET_ID: {asset_id}]",
        f"[SCENE: {mode_tag}, 16:9 widescreen — {title}]",
        f"[CAMERA: {{{angle}}}]",
        f"[BEAT: {{Maya {pose}}}]",
        "[CAST: Maya (exact reference: East Asian young woman with a soft round-oval face, gentle rounded cheeks, expressive almond eyes, long straight dark hair with blonde-dipped ombre ends, innocent sweet angel-face contrast with bold, playful con-artist moves)]",
        "[REFERENCES: {Strictly match the given reference images for Maya's exact East Asian round-oval face, facial proportions, cel-shaded 2D rendering, blonde-dipped dark hair, and dark navy-blue t-shirt short dress}]",
        f"[CONTINUITY: {{{dress}}}; (no laptop, no hologram)]",
        f"[PLACE: {{{place}}}]",
        "[PHYSICS: {natural gravity, firm physical contact between Maya's sandals/feet/body and solid surface, accurate two-leg and two-arm human anatomy}]",
        frame,
        f"[STYLE: {{Hybrid composite art: 2D animated cel-shaded Maya character integrated seamlessly into a fully photorealistic real-world environment background with matched shadows and {light}}}]",
        f"[STARTER_EGG: {{Subtle background-only {egg}}}]",
        avoid,
    ])


def generate_menu_prompts(count: int = 5, seed: int | None = None,
                          menu_mode: bool = True, theme: str = "") -> list[dict]:
    rng = random.Random(seed)
    recent = set(_load_json(HISTORY_FILE, [])) if seed is None else set()
    manifest = _load_json(MANIFEST_FILE, []) if seed is None else []
    angles = _cycled(CAMERA_ANGLES if menu_mode else STORY_CAMERAS, count, rng)
    dresses = _cycled(DRESS_VARIATIONS, count, rng)
    lights, blurs, eggs = _cycled(LIGHTING, count, rng), _cycled(RIGHT_BLURS, count, rng), _cycled(EGGS, count, rng)
    arc = _cycled(STORY_THEMES[theme], count, rng) if (not menu_mode and theme in STORY_THEMES) else None
    poses = [a[3] for a in arc] if arc else _cycled(POSES if menu_mode else STORY_BEATS, count, rng)
    setups = ([(a[0], a[1], a[2]) for a in arc] if arc else
              (_cycled(SETUPS, len(SETUPS), rng) if menu_mode else _cycled(STORY_LOCATIONS, len(STORY_LOCATIONS), rng)))
    backdrops = _cycled(BACKDROPS, count, rng)
    results = []
    for i in range(count):
        if menu_mode:
            cat, slug_base = "menu", setups[i % len(setups)].lower().replace(" ", "_")[:24]
            title, place = setups[i % len(setups)].title(), f"{setups[i % len(setups)]} overlooking {backdrops[i]}"
        else:
            cat, slug_base, place = setups[i % len(setups)]
            title = slug_base.replace("_", " ").title()
        tag = hashlib.sha1(f"{slug_base}|{angles[i]}|{poses[i]}".encode()).hexdigest()[:6]
        asset_id = f"{cat}_{slug_base}_{tag}"
        prompt = build_prompt(title, place, lights[i], angles[i], poses[i], dresses[i], blurs[i], eggs[i], asset_id, menu_mode)
        clean_place = place.replace("photorealistic ", "")
        caption = f"At {clean_place}, Maya was {poses[i]}."
        item = {"asset_id": asset_id, "category": cat, "suggested_filename": f"{asset_id}.png",
                "title": title, "caption": caption, "prompt": prompt}
        results.append(item)
        recent.add(f"{slug_base}|{angles[i]}")
        manifest.append({k: item[k] for k in ("asset_id", "category", "suggested_filename", "title", "caption")})
    if seed is None:
        HISTORY_FILE.write_text(json.dumps(list(recent)[-120:], indent=2), encoding="utf-8")
        MANIFEST_FILE.write_text(json.dumps(manifest[-60:], indent=2), encoding="utf-8")
    return results
