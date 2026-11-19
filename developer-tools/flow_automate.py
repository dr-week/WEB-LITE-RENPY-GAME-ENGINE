"""Automate 5-prompt Reuse-Prompt batches in Google Flow via Chrome CDP."""

import argparse
import json
import subprocess
import time

from flow_automation.cdp import CdpSession, find_flow_target
from flow_automation.flow_dom import CLICK_REUSE_JS, CLICK_SEND_JS, INSPECT_JS, build_set_prompt_js
from flow_session import update_session
from image_generation.menu_prompts import generate_menu_prompts
from prompt_batch import build_prompt_batch, format_flow_agent_message, mark_dispatched


def build_flow_batch_payload(source: str = "story", count: int = 5, seed: int | None = None) -> tuple[str, int]:
    """Generate a 5-prompt Flow batch string and return (payload, item_count)."""
    if source == "batch":
        batch = build_prompt_batch(limit=min(count, 5), kind="all")
        return (format_flow_agent_message(batch) if batch else "", len(batch))
    items = generate_menu_prompts(min(count, 5), seed, menu_mode=(source == "menu"))
    header = f"Generate {len(items)} 16:9 images using the attached reference images, one for each prompt below:\n\n"
    body = "\n\n".join(f"{i}. {it['title']}\n{it['prompt']}" for i, it in enumerate(items, 1))
    return header + body, len(items)


def _copy_clipboard(text: str):
    try:
        subprocess.run(["clip"], input=text, text=True, check=True)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=9222, help="Chrome CDP port (default: 9222).")
    parser.add_argument("--inspect", action="store_true", help="Inspect the open Google Flow tab DOM.")
    parser.add_argument("--source", choices=["story", "menu", "batch"], default="story")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--no-reuse", action="store_true", help="Skip clicking Reuse Prompt before pasting.")
    parser.add_argument("--no-submit", action="store_true", help="Fill the prompt box without clicking Send.")
    parser.add_argument("--dry-run", action="store_true", help="Copy batch to clipboard without touching Chrome.")
    args = parser.parse_args()

    if args.dry_run:
        text, n = build_flow_batch_payload(args.source, args.count, args.seed)
        _copy_clipboard(text)
        print(f"[Dry-run: copied {n} prompts to clipboard]\n\n{text}")
        return

    target = find_flow_target(args.port)
    if not target:
        raise SystemExit(
            f"No Google Flow tab found on CDP port {args.port}. "
            "Run launcher/tools/Launch Flow Chrome (CDP).bat first."
        )

    cdp = CdpSession(target["webSocketDebuggerUrl"])
    try:
        if args.inspect:
            print(json.dumps(cdp.eval_js(INSPECT_JS), indent=2))
            return
        text, n = build_flow_batch_payload(args.source, args.count, args.seed)
        if not text:
            print("No pending prompts to send.")
            return
        if not args.no_reuse:
            print("Reuse:", cdp.eval_js(CLICK_REUSE_JS))
            time.sleep(0.4)
        print("Input:", cdp.eval_js(build_set_prompt_js(text)))
        if not args.no_submit:
            time.sleep(0.2)
            print("Submit:", cdp.eval_js(CLICK_SEND_JS))
            update_session(prompts=n, notes=f"flow_automate:{args.source}")
            if args.source == "batch":
                mark_dispatched(build_prompt_batch(limit=n, kind="all"))
    finally:
        cdp.close()


if __name__ == "__main__":
    main()
