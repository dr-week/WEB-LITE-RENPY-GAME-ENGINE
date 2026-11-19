"""Sync in-game Thumbs Up/Down feedback into SQLite and list regeneration targets."""

import argparse
from pathlib import Path

from image_audit import DATABASE, get_flagged_assets, sync_feedback_file
from image_audit.feedback_sync import FEEDBACK_JSON
from image_generation.feedback_prompts import build_regen_prompt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feedback-file", type=Path, default=FEEDBACK_JSON)
    parser.add_argument("--db", type=Path, default=DATABASE)
    args = parser.parse_args()
    stats = sync_feedback_file(args.feedback_file, args.db)
    print(f"Feedback synced: {stats['imported']} new ({stats['flagged']} down, {stats['approved']} up).")
    flagged = get_flagged_assets(args.db)
    if not flagged:
        print("No assets currently flagged for regeneration.")
        return
    print(f"Flagged assets ({len(flagged)}):")
    for item in flagged:
        print(f"- {item['path']} [score={item['quality_score']}, status={item['status']}, reason={item['last_reason'] or 'low_quality'}]")
        print(f"  Suggested prompt fix: {build_regen_prompt(item)}")


if __name__ == "__main__":
    main()
