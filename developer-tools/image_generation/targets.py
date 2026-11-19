"""Build selectable story moments that do not already show a CG."""

from collections import Counter
from .identity import story_request_id


def story_targets(story_lines):
    counts = Counter((source, label, dialogue.casefold())
                     for label, _, _, _, dialogue, source in story_lines
                     if len(dialogue.strip()) >= 14)
    targets, seen = [], set()
    for label, scene, _, line, dialogue, source in story_lines:
        identity = (source, label, dialogue.casefold())
        if counts[identity] != 1 or identity in seen or len(dialogue.strip()) < 14:
            continue
        if (scene or "").startswith("cg_"):
            continue
        seen.add(identity)
        targets.append({"storyKey": story_request_id(source, label, dialogue),
                        "storyFile": source, "storyLabel": label,
                        "dialogueContains": dialogue, "line": line,
                        "currentScene": scene or ""})
    return targets
