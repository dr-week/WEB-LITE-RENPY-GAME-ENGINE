import json
import re

from generate_image_list import RULES
from image_generation.identity import story_request_id
from organize_images import category as infer_category


LABEL = re.compile(r"^\s*label\s+([\w]+)\s*:")
QUOTED = re.compile(r"""^\s*["']""")


def load_metadata(image):
    sidecar = image.with_suffix(".json")
    if not sidecar.exists():
        return {}, None
    data = json.loads(sidecar.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{sidecar} must contain a JSON object.")
    return data, sidecar


def image_category(image, metadata):
    if str(metadata.get("role", "")).lower() == "reference":
        return "character_reference"
    rule = image_rule(image.name)
    name = str(metadata.get("category") or (rule["category"] if rule else infer_category(image.name))).lower()
    name = {"characters": "character_reference", "backgrounds": "general_scenes",
            "cgs": "general_scenes"}.get(name, name)
    if not re.fullmatch(r"[a-z0-9_-]+", name):
        raise ValueError(f"Invalid image category {name!r} for {image.name}.")
    return name


def explicit_story_target(game, metadata):
    fields = ("story_file", "story_label", "dialogue_contains")
    present = [field for field in fields if str(metadata.get(field, "")).strip()]
    if str(metadata.get("story_key", "")).strip() and not present:
        raise ValueError("story_key requires story_file, story_label, and dialogue_contains.")
    if present and len(present) != len(fields):
        raise ValueError("Story placement metadata must include story_file, story_label, and dialogue_contains.")
    if not all(str(metadata.get(field, "")).strip() for field in fields):
        return None
    expected = story_request_id(metadata["story_file"], metadata["story_label"],
                                metadata["dialogue_contains"])
    supplied = str(metadata.get("story_key", "")).strip()
    if supplied and supplied != expected:
        raise ValueError(f"story_key {supplied!r} does not match target request {expected!r}.")
    metadata["story_key"] = expected
    return target_dialogue(game, metadata, metadata["dialogue_contains"])


def image_rule(filename):
    normalized = filename.casefold()
    scored = [(max(len(tag) for tag in rule["filename_keywords"] if tag in normalized), rule)
              for rule in RULES if any(tag in normalized for tag in rule["filename_keywords"])]
    scored.sort(key=lambda item: (-item[0], item[1]["title"]))
    if not scored or (len(scored) > 1 and scored[0][0] == scored[1][0]):
        return None
    return scored[0][1]


def target_dialogue(game, metadata, needle):
    story = game / "40_story"
    files = [game / metadata["story_file"]] if metadata.get("story_file") else sorted(story.rglob("*.rpy"))
    hits = []
    for path in files:
        path = path.resolve()
        path.relative_to(story.resolve())
        label = path.stem
        for index, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            found = LABEL.match(line)
            if found:
                label = found.group(1)
            if (not metadata.get("story_label") or label == metadata["story_label"]) and QUOTED.match(line) and needle.casefold() in line.casefold():
                hits.append((path, index, label))
    if len(hits) != 1:
        raise ValueError(f"Dialogue target {needle!r} matched {len(hits)} story lines; add a unique story_label.")
    return hits[0]
