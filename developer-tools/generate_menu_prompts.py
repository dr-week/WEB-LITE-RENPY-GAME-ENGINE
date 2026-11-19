"""CLI to generate fresh Flow-ready 5-prompt batches for LOLA."""

import argparse
import subprocess
from image_generation.menu_prompts import generate_menu_prompts


def main():
    parser = argparse.ArgumentParser(description="Generate artistic LOLA menu/story prompts.")
    parser.add_argument("--count", type=int, default=5, help="Number of prompts to generate.")
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed.")
    parser.add_argument("--story", action="store_true", help="Generate full-bleed story scenes instead of menu art.")
    parser.add_argument("--theme", default="", help="Optional story theme (e.g. body_worry).")
    parser.add_argument("--flow-batch", action="store_true", help="Format as one paste-ready Google Flow batch & copy to clipboard.")
    args = parser.parse_args()
    items = generate_menu_prompts(args.count, args.seed, menu_mode=not args.story, theme=args.theme)
    if args.flow_batch:
        header = f"Generate {len(items)} 16:9 images using the attached reference images, one for each prompt below:\n\n"
        body = "\n\n".join(f"{i}. {it['title']}\n{it['prompt']}" for i, it in enumerate(items, 1))
        text = header + body
        try:
            subprocess.run(["clip"], input=text, text=True, check=True)
            print("[Copied Flow batch to Windows clipboard — click Reuse Prompt, Ctrl+A, Ctrl+V, Enter]\n")
        except Exception:
            pass
        print(text)
    else:
        for idx, item in enumerate(items, start=1):
            print(f"### {idx}. {item['title']}\n- **Suggested filename:** `{item['suggested_filename']}` (`game/images/{item['category']}/`)\n{item['prompt']}\n")


if __name__ == "__main__":
    main()
