"""Batch-import an external image folder into LOLA with visual QC and catalog refresh."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from image_audit import collect_sources, create_database
from image_import.core import EXTENSIONS, asset_id
from image_import.matching import image_category
from image_quality import inspect_image
from image_story_loop.catalog import write_catalog

ROOT = Path(__file__).resolve().parents[1]


def _existing_hashes(images_dir: Path) -> set[str]:
    return {
        hashlib.sha256(p.read_bytes()).hexdigest()
        for p in images_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    }


def plan_collection_import(source_dir: Path, project_root: Path = ROOT) -> tuple[list[dict], list[dict]]:
    images_dir = project_root / "game" / "images"
    seen = _existing_hashes(images_dir)
    accepted, skipped = [], []
    for src in sorted(source_dir.iterdir()):
        if not src.is_file() or src.suffix.lower() not in EXTENSIONS:
            continue
        qc = inspect_image(src)
        if not qc["ok"]:
            skipped.append({"file": src.name, "reason": f"visual_qc_failed: {qc['flags']}"})
            continue
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        if digest in seen:
            skipped.append({"file": src.name, "reason": "duplicate_sha256"})
            continue
        seen.add(digest)
        category = image_category(src, {})
        dest = images_dir / category / src.name
        if dest.exists():
            skipped.append({"file": src.name, "reason": f"filename_exists_in_{category}"})
            continue
        accepted.append({"src": src, "dest": dest, "category": category, "qc": qc, "aid": asset_id(src)})
    return accepted, skipped


def apply_collection_import(accepted: list[dict], project_root: Path = ROOT, move: bool = False) -> dict:
    for item in accepted:
        item["dest"].parent.mkdir(parents=True, exist_ok=True)
        if move:
            shutil.move(str(item["src"]), str(item["dest"]))
        else:
            shutil.copy2(str(item["src"]), str(item["dest"]))
        sidecar = {
            "asset_id": item["aid"],
            "category": item["category"],
            "role": "cg",
            "placement_status": "story_loop",
            "source_name": item["src"].name,
            "width": item["qc"]["width"],
            "height": item["qc"]["height"],
            "quality_score": item["qc"]["quality_score"],
            "quality_flags": item["qc"]["flags"],
        }
        item["dest"].with_suffix(".json").write_text(
            json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    game = project_root / "game"
    cat_path, catalog = write_catalog(game)
    assets, refs, aliases, alias_refs = collect_sources(game)
    create_database(assets, refs, aliases, alias_refs, game_root=game)
    return {"imported": len(accepted), "events": len(catalog["events"]), "catalog": str(cat_path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Folder containing newly generated images.")
    parser.add_argument("--apply", action="store_true", help="Copy images, write sidecars, and update catalog/DB.")
    parser.add_argument("--move", action="store_true", help="Move files instead of copying when --apply is set.")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    args = parser.parse_args()
    accepted, skipped = plan_collection_import(args.source, args.project_root.resolve())
    for item in accepted:
        qc = item["qc"]
        print(f"IMPORT {item['src'].name} -> images/{item['category']} [{qc['width']}x{qc['height']} score={qc['quality_score']}]")
    for item in skipped:
        print(f"SKIP   {item['file']} ({item['reason']})")
    if args.apply and accepted:
        summary = apply_collection_import(accepted, args.project_root.resolve(), move=args.move)
        print(f"Imported {summary['imported']} image(s). Story loop now has {summary['events']} moments.")
    elif not args.apply:
        print(f"Dry run: {len(accepted)} ready to import, {len(skipped)} skipped. Re-run with --apply.")


if __name__ == "__main__":
    main()
