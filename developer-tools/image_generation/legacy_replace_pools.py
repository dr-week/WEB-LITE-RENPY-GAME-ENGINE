"""Auto-build replacement prompts with meme easter eggs for older Girl_* story images."""

import hashlib
from pathlib import Path
from image_audit.database import GAME_ROOT
from .desperate_story_pools import MAYA_CONTINUITY

MEME_EGGS = (
    "subtle 'This Is Fine' tiny orange plush dog beside a coffee mug in the background, no text",
    "subtle 'Distracted Boyfriend' bystander glancing back in the blurred background, no text",
    "subtle 'Stonks' tiny green zigzag neon arrow sticker on a nearby surface, no text",
    "subtle 'Doge' fluffy Shiba Inu peeking into the scene with an approving side-eye, no text",
    "subtle 'Awkward Look Monkey Puppet' side-glance plush keychain on Maya's bag, no text",
    "subtle 'Woman Yelling at a Cat' white cat sitting upright behind a small plate in the background, no text",
    "subtle 'Kermit Sipping Tea' small green frog figurine beside a teacup on a shelf, no text",
)

EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def _scene_from_stem(stem: str) -> str:
    parts = stem.split("_")
    if len(parts) > 1 and len(parts[-1]) == 8:
        parts = parts[:-1]
    phrase = " ".join(parts).replace("Girl ", "Maya ")
    return phrase.strip()


def build_legacy_girl_prompts(limit: int = 5, game_root: Path = GAME_ROOT) -> list[dict]:
    """Scan game/images for older Girl_* story files and emit upgraded Maya + easter-egg prompts."""
    images_dir = game_root / "images"
    if not images_dir.is_dir():
        return []
    seen_scenes, items = set(), []
    for img in sorted(images_dir.rglob("Girl_*")):
        if not img.is_file() or img.suffix.lower() not in EXTS:
            continue
        if img.parent.name in {"character_reference", "menu_assets", "ui", "generated_art"}:
            continue
        scene_desc = _scene_from_stem(img.stem)
        if scene_desc.casefold() in seen_scenes:
            continue
        seen_scenes.add(scene_desc.casefold())
        pid = "leg_" + hashlib.sha1(scene_desc.encode("utf-8")).hexdigest()[:10]
        egg = MEME_EGGS[len(items) % len(MEME_EGGS)]
        prompt = (
            f"[SCENE: {scene_desc}, upgraded cinematic composition with expressive lighting and natural off-camera gaze] "
            f"[EASTER_EGG: {egg}] "
            f"[FRAME: clear cinematic medium-wide shot] "
            f"[CONTINUITY: {MAYA_CONTINUITY}] "
            f"[AVOID: explicit content, nudity, extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
        )
        items.append({
            "id": pid,
            "kind": "legacy-girl",
            "category": img.parent.name,
            "target": img.relative_to(game_root).as_posix(),
            "prompt": prompt,
        })
        if len(items) >= limit:
            break
    return items
