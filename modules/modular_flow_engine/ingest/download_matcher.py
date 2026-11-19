"""Matches downloaded Flow images to .prompt_manifest.json and updates catalog."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEV_TOOLS = ROOT / "developer-tools"
GAME_DIR = ROOT / "game"

if str(DEV_TOOLS) not in sys.path:
    sys.path.insert(0, str(DEV_TOOLS))

from image_story_loop.catalog import write_catalog  # noqa: E402
from ingest_flow_download import ingest_file, ingest_latest  # noqa: E402


def ingest_flow_downloads(latest: int | None, file_path: Path | None, asset_id: str | None,
                          downloads_dir: Path, rebuild_catalog: bool = True) -> dict:
    if latest:
        imported = ingest_latest(latest, downloads_dir)
    elif file_path and asset_id:
        imported = [ingest_file(file_path, asset_id)]
    else:
        raise ValueError("Provide --latest N or both --file and --asset-id.")
    rel = [str(p.relative_to(ROOT)).replace("\\", "/") for p in imported]
    cat_info = None
    if imported and rebuild_catalog:
        cat_path, catalog = write_catalog(GAME_DIR)
        cat_info = {"path": str(cat_path.relative_to(ROOT)).replace("\\", "/"), "events": len(catalog["events"])}
    return {"ok": True, "imported": rel, "catalog": cat_info}
