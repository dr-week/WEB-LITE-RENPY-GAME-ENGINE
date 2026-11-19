"""Apply reviewed aliases, story placements, and sidecar status updates."""

import json
from image_import.core import asset_id
from image_import.matching import explicit_story_target, load_metadata


def apply_reconciliation(proposals):
    _write_definitions(proposals)
    grouped = {}
    for alias, _, _, target, _, _, _ in proposals:
        grouped.setdefault(target[0], []).append((target[1], alias))
    for path, insertions in grouped.items():
        lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
        for number, alias in sorted(insertions, reverse=True):
            indent = lines[number - 1][:len(lines[number - 1]) - len(lines[number - 1].lstrip())]
            lines[number - 1:number - 1] = [f"{indent}scene {alias}\n", f"{indent}with dissolve\n"]
        path.write_text("".join(lines), encoding="utf-8")
    _mark_placements(proposals)


def _write_definitions(proposals):
    pending = [item for item in proposals if item[5] is None]
    if not pending:
        return
    game = next(parent for item in pending for parent in item[3][0].parents if parent.name == "game")
    directory = game / "10_characters"
    directory.mkdir(exist_ok=True)
    files = sorted(directory.glob("generated_art_*.rpy"))
    number = max((int(path.stem.rsplit("_", 1)[-1]) for path in files), default=0)
    target = files[-1] if files else None
    rows = [f'image {item[0]} = fit_scene_art("images/{item[1]}")' for item in pending]
    _append(directory, rows, target, number)


def _append(directory, rows, target, number):
    while rows:
        capacity = 98 - len(target.read_text(encoding="utf-8-sig").splitlines()) if target else 97
        if capacity <= 0:
            target = None
            continue
        if target is None:
            number += 1
            target = directory / f"generated_art_{number:03}.rpy"
            target.write_text("# Images imported by reconcile_story_images.py\n", encoding="utf-8")
        chunk, rows = rows[:capacity], rows[capacity:]
        with target.open("a", encoding="utf-8", newline="\n") as output:
            output.write("\n".join(chunk) + "\n")


def _mark_placements(proposals):
    for alias, relative, _, target, _, _, placement in proposals:
        game = next(parent for parent in target[0].parents if parent.name == "game")
        image = game / "images" / relative
        metadata, _ = load_metadata(image)
        metadata.update(placement)
        explicit_story_target(game, metadata)
        metadata.update({"asset_id": metadata.get("asset_id") or asset_id(image),
                         "alias": alias, "category": image.parent.name,
                         "role": metadata.get("role", "cg"), "placement_status": "placed",
                         "story_target": {"file": target[0].relative_to(game).as_posix(),
                                          "label": target[2], "dialogue": metadata["dialogue_contains"],
                                          "line_before_import": target[1]}})
        image.with_suffix(".json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
