"""Curate short-duration transition SFX from an external SFX folder into LOLA."""

import argparse
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
DEST_DIR = ROOT / "game" / "audio" / "sfx" / "transitions"
MANIFEST_OUT = ROOT / "game" / "audio" / "sfx_transitions.json"
DEFAULT_SRC = Path(r"C:\Users\disha\Videos\FX\SFX")
PREFERRED_KEYWORDS = ("swoosh", "whoosh", "riser", "zoom", "transition")
REJECT_KEYWORDS = ("airhorn", "heavy", "rock", "clock", "heartbeat", "huge")


def curate_short_sfx(src_dir: Path = DEFAULT_SRC, dest_dir: Path = DEST_DIR,
                     max_bytes: int = 105_000, apply: bool = False) -> list[dict]:
    """Select short-duration swoosh/riser SFX (<= max_bytes) and optionally copy into game/."""
    if not src_dir.is_dir():
        return []
    selected = []
    for path in sorted(src_dir.iterdir()):
        if not path.is_file() or path.suffix.lower() not in {".mp3", ".ogg", ".wav"}:
            continue
        name_low = path.name.lower()
        if any(bad in name_low for bad in REJECT_KEYWORDS):
            continue
        if path.stat().st_size > max_bytes:
            continue
        if not any(good in name_low for good in PREFERRED_KEYWORDS):
            continue
        clean_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in path.stem) + path.suffix.lower()
        dest = dest_dir / clean_name
        if apply:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(path), str(dest))
        selected.append({"file": f"audio/sfx/transitions/{clean_name}", "bytes": path.stat().st_size})
    if apply and selected:
        MANIFEST_OUT.write_text(json.dumps({"schema_version": 1, "sfx": selected}, indent=2) + "\n", encoding="utf-8")
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--max-bytes", type=int, default=105_000)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    items = curate_short_sfx(args.source, DEST_DIR, args.max_bytes, apply=args.apply)
    for item in items:
        print(f"{'COPIED' if args.apply else 'MATCH '} {item['file']} ({item['bytes']} bytes)")
    print(f"Total short transition SFX: {len(items)}")


if __name__ == "__main__":
    main()
