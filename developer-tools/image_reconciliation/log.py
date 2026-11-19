"""Write a fresh, structured review queue for images not safely placed."""

import json
from datetime import datetime
from pathlib import Path

from image_import.core import asset_id
from image_import.matching import load_metadata


def write_story_proposals(game: Path, unmatched: list[tuple[str, str, str]]) -> Path:
    root = game.parent
    items = []
    for name, relative, reason in unmatched:
        image = game / "images" / relative
        if not image.is_file():
            continue
        metadata, _ = load_metadata(image)
        if image.parent.name == "character_reference" or metadata.get("role") == "reference":
            continue
        items.append({
            "asset_id": metadata.get("asset_id") or asset_id(image),
            "image_path": image.relative_to(root).as_posix(),
            "filename": name,
            "category": image.parent.name,
            "role": metadata.get("role", "unset"),
            "caption": metadata.get("caption", ""),
            "story_key": metadata.get("story_key", ""),
            "story_file": metadata.get("story_file", ""),
            "story_label": metadata.get("story_label", ""),
            "dialogue_contains": metadata.get("dialogue_contains", ""),
            "review_reason": reason,
            "status": "needs_human_story_review",
        })
    path = root / "developer-tools" / "story_image_proposals.json"
    payload = {"schema_version": 1, "generated_at": datetime.now().astimezone().isoformat(),
               "items": items}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
