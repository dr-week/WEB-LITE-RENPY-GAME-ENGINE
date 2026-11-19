"""Build structured prompt batches (max 5 per batch) from story, feedback, and themed pools."""

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3

from image_audit.database import DATABASE
from image_audit.schema import SCHEMA_SQL
from image_generation.allure_pose_pools import build_allure_pose_prompts, build_group_tease_prompts
from image_generation.caught_egg_pools import build_caught_egg_prompts, build_hidden_caught_prompts
from image_generation.config import REQUESTS_OUTPUT
from image_generation.daily_replace_pools import build_daily_replace_prompts, build_start_replace_prompts
from image_generation.desperate_story_pools import build_desperate_prompts
from image_generation.easter_egg_pools import build_easter_egg_prompts, build_hazy_egg_prompts
from image_generation.feedback_prompts import export_regen_queue
from image_generation.group_touch_pools import build_group_bold_prompts, build_group_touch_prompts
from image_generation.legacy_replace_pools import build_legacy_girl_prompts
from image_generation.menu_prompts import generate_menu_prompts
from image_generation.outfit_pose_pools import build_navy_mod_prompts, build_outfit_pose_prompts
from image_generation.teasing_story_pools import build_cheeky_start_prompts, build_teasing_prompts
from image_generation.tipsy_oops_pools import build_shameless_pose_prompts, build_tipsy_oops_prompts

MAX_BATCH = 5
POOL_BUILDERS = {
    "desperate": build_desperate_prompts,
    "teasing": build_teasing_prompts,
    "cheeky-start": build_cheeky_start_prompts,
    "easter-eggs": build_easter_egg_prompts,
    "hazy-eggs": build_hazy_egg_prompts,
    "caught-eggs": build_caught_egg_prompts,
    "hidden-caught": build_hidden_caught_prompts,
    "daily-replace": build_daily_replace_prompts,
    "start-flagged": build_start_replace_prompts,
    "legacy-girl": build_legacy_girl_prompts,
    "allure-poses": build_allure_pose_prompts,
    "group-tease": build_group_tease_prompts,
    "group-touch": build_group_touch_prompts,
    "group-bold": build_group_bold_prompts,
    "tipsy-oops": build_tipsy_oops_prompts,
    "shameless-poses": build_shameless_pose_prompts,
    "outfit-poses": build_outfit_pose_prompts,
    "navy-mods": build_navy_mod_prompts,
}


def _sent_keys(db_path: Path) -> set[str]:
    if not db_path.is_file():
        return set()
    with closing(sqlite3.connect(db_path)) as db:
        rows = db.execute("SELECT DISTINCT request_id FROM prompt_history WHERE request_id != ''").fetchall()
    return {row[0] for row in rows}


def _story_items(requests_path: Path, sent: set[str]) -> list[dict]:
    if not requests_path.is_file():
        return []
    reqs = json.loads(requests_path.read_text(encoding="utf-8-sig")).get("requests", [])
    return [{"id": r["storyKey"], "kind": "story", "category": r.get("category", ""),
             "target": r.get("storyFile", ""), "prompt": r["prompt"]}
            for r in reqs if r.get("status") == "needs_generation" and r.get("storyKey") and r["storyKey"] not in sent]


