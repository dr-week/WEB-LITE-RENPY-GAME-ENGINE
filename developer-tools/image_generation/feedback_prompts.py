"""Build corrective prompt guidance from in-game Thumbs Down feedback and visual QC."""

from pathlib import Path
from image_audit import DATABASE, get_flagged_assets
from .desperate_story_pools import MAYA_CONTINUITY

REASON_FIXES = {
    "Wrong character / outfit": (
        "Strictly keep Maya in her consistent oversized, mid-thigh dark slate-blue T-shirt dress, "
        "blonde-dipped dark hair, dark slide sandals, clear facial likeness."
    ),
    "Bad anatomy / artifacts": (
        "Clean anatomical proportions, natural hands and fingers, solid ground contact, no extra limbs or distortion."
    ),
    "Wrong setting": (
        "Match the exact story location and time of day clearly in the photorealistic background."
    ),
    "Low quality / blurry": (
        "Sharp focus, crisp 2D cell-shaded character linework over high-detail 16:9 photorealistic background."
    ),
}

DEFAULT_FIX = "Clean composition, matched lighting, sharp 2D cell-shaded Maya over photorealistic 16:9 scene."


def build_regen_prompt(flagged_item: dict, easter_egg: str = "") -> str:
    """Return a structured corrective prompt for a flagged or low-quality asset."""
    name_hint = Path(flagged_item.get("path", "")).stem.replace("_", " ")
    reason = str(flagged_item.get("last_reason", "")).strip()
    fix = REASON_FIXES.get(reason, DEFAULT_FIX)
    scene_hint = f" Scene context: {flagged_item['scene_label']}." if flagged_item.get("scene_label") else ""
    egg_part = f" [EASTER_EGG: {easter_egg}]" if easter_egg else ""
    return (
        f"[SCENE: Regenerate '{name_hint}'.{scene_hint}] "
        f"[FIX: {fix}]{egg_part} "
        f"[CONTINUITY: {MAYA_CONTINUITY}] "
        f"[AVOID: extra limbs, distorted hands, floating feet, text, captions, logos, watermarks]"
    )


def export_regen_queue(db_path: Path = DATABASE) -> list[dict]:
    """Return regeneration queue entries with corrective prompts from SQLite."""
    return [
        {
            "path": item["path"],
            "category": item.get("category", ""),
            "reason": item.get("last_reason", ""),
            "quality_score": item.get("quality_score", 0),
            "suggested_prompt": build_regen_prompt(item),
        }
        for item in get_flagged_assets(db_path)
    ]
