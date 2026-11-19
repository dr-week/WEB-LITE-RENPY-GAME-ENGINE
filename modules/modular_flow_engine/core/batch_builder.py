"""Builds structured Flow prompt batches and queries open story requests."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEV_TOOLS = ROOT / "developer-tools"
REQUESTS_JSON = DEV_TOOLS / "image_requests.json"

if str(DEV_TOOLS) not in sys.path:
    sys.path.insert(0, str(DEV_TOOLS))

from image_generation.menu_prompts import generate_menu_prompts  # noqa: E402


def format_flow_batch(items: list[dict]) -> str:
    header = f"Generate {len(items)} 16:9 images using the attached reference images, one for each prompt below:\n\n"
    body = "\n\n".join(f"{i}. {it['title']}\n{it['prompt']}" for i, it in enumerate(items, 1))
    return header + body


def build_prompt_batch(count: int = 5, seed: int | None = None,
                       story: bool = False, theme: str = "") -> dict:
    items = generate_menu_prompts(count=count, seed=seed, menu_mode=not story, theme=theme)
    return {"ok": True, "count": len(items), "flow_batch": format_flow_batch(items), "items": items}


def list_open_story_requests(refresh: bool = False) -> dict:
    if refresh or not REQUESTS_JSON.is_file():
        subprocess.run([sys.executable, str(DEV_TOOLS / "generate_image_list.py")], cwd=str(DEV_TOOLS), check=True)
    data = json.loads(REQUESTS_JSON.read_text(encoding="utf-8")) if REQUESTS_JSON.is_file() else []
    open_reqs = [r for r in data if isinstance(r, dict) and r.get("status") == "needs_generation"]
    return {"ok": True, "total_requests": len(data), "open_count": len(open_reqs), "open_requests": open_reqs}
