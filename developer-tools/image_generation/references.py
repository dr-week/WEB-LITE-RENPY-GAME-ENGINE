import json
import re
from .config import GAME, SCENE, TEXT
from .identity import story_request_id
from .prompts import structured_prompt, starter_egg


def tagged_story_assets():
    tagged = {}
    for image in (GAME / "images").rglob("*"):
        if not image.is_file() or image.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        sidecar = image.with_suffix(".json")
        if sidecar.is_file():
            try:
                metadata = json.loads(sidecar.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                metadata = {}
            if isinstance(metadata, dict) and metadata.get("story_key"):
                tagged[str(metadata["story_key"])] = image.relative_to(GAME).as_posix()
        for key in re.findall(r"story_[a-f0-9]{10}", image.stem.casefold()):
            tagged.setdefault(key, image.relative_to(GAME).as_posix())
    return tagged


def character_references():
    paths = sorted((GAME / "images" / "character_reference").glob("*"))
    return [p.relative_to(GAME).as_posix() for p in paths if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
            and any(tag in p.stem.casefold() for tag in ("blue_outfit", "turnaround"))]


def curated_request(rule, occurrences, definitions):
    anchor = next((row for row in occurrences if row[0] == rule["target_label"]
                   and rule["target_dialogue"].casefold() in row[3].casefold()), occurrences[0])
    label, _, line, dialogue, source = anchor
    key = story_request_id(source, label, dialogue)
    location = definitions.get(rule["image_alias"], "")
    references = character_references() + ([location] if location else [])
    egg = starter_egg(key)
    metadata = {"category": rule["category"], "role": "cg", "story_file": source,
                "story_label": label, "dialogue_contains": dialogue, "story_key": key,
                "reference_images": references, "starter_egg": egg}
    return {"key": key, "source": source, "label": label, "line": line, "dialogue": dialogue,
            "references": references, "metadata": metadata, "starter_egg": egg,
            "prompt": structured_prompt(key, rule["prompt"], dialogue, location, references)}


def has_cg_at_dialogue(source, line):
    lines = (GAME / source).read_text(encoding="utf-8-sig").splitlines()
    for previous in reversed(lines[max(0, line - 12):line - 1]):
        stripped = previous.strip()
        if not stripped:
            continue
        if stripped == "menu:" or stripped.startswith(("label ", "jump ", "return")):
            break
        if (text := TEXT.match(previous)) and not stripped.endswith(":") and text.group(2).strip():
            break
        scene = SCENE.match(previous)
        if scene:
            return scene.group(1).startswith("cg_")
    return False
