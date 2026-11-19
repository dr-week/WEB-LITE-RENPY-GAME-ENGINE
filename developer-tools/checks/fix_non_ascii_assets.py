"""Normalize non-ASCII filenames under game/images/ and update .rpy/.json references."""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "game"
IMAGES = GAME / "images"


def ascii_name(name: str) -> str:
    cleaned = re.sub(r"[^\x00-\x7F]+", "_", name)
    return re.sub(r"_+", "_", cleaned)


def find_non_ascii_files() -> list[tuple[Path, Path]]:
    pairs = []
    for path in sorted(IMAGES.rglob("*")):
        if path.is_file() and any(ord(c) > 127 for c in path.name):
            pairs.append((path, path.with_name(ascii_name(path.name))))
    return pairs


def apply_renames(pairs: list[tuple[Path, Path]]) -> int:
    if not pairs:
        return 0
    replacements = [(old.relative_to(GAME).as_posix(), new.relative_to(GAME).as_posix()) for old, new in pairs]
    for old, new in pairs:
        old.rename(new)
    for target in list(GAME.rglob("*.rpy")) + list((GAME / "data").glob("*.json")):
        text = target.read_text(encoding="utf-8", errors="ignore")
        updated = text
        for old_rel, new_rel in replacements:
            updated = updated.replace(old_rel, new_rel)
            updated = updated.replace(Path(old_rel).name, Path(new_rel).name)
        if updated != text:
            target.write_text(updated, encoding="utf-8")
    return len(pairs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fix non-ASCII filenames under game/images/.")
    parser.add_argument("--apply", action="store_true", help="Rename files and update references.")
    args = parser.parse_args()
    pairs = find_non_ascii_files()
    if not pairs:
        print("OK: No non-ASCII filenames under game/images/.")
        return 0
    for old, new in pairs:
        print(f"{'RENAME' if args.apply else 'WOULD RENAME'}: {old.name} -> {new.name}")
    if args.apply:
        print(f"Updated {apply_renames(pairs)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
