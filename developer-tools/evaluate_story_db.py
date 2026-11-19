"""Evaluate the unified story & image SQLite database."""

import argparse
from contextlib import closing
from pathlib import Path
import sqlite3

from image_audit.database import DATABASE, GAME_ROOT
from story_db import sync_story_db


def evaluate(game_root: Path = GAME_ROOT, db_path: Path = DATABASE) -> None:
    stats = sync_story_db(game_root, db_path)
    print(f"Story DB synced: {stats['nodes']} nodes, {stats['choices']} choices, "
          f"{stats['links']} image links, {stats['endings']} endings.")
    with closing(sqlite3.connect(db_path)) as db:
        prologues = db.execute("SELECT node_id, category FROM story_nodes WHERE node_type='prologue' ORDER BY node_id").fetchall()
        endings = db.execute("SELECT ending_id, title FROM story_endings ORDER BY ending_id").fetchall()
        unhealthy = db.execute(
            "SELECT node_id, asset_path, quality_score, asset_status FROM v_story_image_health "
            "WHERE asset_status IN ('needs_regen', 'missing') OR quality_score < 80"
        ).fetchall()
        unlinked = db.execute(
            "SELECT category, COUNT(*) FROM v_unlinked_good_images GROUP BY category ORDER BY COUNT(*) DESC"
        ).fetchall()
    print(f"Prologues ({len(prologues)}): {', '.join(p[0] for p in prologues)}")
    print(f"Endings ({len(endings)}): {', '.join(f'{e[0]} ({e[1]})' for e in endings)}")
    print(f"Unhealthy story-image links: {len(unhealthy)}")
    for row in unhealthy[:10]:
        print(f"  WARN {row[0]} -> {row[1]} [score={row[2]}, status={row[3]}]")
    print("Unlinked high-quality images available for new story beats:")
    for cat, count in unlinked:
        print(f"  {cat}: {count}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-root", type=Path, default=GAME_ROOT)
    parser.add_argument("--db", type=Path, default=DATABASE)
    args = parser.parse_args()
    evaluate(args.game_root, args.db)


if __name__ == "__main__":
    main()
