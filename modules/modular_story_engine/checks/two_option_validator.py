"""Validates that story menus strictly follow the 2-option rule."""

import re
from pathlib import Path

MENU_RE = re.compile(r"^(\s*)menu\s*:\s*$")
CHOICE_RE = re.compile(r'^(\s*)"([^"]+)"(?:\s+if\s+[^:]+)?\s*:\s*$')


def count_menu_options(rpy_path: Path) -> list[dict]:
    """Return every menu block in rpy_path with its line number and option count."""
    lines = rpy_path.read_text(encoding="utf-8-sig").splitlines()
    results = []
    i = 0
    while i < len(lines):
        m = MENU_RE.match(lines[i])
        if not m:
            i += 1
            continue
        menu_indent = len(m.group(1))
        choice_indent = None
        options = 0
        j = i + 1
        while j < len(lines):
            raw = lines[j]
            stripped = raw.strip()
            if not stripped or stripped.startswith("#"):
                j += 1
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            if indent <= menu_indent:
                break
            cm = CHOICE_RE.match(raw)
            if cm and (choice_indent is None or indent == choice_indent):
                choice_indent = indent
                options += 1
            j += 1
        results.append({"line": i + 1, "options": options})
        i = j
    return results


def validate_two_option_rule(story_root: Path, allow_files: set[str] | None = None) -> dict:
    allow = allow_files or {"day_hub.rpy", "prologue_starts.rpy", "week_01_eval.rpy", "day_end.rpy", "image_story_hub.rpy"}
    violations = []
    checked = 0
    for rpy in sorted(story_root.rglob("*.rpy")):
        if rpy.name in allow:
            continue
        checked += 1
        for menu in count_menu_options(rpy):
            if menu["options"] != 2:
                violations.append({"file": rpy.name, "line": menu["line"], "options": menu["options"]})
    return {"ok": not violations, "files_checked": checked, "violations": violations}
