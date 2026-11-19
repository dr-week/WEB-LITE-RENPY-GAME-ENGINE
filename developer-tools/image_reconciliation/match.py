"""Suggest one unique story target from curated image-name rules."""

from image_generation.config import LABEL, TEXT
from image_generation.identity import story_request_id
from image_import.matching import image_rule


def filename_story_target(game, image):
    rule = image_rule(image.name)
    if not rule:
        return None, {}, "No curated filename rule matched this picture."
    hits = []
    for path in sorted((game / "40_story").rglob("*.rpy")):
        label = path.stem
        for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            found = LABEL.match(line)
            if found:
                label = found.group(1)
            text = TEXT.match(line)
            if (label == rule["target_label"] and text and
                    rule["target_dialogue"].casefold() in text.group(2).casefold()):
                hits.append((path, number, label, text.group(2)))
    if len(hits) != 1:
        return None, {}, f"Rule '{rule['title']}' found {len(hits)} exact story moments."
    path, number, label, dialogue = hits[0]
    story_file = path.relative_to(game).as_posix()
    metadata = {"story_file": story_file, "story_label": label,
                "dialogue_contains": dialogue, "category": rule["category"],
                "role": "cg", "match_rule": rule["title"],
                "story_key": story_request_id(story_file, label, dialogue)}
    return (path, number, label), metadata, f"Suggested by the '{rule['title']}' image rule."
