"""Replace low-quality or flagged images in alias files with better-quality images."""

import argparse
from contextlib import closing
from pathlib import Path
import re
import sqlite3

from image_audit.database import DATABASE, GAME_ROOT

ALIAS_LINE = re.compile(r'^(\s*image\s+[\w]+\s*=.*?["\'])(images/[^"\']+)(["\'].*)$')


def find_replacements(game_root: Path = GAME_ROOT, db_path: Path = DATABASE, min_score: int = 85) -> list[dict]:
    with closing(sqlite3.connect(db_path)) as db:
        db.row_factory = sqlite3.Row
        bad = {
            row["path"]: dict(row)
            for row in db.execute(
                "SELECT path, category, width, height, quality_score, status FROM image_assets "
                "WHERE path LIKE 'images/%' AND (status = 'needs_regen' OR quality_score < ?)",
                (min_score,),
            )
        }
        pool = [dict(row) for row in db.execute(
            "SELECT path, category, width, height, quality_score, status FROM image_assets "
            "WHERE path LIKE 'images/%' AND status != 'needs_regen' AND quality_score >= ? "
            "ORDER BY (status = 'approved') DESC, quality_score DESC, (width * height) DESC",
            (min_score,),
        )]
    used_in_aliases = _collect_alias_paths(game_root)
    plans = []
    for rpy, line_no, old_path in used_in_aliases:
        if old_path not in bad:
            continue
        cat = bad[old_path]["category"]
        candidate = next((c for c in pool if c["category"] == cat and c["path"] != old_path), None)
        if candidate:
            plans.append({"rpy": rpy, "line": line_no, "old": old_path, "new": candidate["path"],
                          "old_score": bad[old_path]["quality_score"], "new_score": candidate["quality_score"]})
    return plans


def _collect_alias_paths(game_root: Path) -> list[tuple[Path, int, str]]:
    found = []
    for rpy in sorted((game_root / "10_characters").glob("*.rpy")):
        for idx, line in enumerate(rpy.read_text(encoding="utf-8-sig").splitlines(), 1):
            if m := ALIAS_LINE.match(line):
                found.append((rpy, idx, m.group(2)))
    return found


def apply_replacements(plans: list[dict], db_path: Path = DATABASE) -> int:
    by_file = {}
    for p in plans:
        by_file.setdefault(p["rpy"], {})[p["line"]] = (p["old"], p["new"])
    for rpy, edits in by_file.items():
        lines = rpy.read_text(encoding="utf-8-sig").splitlines(keepends=True)
        for ln, (old, new) in edits.items():
            lines[ln - 1] = lines[ln - 1].replace(old, new)
        rpy.write_text("".join(lines), encoding="utf-8")
    with closing(sqlite3.connect(db_path)) as db, db:
        for p in plans:
            db.execute("UPDATE image_assets SET status='replaced' WHERE path=?", (p["old"],))
            db.execute("INSERT INTO prompt_history (category, prompt_text, status, parent_asset_path) VALUES (?, ?, 'replaced', ?)",
                       (Path(p["old"]).parts[1], f"Replaced with {p['new']}", p["old"]))
    return len(plans)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply proposed replacements.")
    parser.add_argument("--min-score", type=int, default=85)
    args = parser.parse_args()
    plans = find_replacements(min_score=args.min_score)
    for p in plans:
        print(f"REPLACE {p['rpy'].name}:{p['line']} | {p['old']} ({p['old_score']}) -> {p['new']} ({p['new_score']})")
    if not plans:
        print("No low-quality or flagged alias images need replacement.")
    elif args.apply:
        print(f"Applied {apply_replacements(plans)} replacement(s).")
    else:
        print(f"Dry run: {len(plans)} replacement(s) available. Re-run with --apply.")


if __name__ == "__main__":
    main()
