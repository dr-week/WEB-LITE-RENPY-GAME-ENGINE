import json
from datetime import datetime
from . import beats, references, story_scan
from .targets import story_targets
from .config import GAME, RULES
from .formatting import available_section, curated_section, fresh_section, tagged_section


def build_list():
    return build_outputs()[0]


def build_outputs():
    definitions, events, lines = story_scan.scan()
    fresh, tagged_rows = beats.fresh_story_beats(definitions, events, lines)
    assets = [p for p in (GAME / "images").rglob("*") if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
    tagged = references.tagged_story_assets()
    missing, available = [], []
    for rule in RULES:
        occurrences = events[rule["title"]]
        if not occurrences:
            continue
        request = references.curated_request(rule, occurrences, definitions)
        if references.has_cg_at_dialogue(request["source"], request["line"]):
            continue
        found = [p for p in assets if any(word in p.stem.casefold() for word in rule["filename_keywords"])]
        if found:
            available.append((rule, occurrences, found))
        elif request["key"] in tagged:
            tagged_rows.append((request["key"], tagged[request["key"]], request["source"], request["line"], request["label"], request["dialogue"]))
        else:
            missing.append((rule, occurrences, request))
    requests = [_catalog_item(request["metadata"], "needs_generation", request["prompt"])
                for _, _, request in missing]
    requests.extend(_catalog_item(beat["metadata"], "needs_generation", beat["prompt"])
                    for beat in fresh)
    requests.extend(_tagged_item(item) for item in tagged_rows)
    requests = list({item["storyKey"]: item for item in requests if item["storyKey"]}.values())
    return _format(missing, fresh, available, tagged_rows), {
        "schema_version": 1, "requests": requests, "story_targets": story_targets(lines)}


def _catalog_item(metadata, status, prompt="", image_path=""):
    return {"storyKey": metadata.get("story_key", ""), "category": metadata.get("category", "general_scenes"),
            "role": metadata.get("role", "cg"), "storyFile": metadata.get("story_file", ""),
            "storyLabel": metadata.get("story_label", ""),
            "dialogueContains": metadata.get("dialogue_contains", ""),
            "referenceImages": metadata.get("reference_images", []),
            "starterEgg": metadata.get("starter_egg", ""), "prompt": prompt,
            "imagePath": image_path, "status": status}


def _tagged_item(item):
    key, image, source, line, label, dialogue = item
    path = GAME / image
    try:
        metadata = json.loads(path.with_suffix(".json").read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        metadata = {}
    metadata.update({"story_key": key, "story_file": source, "story_label": label,
                     "dialogue_contains": dialogue, "category": path.parent.name})
    return _catalog_item(metadata, "generated_pending", image_path=image)


def _format(missing, fresh, available, tagged_rows):
    rows = ["# Story-driven image generation list", "", f"Fresh scan: {datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z}",
            "Fresh story dialogue scan with stable request keys and tagged references.", "", "## Fresh image generation requirements", ""]
    if not missing and not fresh:
        rows.append("No missing story visuals detected.")
    for rule, occurrences, request in missing:
        rows.extend(curated_section(rule, occurrences, request))
    rows.append(f"- **New dialogue moments needing a fresh CG:** {len(fresh)}")
    for beat in fresh:
        rows.extend(fresh_section(beat))
    rows.extend(["## Existing art to review", "",
                 "Filename matches only suggest a category. Add a tagged sidecar to route an image to dialogue.", ""])
    if not available and not tagged_rows:
        rows.append("No unplaced art or category-hint matches found.")
    for rule, occurrences, files in available:
        rows.extend(available_section(rule, occurrences, [p.relative_to(GAME).as_posix() for p in files]))
    for item in tagged_rows:
        rows.extend(tagged_section(item))
    rows.extend(["## Summary", "", f"- Curated story gaps: {len(missing)}", f"- Fresh dialogue moments: {len(fresh)}",
                 f"- Existing art groups to review: {len(available) + len(tagged_rows)}", "",
                 "Regenerate with `python developer-tools/generate_image_list.py`.",
                 "Import reviewed files with `python developer-tools/integrate_story_images.py`.", ""])
    return "\n".join(rows)
