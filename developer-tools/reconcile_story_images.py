"""Preview or place unused image art at matching story beats."""

import argparse
from pathlib import Path

from image_reconciliation import (
    apply_reconciliation,
    plan_reconciliation,
    write_story_proposals,
)
from image_story_loop.catalog import build_catalog, write_catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Insert the reviewed scene placements.")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    game = args.project_root.resolve() / "game"
    proposals, unmatched = plan_reconciliation(game)
    for alias, image, title, target, current, _, _ in proposals:
        location = f"{target[0].relative_to(game)}:{target[1]}"
        print(f"PLACE {alias} | {image} -> {title} [{location}]; current scene: {current or 'none'}")
    for alias, image, reason in unmatched[:20]:
        print(f"REVIEW {alias} ({image}): {reason}")
    if len(unmatched) > 20:
        print(f"... {len(unmatched) - 20} more review notes are in the story proposal log.")
    if args.apply:
        apply_reconciliation(proposals)
        catalog_path, catalog = write_catalog(game)
        event_count = len(catalog["events"])
        image_count = sum(len(event["images"]) for event in catalog["events"])
        _, remaining = plan_reconciliation(game)
        proposal_log = write_story_proposals(game, remaining)
        print(f"Placed {len(proposals)} exact dialogue match(es); added {image_count} images to {event_count} looping story moments.")
        print(f"{len(remaining)} image(s) still need a story decision.")
        print(f"Story loop catalog: {catalog_path.relative_to(args.project_root.resolve())}")
    else:
        proposal_log = write_story_proposals(game, unmatched)
        print(f"Dry run: {len(proposals)} placement(s), {len(unmatched)} for review. Use --apply after reviewing.")
        catalog = build_catalog(game)
        events = catalog["events"]
        images = sum(len(event["images"]) for event in events)
        print(f"Image-driven story loop: {len(events)} moments from {images} images across {len({event['category'] for event in events})} routes.")
        print("Use --apply to add those moments to the playable story loop.")
    print(f"Fresh story proposal log: {proposal_log.relative_to(args.project_root.resolve())}")
    print("Reference-only art is excluded from story proposals.")


if __name__ == "__main__":
    main()
