import argparse
import json
from pathlib import Path

from image_import.core import plan_imports


META_HELP = "Exact placement uses sidecar story_key plus story_file/story_label/dialogue_contains."


def write_art_definitions(game, plans):
    new = [f'image {p.alias} = fit_scene_art("images/{p.destination.parent.name}/{p.image.name}")'
           for p in plans if p.alias]
    directory = game / "10_characters"
    files = sorted(directory.glob("generated_art_*.rpy"))
    number = max((int(path.stem.rsplit("_", 1)[-1]) for path in files), default=0)
    target = files[-1] if files else None
    _append_definitions(directory, new, target, number)


def _append_definitions(directory, definitions, target, number):
    while definitions:
        capacity = 98 - len(target.read_text(encoding="utf-8-sig").splitlines()) if target else 97
        if capacity <= 0:
            target = None
            continue
        if target is None:
            number += 1
            target = directory / f"generated_art_{number:03}.rpy"
            target.write_text("# Images imported by integrate_story_images.py\n", encoding="utf-8")
        chunk, definitions = definitions[:capacity], definitions[capacity:]
        with target.open("a", encoding="utf-8", newline="\n") as output:
            output.write("\n".join(chunk) + "\n")


def _place_scenes(plans):
    grouped = {}
    for plan in plans:
        if plan.target:
            path, line, _ = plan.target
            grouped.setdefault(path, []).append((line, plan.alias))
    for path, placements in grouped.items():
        lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
        for line, alias in sorted(placements, reverse=True):
            indent = lines[line - 1][:len(lines[line - 1]) - len(lines[line - 1].lstrip())]
            lines[line - 1:line - 1] = [f"{indent}scene {alias}\n", f"{indent}with dissolve\n"]
        path.write_text("".join(lines), encoding="utf-8")


def _save_sidecar(game, plan):
    data = dict(plan.metadata)
    data.update({"asset_id": plan.asset_id, "category": plan.destination.parent.name,
                 "role": plan.role, "alias": plan.alias})
    data["placement_status"] = "placed" if plan.target else (
        "reference_only" if plan.role == "reference" else "needs_review")
    if plan.target:
        path, line, label = plan.target
        data["story_target"] = {"file": path.relative_to(game).as_posix(),
                                "label": label, "dialogue": data["dialogue_contains"],
                                "line_before_import": line}
    plan.destination.with_suffix(".json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def apply_import(game, plans):
    for plan in plans:
        plan.destination.parent.mkdir(exist_ok=True)
        plan.image.rename(plan.destination)
        if plan.sidecar:
            plan.sidecar.rename(plan.destination.with_suffix(".json"))
    write_art_definitions(game, plans)
    _place_scenes(plans)
    for plan in plans:
        _save_sidecar(game, plan)


def main():
    parser = argparse.ArgumentParser(description="Preview image identity, category, and exact story route.", epilog=META_HELP)
    parser.add_argument("--apply", action="store_true", help="Apply the reviewed categories and explicit placements.")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    game, plans = plan_imports(args.project_root.resolve())
    for plan in plans:
        target = f"{plan.target[0].relative_to(game)}:{plan.target[1]} [{plan.target[2]}]" if plan.target else plan.review
        print(f"{plan.asset_id} | {plan.metadata.get('story_key', 'no request id')} | {plan.role} | {plan.image.name} -> images/{plan.destination.parent.name} | {plan.alias or 'no alias'} | {target}")
    if args.apply:
        apply_import(game, plans)
        print(f"Imported {len(plans)} image(s).")
    else:
        print(f"Dry run: {len(plans)} image(s). Review IDs and targets, then rerun with --apply.")


if __name__ == "__main__":
    main()
