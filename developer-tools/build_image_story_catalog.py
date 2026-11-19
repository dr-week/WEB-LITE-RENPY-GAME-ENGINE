"""Refresh the looping story catalog from all organized full-frame art."""

import argparse
from pathlib import Path

from image_story_loop.catalog import write_catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    game = args.project_root.resolve() / "game"
    path, catalog = write_catalog(game)
    categories = {event["category"] for event in catalog["events"]}
    assets = sum(len(event["images"]) for event in catalog["events"])
    print(f"Built {len(catalog['events'])} story moments from {assets} images across {len(categories)} routes.")
    print(f"Catalog: {path.relative_to(args.project_root.resolve())}")


if __name__ == "__main__":
    main()
