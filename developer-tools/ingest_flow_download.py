"""Rename, annotate, and auto-catalog Google Flow downloads into LOLA."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from image_story_loop.catalog import write_catalog

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "developer-tools" / "image_generation" / ".prompt_manifest.json"
IMAGES_DIR = ROOT / "game" / "images"
EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ingest_file(src: Path, asset_id: str, manifest_path: Path = MANIFEST, images_dir: Path = IMAGES_DIR) -> Path:
    entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    entry = next((e for e in reversed(entries) if e["asset_id"] == asset_id), None)
    if not entry:
        raise ValueError(f"Unknown asset_id in manifest: {asset_id}")
    dest_dir = images_dir / entry["category"]
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{asset_id}{src.suffix.lower()}"
    shutil.move(str(src), str(dest))
    dest.with_suffix(".json").write_text(json.dumps({
        "asset_id": asset_id, "category": entry["category"],
        "title": entry.get("title", ""), "caption": entry.get("caption", ""),
        "source_name": src.name, "sha256": sha256_file(dest),
    }, indent=2), encoding="utf-8")
    return dest


def ingest_latest(count: int, downloads_dir: Path, manifest_path: Path = MANIFEST,
                  images_dir: Path = IMAGES_DIR) -> list[Path]:
    entries = json.loads(manifest_path.read_text(encoding="utf-8"))[-count:]
    files = sorted(
        (p for p in downloads_dir.iterdir() if p.is_file() and p.suffix.lower() in EXTS),
        key=lambda p: p.stat().st_mtime,
    )[-len(entries):]
    return [ingest_file(src, entry["asset_id"], manifest_path, images_dir) for src, entry in zip(files, entries)]


def main():
    parser = argparse.ArgumentParser(description="Match, rename, and catalog Google Flow downloads.")
    parser.add_argument("--file", type=Path, help="Single downloaded Flow image path.")
    parser.add_argument("--asset-id", help="Target ASSET_ID from prompt output.")
    parser.add_argument("--latest", type=int, help="Batch-ingest N newest Downloads matching last N prompts.")
    parser.add_argument("--downloads", type=Path, default=Path.home() / "Downloads", help="Downloads folder.")
    parser.add_argument("--no-rebuild", action="store_true", help="Skip rebuilding image_story_catalog.json.")
    args = parser.parse_args()
    if args.latest:
        imported = ingest_latest(args.latest, args.downloads)
    elif args.file and args.asset_id:
        imported = [ingest_file(args.file, args.asset_id)]
    else:
        return parser.error("Provide --latest N or both --file and --asset-id.")
    for dest in imported:
        print(f"Imported -> {dest.relative_to(ROOT)}")
    if imported and not args.no_rebuild:
        cat_path, catalog = write_catalog(ROOT / "game")
        print(f"Updated {cat_path.relative_to(ROOT)} ({len(catalog['events'])} story moments)")


if __name__ == "__main__":
    main()