def build_prompt_batch(limit: int = MAX_BATCH, kind: str = "all", include_sent: bool = False,
                       db_path: Path = DATABASE, requests_path: Path = REQUESTS_OUTPUT) -> list[dict]:
    """Return up to 5 structured prompts prioritized by regen -> story -> themed pools -> menu."""
    cap = max(1, min(limit, MAX_BATCH))
    sent = set() if include_sent else _sent_keys(db_path)
    items = []
    if kind in ("all", "regen", "start-flagged", "cheeky-start"):
        items.extend({"id": f"regen:{q['path']}", "kind": "regen", "category": q["category"],
                      "target": q["path"], "prompt": q["suggested_prompt"]}
                     for q in export_regen_queue(db_path) if f"regen:{q['path']}" not in sent)
    if kind in ("all", "story"):
        items.extend(_story_items(requests_path, sent))
    if kind in POOL_BUILDERS and len(items) < cap:
        items.extend(p for p in POOL_BUILDERS[kind](limit=10) if p["id"] not in sent)
    elif kind in ("all", "mixed") and len(items) < cap:
        order = ("desperate", "teasing") if kind == "mixed" else tuple(POOL_BUILDERS)
        for name in order:
            items.extend(p for p in POOL_BUILDERS[name](limit=10) if p["id"] not in sent)
    if kind in ("all", "menu") and len(items) < cap:
        items.extend({"id": m["asset_id"], "kind": "menu", "category": m["category"],
                      "target": "menu_assets", "prompt": m["prompt"]}
                     for m in generate_menu_prompts(count=cap) if m["asset_id"] not in sent)
    return items[:cap]


def mark_dispatched(batch: list[dict], db_path: Path = DATABASE) -> int:
    """Persist dispatched prompts into prompt_history so future batches advance."""
    with closing(sqlite3.connect(db_path)) as db, db:
        db.executescript(SCHEMA_SQL)
        for item in batch:
            db.execute(
                "INSERT INTO prompt_history (request_id, asset_id, category, prompt_text, status, parent_asset_path) "
                "VALUES (?, ?, ?, ?, 'dispatched', ?)",
                (item["id"], item["id"], item["category"], item["prompt"], item.get("target", "")),
            )
    return len(batch)


def format_flow_agent_message(batch: list[dict], kind: str = "all") -> str:
    """Format up to 5 prompts into one copy-ready message for the Google Flow agent."""
    outfit_note = (
        "occasion-specific outfits described in each prompt"
        if kind == "outfit-poses"
        else "boldly customized/modified dark navy-blue t-shirt short dress as described in each prompt, dark slide sandals"
        if kind == "navy-mods"
        else "oversized dark navy-blue t-shirt short dress, dark slide sandals"
    )
    lines = [
        f"Generate {len(batch)} 16:9 images using the attached reference images, one for each prompt below:",
        f"Keep Maya's exact likeness (East Asian young woman, soft round-oval face, gentle rounded cheeks, "
        f"expressive almond eyes, blonde-dipped dark hair, {outfit_note}), "
        "natural off-camera gaze, 2D cel-shaded character in photorealistic world, no text/watermarks.",
        "",
    ]
    for idx, item in enumerate(batch, 1):
        lines.extend([f"{idx}. [{item['id']} | {item['category']}]", item["prompt"], ""])
    return "\n".join(lines).rstrip()


def main():
    choices = ["all", "story", "regen", "mixed", "menu", *POOL_BUILDERS]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=MAX_BATCH, help="Max prompts (capped at 5).")
    parser.add_argument("--kind", choices=choices, default="all")
    parser.add_argument("--include-sent", action="store_true")
    parser.add_argument("--dispatch", action="store_true", help="Record batch as dispatched in SQLite.")
    parser.add_argument("--format", choices=["text", "json", "flow-agent"], default="text")
    args = parser.parse_args()
    batch = build_prompt_batch(args.limit, args.kind, args.include_sent)
    if args.dispatch and batch:
        mark_dispatched(batch)
    if args.format == "json":
        print(json.dumps({"count": len(batch), "prompts": batch}, indent=2))
    elif args.format == "flow-agent":
        print(format_flow_agent_message(batch, args.kind) if batch else "No pending prompts in queue.")
    else:
        for idx, item in enumerate(batch, 1):
            print(f"[{idx}/{len(batch)}] {item['id']} ({item['kind']} | {item['category']})\n  {item['prompt']}\n")
        if not batch:
            print("No pending prompts in queue.")


if __name__ == "__main__":
    main()
