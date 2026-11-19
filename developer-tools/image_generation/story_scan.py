import re
from .config import GAME, RULES, IMAGE_DEF, LABEL, SCENE, TEXT


def scan():
    definitions, events, story_lines = {}, {rule["title"]: [] for rule in RULES}, []
    for path in sorted(GAME.rglob("*.rpy")):
        label, scene, background_scene = path.stem, None, None
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        for number, line in enumerate(lines, 1):
            match = IMAGE_DEF.match(line)
            if match:
                definitions[match.group(1)] = match.group(2)
            match = LABEL.match(line)
            if match:
                label = match.group(1)
                if path.is_relative_to(GAME / "40_story"):
                    scene = background_scene = None
            match = SCENE.match(line)
            if match:
                scene = match.group(1)
                if scene.startswith("bg_"):
                    background_scene = scene
            text = TEXT.match(line)
            if not text or line.lstrip().startswith("#") or line.rstrip().endswith(":") or not text.group(2).strip():
                continue
            source = path.relative_to(GAME).as_posix()
            record = (label, scene, number, text.group(2), source)
            if path.is_relative_to(GAME / "40_story"):
                story_lines.append((label, scene, background_scene, number, text.group(2), source))
            for rule in RULES:
                if re.search(rule["dialogue_pattern"], text.group(2), re.I):
                    events[rule["title"]].append(record)
    return definitions, events, story_lines


def story_time(label, default):
    if label.startswith("day_02"):
        return "Day 2 morning"
    if label.startswith("day_01") or label in {"travel_bus_stop", "arrive_college", "find_classroom", "class_session"}:
        return "Day 1 morning"
    if label.startswith(("after_class", "travel_to_", "cafe_", "first_work")):
        return "Day 1 afternoon"
    if label.startswith(("end_day", "day_end")):
        return "Day 1 evening"
    return default
