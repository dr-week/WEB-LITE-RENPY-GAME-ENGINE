"""End-of-session automation: extract a Flow collection ZIP, organize, catalog, and sync story DB."""

import argparse
from pathlib import Path
import shutil
import tempfile
import zipfile

from flow_session import update_session
from image_audit.database import DATABASE
from image_story_loop.catalog import write_catalog
from organize_images import GAME_ROOT, IMAGE_ROOT, category
from replace_low_quality import apply_replacements, find_replacements
from story_db import sync_story_db

EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def find_collection_zip(downloads: Path, collection: str = "") -> Path | None:
    """Find the matching or newest Flow collection .zip in Downloads."""
    zips = sorted((p for p in downloads.glob("*.zip") if p.is_file()), key=lambda p: p.stat().st_mtime, reverse=True)
    if collection:
        slug = collection.strip().casefold()
        exact = next((z for z in zips if slug in z.stem.casefold()), None)
        if exact:
            return exact
    return zips[0] if zips else None


def extract_collection_zip(zip_path: Path, image_root: Path = IMAGE_ROOT) -> list[Path]:
    """Extract images from a Flow collection ZIP into categorized game/images/ subfolders."""
    imported = []
    with tempfile.TemporaryDirectory() as tmp, zipfile.ZipFile(zip_path) as zf:
        tmp_dir = Path(tmp)
        for member in zf.infolist():
            if member.is_dir():
                continue
            name = Path(member.filename).name
            if Path(name).suffix.lower() not in EXTS:
                continue
            extracted = Path(zf.extract(member, tmp_dir))
            dest_dir = image_root / category(name)
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / name
            if dest.exists():
                continue
            shutil.move(str(extracted), str(dest))
            imported.append(dest)
    return imported


def finalize_session(zip_path: Path, game_root: Path = GAME_ROOT, db_path: Path = DATABASE,
                     apply_replacements_flag: bool = False, collection: str = "") -> dict:
    """Extract ZIP, rebuild story catalog, sync story DB, and check quality replacements."""
    imported = extract_collection_zip(zip_path, game_root / "images")
    cat_path, catalog = write_catalog(game_root)
    stats = sync_story_db(game_root, db_path)
    plans = find_replacements(game_root, db_path)
    applied = apply_replacements(plans, db_path) if (apply_replacements_flag and plans) else 0
    update_session(downloaded=len(imported), notes=f"ended:{collection or zip_path.stem}", db_path=db_path)
    return {
        "zip": zip_path.name, "imported": len(imported), "catalog": str(cat_path),
        "events": len(catalog["events"]), "story_stats": stats,
        "replacements_found": len(plans), "replacements_applied": applied,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, help="Explicit path to downloaded Flow collection .zip.")
    parser.add_argument("--collection", default="", help="Collection name to match in Downloads.")
    parser.add_argument("--downloads", type=Path, default=Path.home() / "Downloads")
    parser.add_argument("--apply-replacements", action="store_true", help="Auto-swap low-quality story placeholders.")
    args = parser.parse_args()
    zip_path = args.zip or find_collection_zip(args.downloads, args.collection)
    if not zip_path or not zip_path.is_file():
        raise SystemExit(f"No collection .zip found in {args.downloads} (collection={args.collection!r}).")
    summary = finalize_session(zip_path, apply_replacements_flag=args.apply_replacements, collection=args.collection)
    print(summary)


if __name__ == "__main__":
    main()
