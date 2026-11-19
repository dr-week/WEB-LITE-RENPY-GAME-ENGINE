"""Verify Ren'Py story labels, jump/call targets, and JSON data files."""

import json
from pathlib import Path
import re

LABEL_DEF = re.compile(r"^\s*label\s+([\w]+)\s*:")
JUMP_CALL = re.compile(r"^\s*(?:jump|call)\s+(?!expression\b)([\w]+)\b")


def check_story_integrity(game_root: Path) -> dict:
    """Return missing jump/call targets and invalid JSON files under game/."""
    labels, refs, bad_json = set(), [], []
    for rpy in sorted(game_root.rglob("*.rpy")):
        rel = rpy.relative_to(game_root).as_posix()
        for ln, line in enumerate(rpy.read_text(encoding="utf-8-sig").splitlines(), 1):
            if m := LABEL_DEF.match(line):
                labels.add(m.group(1))
            if m := JUMP_CALL.match(line):
                refs.append((rel, ln, m.group(1)))

    starts = game_root / "data" / "story_starts.json"
    if starts.is_file():
        try:
            for item in json.loads(starts.read_text(encoding="utf-8-sig")).get("starts", []):
                if nxt := item.get("next_label"):
                    refs.append(("data/story_starts.json", 1, nxt))
        except json.JSONDecodeError as exc:
            bad_json.append(("data/story_starts.json", str(exc)))

    for jf in sorted((game_root / "data").glob("*.json")):
        try:
            json.loads(jf.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            bad_json.append((jf.relative_to(game_root).as_posix(), str(exc)))

    missing_targets = [(src, ln, tgt) for src, ln, tgt in refs if tgt not in labels]
    return {"ok": not missing_targets and not bad_json, "labels": len(labels),
            "missing_targets": missing_targets, "bad_json": bad_json}
