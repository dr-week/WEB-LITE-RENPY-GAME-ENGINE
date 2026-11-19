"""Index Ren'Py image definitions and identify story usage."""

import re


IMAGE_DEF = re.compile(r'^\s*image\s+((?:bg|cg)_[\w]+)\s*=.*?["\']images/([^"\']+)["\']')
ALIAS_TOKEN = re.compile(r'\b((?:bg|cg)_[\w]+)\b')
LABEL = re.compile(r'^\s*label\s+([\w]+)\s*:')
SCENE = re.compile(r'^\s*scene\s+((?:bg|cg)_[\w]+)\b')


def registered_art(game):
    definitions, source_lines = {}, []
    for path in sorted(game.rglob("*.rpy")):
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            definition = IMAGE_DEF.match(line)
            if definition:
                definitions[definition.group(1)] = (path, definition.group(2).replace("\\", "/"))
            source_lines.append((line, definition.group(1) if definition else None))
    used = {alias for line, defined in source_lines if not line.lstrip().startswith("#")
            for alias in ALIAS_TOKEN.findall(line) if alias != defined}
    return definitions, used


def active_scene(game, target):
    path, line_number, label_target = target
    label, current = path.stem, None
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        found = LABEL.match(line)
        if found:
            label = found.group(1)
        if label != label_target:
            continue
        scene = SCENE.match(line)
        if scene:
            current = scene.group(1)
        if number == line_number:
            return current
    return None
